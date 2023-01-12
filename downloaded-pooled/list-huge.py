import os
import re
import json

from tqdm import tqdm
from typing import Union, Iterable
from datetime import datetime, timedelta
from tabulate import tabulate

huge_set = {'Kill both', 'Y-10', 'ele.me', 'Link Space', 'Chinese Internet', 'NJ1', 'Change 4', 'Y-11', 'Ktt', 'weibo.com', 'POTASSIUM', 'T.T.Yu', 'Sense Time', '美的', 'T91', 'T-91', 'BOKE', 'AT-3', 'S. S. Sin', 'Aliexpress', 'TH-2', 'realme', 'Internet (China)', 'J-10', 'qq.com', 'T-63', 'EAST', 'MLR', 'SUNDAY', 'Z.T.E.', 'moda', 'Y-9', 'MiHoYo', 'HoYoverse', 'PEOPLES', 'AVIC', 'China Internet', 'AUO', 'F-10', 'Sinovac', 'Y-8', 'Shi Z', 'NAER', 'Mi 8', 'Base 20', '雄三', 'SS9', 'NOW TV', 'One plus', 'J-8', 'Nimo TV', 'nimo.tv', 'SBI', 'J-11', 'SIMIT', 'One+', 'Tsmc', 'T-86', 'bilibili', 'Y-12'}
huge_set = {'AT-3', 'Change 4', 'EAST', 'One+', 'PEOPLES', 'SUNDAY', 'moda', 'ele.me'}

def main():
    with open('huge.txt', 'w+') as file:
        for keyword in huge_set:
            file.write(keyword + '\n')

def str_to_date(date: str):
    year, month, day = tuple(date.split('-'))
    return datetime(year = int(year), month = int(month), day = int(day))

def get_log_content():
    FILE_NAME = './pooled-download.log.bak'
    with open(FILE_NAME, 'r') as file:
        content = file.readlines()
    return [line.strip() for line in content]

def get_process_info(keyword: int, file_path: str, until: datetime) -> Union[datetime, None]:
    last_date = None
    with open(file_path, 'r') as file:
        for line in tqdm(file, desc = f'keyword - {file_path}'):
            obj = json.loads(line)
            if keyword == obj['keyword']:
                new_last_date = str_to_date(re.match(r'[0-9]+-[0-9]+-[0-9]+', obj['date']).group(0))
                if new_last_date < until and new_last_date > until - timedelta(days = 30):
                    last_date = new_last_date
            elif last_date is not None:
                break
    return last_date
 
def main2():
    content = get_log_content()
    huge_dict = {keyword: [] for keyword in huge_set}
    last_json_file = ''
    for line in tqdm(content):
        json_file_maybe = re.search(r'opening file (.+?.jsonl) for write...', line)
        if json_file_maybe is not None:
            last_json_file = json_file_maybe.group(1)
            continue
        too_much_maybe = re.search(r'scraping end, keyword = "(.+?)", month = [0-9]+, count = [0-9]+, until = ([0-9]+-[0-9]+-[0-9]+)', line)
        if too_much_maybe is not None:
            keyword = too_much_maybe.group(1)
            until = str_to_date(too_much_maybe.group(2))
            if keyword not in huge_dict:
                continue
            last_date = get_process_info(keyword, last_json_file, until)
            if last_date is None:
                print(f'err: no matched content for keyword "{keyword}" (json file = {last_json_file})')
                continue
            time_delta = until - last_date
            huge_dict[keyword].append(time_delta.total_seconds() / timedelta(days = 30).total_seconds())
    table_content = []
    for keyword, detail in huge_dict.items():
        mean = sum(detail) / len(detail)
        table_content.append((keyword, mean, ', '.join([str(value) for value in detail])))
    table_content.sort(key = lambda x: x[0])
    table = tabulate(table_content, headers = ['keyword', 'mean', 'detail'], tablefmt = 'grid')
    print(table)
    with open('huge-table.txt', 'w+') as file:
        file.write(table)


class FilesReader:

    def __init__(self, file_paths: list) -> None:
        self.file_paths = file_paths
        self.file_index = 0
        self.file: Union[None, Iterable[str]] = None
        assert(len(self.file_paths) > 0)
        self.open()

    def __enter__(self):
        return self

    def __exit__(self, *args, **wargs):
        self.close()

    def open(self):
        self.close()
        if self.file_index < len(self.file_paths):
            file_path: str = self.file_paths[self.file_index]
            print(f'[FilesReader] open file {file_path}')
            self.file = open(file_path, 'r')

    def close(self):
        if self.file is not None:
            self.file.close()
            self.file = None
            self.file_index += 1

    def readall(self):
        while self.file is not None:
            for line in self.file:
                line = line.strip()
                if len(line) == 0:
                    continue
                yield line
            self.open()


def write_huge_sample(file_path: str, keyword: str, json_files: list, sample_num: int):
    count = 0
    with open(file_path, 'w+') as sample_file:
        with FilesReader(json_files) as reader:
            for line in reader.readall():
                obj: dict = json.loads(line)
                if obj['keyword'] == keyword:
                    sample_file.write(obj['content'].replace('\n', '\\n') + '\n')
                    count += 1
                if count >= sample_num:
                    break
        
def main3():
    content = get_log_content()
    huge_dict = {keyword: [] for keyword in huge_set}
    last_json_files = []
    for line in tqdm(content):
        json_file_maybe = re.search(r'opening file (.+?.jsonl) for write...', line)
        if json_file_maybe is not None:
            last_json_file = json_file_maybe.group(1)
            last_json_files.append(last_json_file)
            continue
        too_much_maybe = re.search(r'scraping end, keyword = "(.+?)", month = [0-9]+, count = [0-9]+, until = ([0-9]+-[0-9]+-[0-9]+)', line)
        if too_much_maybe is not None:
            keyword = too_much_maybe.group(1)
            if keyword in huge_dict:
                huge_dict[keyword] += last_json_files
            last_json_files = []

    HUGE_SAMPLE_DIR = './huge-sample'
    DATA_PER_TXT = 20000
    os.makedirs(HUGE_SAMPLE_DIR, exist_ok = True)
    for keyword, json_files in tqdm(huge_dict.items(), 'writing txts'):
        print(f'keyword = "{keyword}", files = {json_files}')
        if len(json_files) == 0:
            print(f'err: keyword "{keyword}" with no json file')
            continue
        sample_file_path = os.path.join(HUGE_SAMPLE_DIR, f'{keyword}.txt')
        write_huge_sample(sample_file_path, keyword, json_files, DATA_PER_TXT)

if __name__ == '__main__':
    main3()
