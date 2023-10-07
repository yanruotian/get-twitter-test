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
MAX_DATA_COUNT = 200000
MAX_DATA_COUNT = float('inf')

def _get_download_keys(args: Namespace, download_key_file_path: str) -> List[str]:
    args.logger.logln(f'loading download keys from file {download_key_file_path}...')
    keys = []
    with open(download_key_file_path, 'r') as file:
        for line in file:
            line = line.strip()
            keyword = re.sub(r'(since|until):\S+', '', line).strip()
            if re.search('[\u4e00-\u9fff]', keyword) is None and len(keyword) <= 2:
                args.logger.logln(f'[keys too short] skipping key "{line}" (len = {len(keyword)})')
            else:
                keys.append(line)
    return keys

def get_download_keys(args: Namespace) -> List[str]:
    download_key_dir_path: str = args.load_path
    keys = []
    for file_name in os.listdir(download_key_dir_path):
        file_path = os.path.join(download_key_dir_path, file_name)
        if file_name.endswith(f'.{args.file_type}') and os.path.isfile(file_path):
            keys += _get_download_keys(args, file_path)
    return keys

def get_used_keys(args: Namespace) -> Set[Tuple[str, int]]:
    log_file_contents: List[str] = args.logger.log_file_record
    used_keywords_set = set()
    if log_file_contents is not None:
        for line in log_file_contents:
            line = line.strip()
            re_result = re.search(r'scraping end, keyword = "(.+?)", month = ([0-9]+|None), count = ([0-9]+)', line)
            if re_result is not None:
                keyword = re_result.group(1)
                month = (lambda s: None if s == 'None' else int(s))(re_result.group(2))
                count = int(re_result.group(3))
                args.logger.logln(f'[used keys] scraping end, keyword = "{keyword}", month = {month}, count = {count}')
                used_keywords_set.add((keyword, month))
    return used_keywords_set

def download_one_keyword(
        keyword: str, 
        file_path: str,
        until: datetime.datetime = None, 
        since: datetime.datetime = None,
    ):

    until_str = until.strftime(r'%Y-%m-%d') if until is not None else None
    since_str = since.strftime(r'%Y-%m-%d') if since is not None else None
    appendix = (
        (f' until:{until_str}' if until_str is not None else '') + 
        (f' since:{since_str}' if since_str is not None else '')
    )

    print(f'starting "{keyword}", since = "{since_str}", until = "{until_str}"')

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
            if count % 10000 == 0 and count > 0:
                dateStr: str = result.get('date')[: len('xxxx-xx-xx')]
                date = datetime.datetime(*map(int, dateStr.split('-')))
                precentage = (until - date).total_seconds() / (until - since).total_seconds() * 100
                print((
                    f'count = {count} in keyword "{keyword}" (since = {since_str}'
                    f', until = {until_str}) {precentage * 100 :.2f}%'
                ))
            if count >= MAX_DATA_COUNT:
                break

    return keyword, file_path, until, since, count

def process_func(config: Tuple[tuple, Union[int, Any]]):
    args, extra_data = config
    try:
        return download_one_keyword(*args), extra_data
    except Exception as e:
        return None, (args, extra_data, e)

def copy_temp_file(
    args: Namespace, 
    temp_file_path: str, 
    writer: DownloadFileWriter, 
    need_check: bool = True,
):
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
        if temp_file_name.endswith('.jsonl') and os.path.isfile(temp_file_path):
            count = copy_temp_file(args, temp_file_path, writer, need_check = True)
            args.logger.logln(f'[abnormal temp file] temp file "{temp_file_path}" has been cleaned, count = {count}')
            total_count += count
    return total_count

def date_minus(initial: Tuple[int, int], month: int):
    initial_year, initial_month = initial
    result = initial_year * 12 + initial_month - month
    return (result - 1) // 12, (result - 1) % 12 + 1


def pooled_download(args: Namespace):

    output_dir: str = args.output_path
    temp_dir: str = os.path.join(os.path.dirname(output_dir), 'temp')
    os.makedirs(temp_dir, exist_ok = True)
    
    begin_file_num = 0
    while os.path.exists(DownloadFileWriter.get_file_path(args.output_path, begin_file_num)):
        begin_file_num += 1

    def _get_configs(counter_callback = lambda: None, ignore_used_keys = True):
        temp_count: int = 0
        keys = get_download_keys(args)
        used_keys = set() if ignore_used_keys else get_used_keys(args)
        for key in keys:
            if 'since:' in key:
                if (key, None) not in used_keys:
                    temp_file_path = os.path.join(temp_dir, f'{temp_count :06d}.jsonl')
                    yield ((key, temp_file_path, None, None), None)
                    temp_count += 1
                    counter_callback()
            else:
                for month in range(12 * 12):
                    if (key, month) not in used_keys:
                        until = datetime.datetime(*date_minus((2023, 1), month), day = 1)
                        since = datetime.datetime(*date_minus((2023, 1), month + 1), day = 1)
                        temp_file_path = os.path.join(temp_dir, f'{temp_count :06d}.jsonl')
                        yield ((key, temp_file_path, until, since), month)
                        temp_count += 1
                        counter_callback()

    class _CountObj:
        def __init__(self, value: int = 0):
            self.count = value
        def callback(self):
            self.count += 1
    count_obj = _CountObj()
    args.logger.mute = True
    count_obj.count = sum(1 for _ in _get_configs())
    args.logger.mute = False
    
    finished_count = 0
    config_count = 0
    downloaded_data_count = 0
    huge_data_keys: Set[str] = set()
    Pool = {
        'pooled-download': ProcessPool,
        'threaded-download': ThreadPool,
    }.get(args.mode)

    with DownloadFileWriter(args, begin_file_num) as writer:
        temp_data_count = clean_temp_dir(args, temp_dir, writer)
        with Pool(int(args.n)) as pool:
            for result in pool.imap_unordered(
                process_func, _get_configs()
            ):
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
                    info_str = '[too much data] '
                    args.logger.logln(
                        f'{info_str}keyword "{keyword}" (month = {month}, '
                        f'until = {until}, since = {since}) might need manual check'
                    )
                    huge_data_keys.add(keyword)
                else:
                    info_str = ''
                copy_temp_file(args, temp_file_path, writer, need_check = False)
                finished_count += 1
                spent_time = datetime.datetime.now(pytz.UTC) - args.logger.create_time
                avg_time = datetime.timedelta(seconds = int(
                    spent_time.total_seconds() / finished_count
                ))
                total_time = datetime.timedelta(seconds = spent_time.total_seconds())
                args.logger.logln(
                    f'scraping end, keyword = "{keyword}", month = {month}, '
                    f'count = {count}, until = {until}, since = {since} '
                    f'{info_str}({finished_count} / {count_obj.count}, '
                    f'avg time = {avg_time}, total time = {total_time})'
                )
                downloaded_data_count += count
        temp_data_count += clean_temp_dir(args, temp_dir, writer)

    args.logger.logln(
        f'all keywords finished. config count = {config_count}, '
        f'downloaded data count = {downloaded_data_count}, '
        f'extra temp data count = {temp_data_count}'
    )
    args.logger.log_iter(huge_data_keys, prefix = (
        'these keywords might need manual check '
        f'(with count >= {MAX_DATA_COUNT}): '
    ))
