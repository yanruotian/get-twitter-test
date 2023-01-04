import os
import re
import json
import datetime

from typing import Any, Set, List, Tuple, Union
from argparse import Namespace
from multiprocessing import Pool

from snscrape.modules.twitter import TwitterSearchScraper

from .download import DownloadFileWriter


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
    args.logger.logln(f'keys = {keys}')
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
    scraper = TwitterSearchScraper(keyword + appendix)
    with open(file_path, 'w+') as file:
        for item in scraper.get_items():
            result: dict = json.loads(item.json())
            result['keyword'] = keyword
            file.write(json.dumps(result, ensure_ascii = False) + '\n')
            count += 1

    return keyword, file_path, until, since, count

def process_func(config: Tuple[tuple, Union[int, Any]]):
    args, extra_data = config
    try:
        return download_one_keyword(*args), extra_data
    except Exception as e:
        return None, (args, extra_data, e)


def pooled_download(args: Namespace):

    keys = get_download_keys(args)
    used_keys = get_used_keys(args)
    output_dir: str = args.output_path
    temp_dir: str = os.path.join(output_dir, 'temp')
    os.makedirs(temp_dir, exist_ok = True)
    
    begin_file_num = 0
    while os.path.exists(DownloadFileWriter.get_file_path(args.output_path, begin_file_num)):
        begin_file_num += 1

    with DownloadFileWriter(args, begin_file_num) as writer:

        temp_count: int = 0
        download_configs: List[Tuple[tuple, int]] = []
        for key in keys:
            for month in range(2 * 12):
                if (key, month) not in used_keys:
                    until = datetime.datetime.now() - datetime.timedelta(days = month * 30)
                    since = until - datetime.timedelta(days = 30)
                    temp_file_path = os.path.join(temp_dir, f'{temp_count: 6d}.jsonl'.replace(' ', '0'))
                    download_configs.append(((key, temp_file_path, until, since), month))
                    temp_count += 1

        with Pool(int(args.n)) as pool:
            for result in pool.imap_unordered(process_func, download_configs):
                func_result, extra_data = result
                if func_result is None:
                    func_args, month, err = extra_data
                    key, temp_file_path, until, since = func_args
                    args.logger.logln(f'exception occurred in keyword "{key}", month {month}')
                    args.logger.logln(f'    func args = {func_args}')
                    args.logger.logln(f'    exception = {err}')
                    continue
                (keyword, temp_file_path, until, since, count) = func_result
                month = extra_data
                with open(temp_file_path, 'r') as temp_file:
                    for line in temp_file:
                        line = line.strip()
                        if len(line) > 0:
                            writer.writestrln(line)
                os.remove(temp_file_path)
                args.logger.logln(f'scraping end, keyword = "{keyword}", month = {month}, count = {count}, until = {until}, since = {since}')
