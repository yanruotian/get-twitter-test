import os
import re
import json
import datetime

from typing import Set, Dict, List
from argparse import Namespace

from snscrape.modules.twitter import TwitterSearchScraper

DOWNLOAD_NUM_PER_FILE = 10000

class DownloadFileWriter:

    def __init__(self, args: Namespace, begin_file_num: int = 0) -> None:
        self.logger = args.logger
        self.output_path: str = args.output_path
        os.makedirs(self.output_path, exist_ok = True)
        self.file_num = begin_file_num
        self.count = 0
        self.file = None
        self.reopen()

    def __enter__(self):
        return self

    def __exit__(self, *args, **wargs):
        self.close()

    @staticmethod
    def get_file_path(output_path: str, file_num: int) -> str:
        return os.path.join(output_path, f'{file_num :6d}.jsonl'.replace(' ', '0'))

    def reopen(self):
        self.close()
        file_path = self.get_file_path(self.output_path, self.file_num)
        self.logger.logln(f'opening file {file_path} for write...')
        self.file = open(file_path, 'w+')
    
    def close(self):
        if self.file is not None:
            self.file.close()
        self.file = None

    def _update_count(self):
        self.count += 1
        if self.count >= DOWNLOAD_NUM_PER_FILE:
            self.file_num += 1
            self.reopen()
            self.count = 0

    def write(self, obj: Dict[str, str]):
        content = json.dumps(obj, ensure_ascii = False)
        self.file.write(content + '\n')
        self._update_count()

    def writestrln(self, line: str):
        while len(line) > 0 and line[-1] == '\n':
            line = line[ : -1]
        self.file.write(line + '\n')
        self._update_count()


def get_download_keys(args: Namespace) -> List[str]:
    download_key_file_path = os.path.join(args.load_path, f'{args.n :2d}.txt'.replace(' ', '0'))
    args.logger.logln(f'loading download keys from file {download_key_file_path}...')
    with open(download_key_file_path, 'r') as file:
        keys = [line.strip() for line in file]
    args.logger.logln(f'keys = {keys}')
    return keys

def get_used_keys(args: Namespace) -> Set[str]:
    log_file_contents: List[str] = args.logger.log_file_record
    used_keywords_set: Set[str] = {''}
    if log_file_contents is not None:
        for line in log_file_contents:
            line = line.strip()
            re_result = re.search(r'begin scraping keyword "(.+)"', line)
            if re_result is not None:
                keyword = re_result.group(1)
                used_keywords_set.add(keyword)
    return used_keywords_set

def download_one_keyword(args: Namespace, keyword: str, writer: DownloadFileWriter) -> int:
    scraper = TwitterSearchScraper(keyword)
    item_count = 0
    for item in scraper.get_items():
        result: dict = json.loads(item.json())
        result['keyword'] = keyword
        writer.write(result)
        item_count += 1
        if args.time - item.date > datetime.timedelta(days = 2 * 365):
            break
    return item_count

def download(args: Namespace) -> None:

    keys = get_download_keys(args)
    used_keywords_set = get_used_keys(args)

    begin_file_num = 0
    while os.path.exists(DownloadFileWriter.get_file_path(args.output_path, begin_file_num)):
        begin_file_num += 1

    with DownloadFileWriter(args, begin_file_num) as writer:

        for index, keyword in enumerate(keys):
            args.logger.logln(f'begin scraping keyword "{keyword}" ({index} of {len(keys)})...')
            if keyword in used_keywords_set:
                args.logger.logln(f'keyword scraped, skipping...')
                continue
            item_count = download_one_keyword(args, keyword, writer)
            args.logger.logln(f'scraping end, item count = {item_count}')
