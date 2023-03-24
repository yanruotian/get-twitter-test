import os
import re
import json
import pytz
import datetime

from typing import Any, Set, List, Tuple, Union
from argparse import Namespace

from snscrape.modules.twitter import TwitterSearchScraper

from multiprocessing import Pool as ProcessPool
from multiprocessing.dummy import Pool as ThreadPool

from .download import DownloadFileWriter


# 一个任务中下载的数据数如果超过这个值，会被截断，经过进一步的人工筛查之后再修改这个值进行下载
# MAX_DATA_COUNT = 20000
MAX_DATA_COUNT = float('inf')

def _get_download_keys(args: Namespace, download_key_file_path: str) -> List[str]:
    args.logger.logln(f'loading download keys from file {download_key_file_path}...')
    keys = []
    with open(download_key_file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if re.search('[\u4e00-\u9fff]', line) is None and len(line) <= 2:
                args.logger.logln(f'[keys too short] skipping key "{line}" (len = {len(line)})')
            else:
                keys.append(line)
    args.logger.log_iter(keys, prefix = 'keys = ')
    return keys

def get_download_keys(args: Namespace) -> List[str]:
    download_key_dir_path: str = args.load_path
    keys = []
    for file_name in os.listdir(download_key_dir_path):
        file_path = os.path.join(download_key_dir_path, file_name)
        if file_name[-4 : ] == '.txt' and os.path.isfile(file_path):
            keys += _get_download_keys(args, file_path)
    return keys

def get_used_keys(args: Namespace) -> Set[Tuple[str, int]]:
    log_file_contents: List[str] = args.logger.log_file_record
    used_keywords_set = set()
    if log_file_contents is not None:
        for line in log_file_contents:
            line = line.strip()
            re_result = re.search(r'scraping end, keyword = "(.+?)", month = ([0-9]+), count = ([0-9]+)', line)
            if re_result is not None:
                keyword = re_result.group(1)
                month = int(re_result.group(2))
                count = int(re_result.group(3))
                args.logger.logln(f'[used keys] scraping end, keyword = "{keyword}", month = {month}, count = {count}')
                used_keywords_set.add((keyword, month))
    return used_keywords_set

def download_one_keyword(
        keyword: str, 
        file_path: str,
        until: datetime.datetime = datetime.datetime.now(), 
        since: datetime.datetime = datetime.datetime.now() - datetime.timedelta(days = 2 * 365)
    ):

    until_str = until.strftime(r'%Y-%m-%d')
    since_str = since.strftime(r'%Y-%m-%d')
    appendix = f' until:{until_str} since:{since_str}'

    count = 0
    # 注意：由于推特API改版导致以往写法不可用，以后或可将top = True删去
    # 具体可见：https://github.com/JustAnotherArchivist/snscrape/issues/641
    scraper = TwitterSearchScraper(keyword + appendix)
    with open(file_path, 'w+') as file:
        for item in scraper.get_items():
            result: dict = json.loads(item.json())
            result['keyword'] = keyword
            file.write(json.dumps(result, ensure_ascii = False) + '\n')
            count += 1
            if count >= MAX_DATA_COUNT:
                break

    return keyword, file_path, until, since, count

def process_func(config: Tuple[tuple, Union[int, Any]]):
    args, extra_data = config
    try:
        return download_one_keyword(*args), extra_data
    except Exception as e:
        return None, (args, extra_data, e)

def copy_temp_file(args: Namespace, temp_file_path: str, writer: DownloadFileWriter, need_check: bool = True):
    count = 0
    with open(temp_file_path, 'r') as temp_file:
        for line in temp_file:
            line = line.strip()
            if len(line) == 0:
                continue
            if need_check:
                try:
                    assert(isinstance(json.loads(line), dict))
                except Exception as e:
                    args.logger.logln(f'problem at temp file "{temp_file_path}", line "{line}"')
                    args.logger.logln(f'    exception = {e}')
                    continue
            writer.writestrln(line)
            count += 1
    os.remove(temp_file_path)
    return count

def clean_temp_dir(args: Namespace, temp_file_dir: str, writer: DownloadFileWriter):
    total_count = 0
    for temp_file_name in os.listdir(temp_file_dir):
        temp_file_path = os.path.join(temp_file_dir, temp_file_name)
        if temp_file_name[-6 : ] == '.jsonl' and os.path.isfile(temp_file_path):
            count = copy_temp_file(args, temp_file_path, writer, need_check = True)
            args.logger.logln(f'[abnormal temp file] temp file "{temp_file_path}" has been cleaned, count = {count}')
            total_count += count
    return total_count

def date_minus(initial: Tuple[int, int], month: int):
    initial_year, initial_month = initial
    result = initial_year * 12 + initial_month - month
    return (result - 1) // 12, (result - 1) % 12 + 1


def pooled_download(args: Namespace):

    keys = get_download_keys(args)
    output_dir: str = args.output_path
    temp_dir: str = os.path.join(os.path.dirname(output_dir), 'temp')
    os.makedirs(temp_dir, exist_ok = True)
    
    begin_file_num = 0
    while os.path.exists(DownloadFileWriter.get_file_path(args.output_path, begin_file_num)):
        begin_file_num += 1

    def _get_configs(counter_callback = lambda: None):
        temp_count: int = 0
        used_keys = get_used_keys(args)
        download_configs: List[Tuple[tuple, int]] = []
        for key in keys:
            for month in range(12 * 12):
                if (key, month) not in used_keys:
                    until = datetime.datetime(*date_minus((2022, 12), month), day = 1)
                    since = datetime.datetime(*date_minus((2022, 12), month + 1), day = 1)
                    temp_file_path = os.path.join(temp_dir, f'{temp_count :06d}.jsonl')
                    download_configs.append(((key, temp_file_path, until, since), month))
                    temp_count += 1
                    counter_callback()
        return download_configs

    class _CountObj:
        def __init__(self, value: int = 0):
            self.count = value
        def callback(self):
            self.count += 1
    count_obj = _CountObj()
    finished_count = 0
    config_count = 0
    downloaded_data_count = 0
    huge_data_keys: Set[str] = set()
    Pool = ThreadPool if args.mode == 'threaded-download' else ProcessPool

    with DownloadFileWriter(args, begin_file_num) as writer:
        temp_data_count = clean_temp_dir(args, temp_dir, writer)
        with Pool(int(args.n)) as pool:
            for result in pool.imap_unordered(process_func, _get_configs(lambda: count_obj.callback())):
                config_count += 1
                func_result, extra_data = result
                if func_result is None:
                    func_args, month, err = extra_data
                    key, temp_file_path, until, since = func_args
                    args.logger.logln(f'exception occurred in keyword "{key}", month {month}')
                    args.logger.logln(f'    func args = {func_args}')
                    args.logger.logln(f'    exception = {err}')
                    continue
                keyword, temp_file_path, until, since, count = func_result
                month = extra_data
                if count >= MAX_DATA_COUNT:
                    args.logger.logln(f'[too much data] keyword "{keyword}" (month = {month}, until = {until}, since = {since}) might need manual check')
                    huge_data_keys.add(keyword)
                copy_temp_file(args, temp_file_path, writer, need_check = False)
                finished_count += 1
                spent_time = datetime.datetime.now(pytz.UTC) - args.logger.create_time
                avg_time = datetime.timedelta(seconds = int(spent_time.total_seconds() / finished_count))
                args.logger.logln(f'scraping end, keyword = "{keyword}", month = {month}, count = {count}, until = {until}, since = {since} ({finished_count} / {count_obj.count}, avg time = {avg_time})')
                downloaded_data_count += count
        temp_data_count += clean_temp_dir(args, temp_dir, writer)

    args.logger.logln(f'all keywords finished. config count = {config_count}, downloaded data count = {downloaded_data_count}, extra temp data count = {temp_data_count}')
    args.logger.log_iter(huge_data_keys, prefix = f'these keywords might need manual check (with count >= {MAX_DATA_COUNT}): ')
