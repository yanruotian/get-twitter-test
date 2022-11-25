import os
import re
import json

from tqdm import tqdm

def count_file(file_path: str):
    count = None
    total = None
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            result = re.match(r'begin scraping keyword ".+" \(([0-9]+) of ([0-9]+)\)', line)
            if result is not None:
                count = int(result.group(1))
                total = int(result.group(2))
    return count, total

def main():
    info_list = []
    for file_name in os.listdir('./'):
        if file_name[-4 : ] == '.log':
            info = {'file name': file_name}
            count, total = count_file(os.path.join('./', file_name))
            info['count'] = count
            info['total'] = total
            info_list.append(info)
    print(info_list)
    sum_count = sum([info['count'] for info in info_list])
    sum_total = sum([info['total'] for info in info_list])
    print(f'sum count = {sum_count}, sum total = {sum_total}')

def deal_line(line: str, summary: dict):
    item = json.loads(line)
    keyword = item['keyword']
    info = False
    if keyword == '长征五号B运载火箭':
        info = True
    if summary.get(keyword, None) is None:
        summary[keyword] = 0
    summary[keyword] += 1
    return info

def deal_json_file(file_path: str, summary: dict):
    info = False
    with open(file_path, 'r') as file:
        for line in file:
            if len(line.strip()) > 0:
                if deal_line(line, summary):
                    info = True
    if info:
        print(f'file {file_path} has info')

def main2(summary_json_path: str = None):
    if summary_json_path is None:
        file_paths = set()
        for dir_name in os.listdir('./'):
            dir_path = os.path.join('./', dir_name)
            if os.path.isdir(dir_path):
                for file_name in os.listdir(dir_path):
                    if file_name[-6 : ] == '.jsonl':
                        file_paths.add(os.path.join(dir_path, file_name))
        with open('file_paths.txt', 'w+') as file:
            file.write(f'{sorted(list(file_paths))}')
        summary = dict()
        for file_path in tqdm(file_paths):
            deal_json_file(file_path, summary)
        with open('summary.json', 'w+') as file:
            file.write(json.dumps(summary, ensure_ascii = False))
    else:
        with open(summary_json_path, 'r') as file:
            summary = json.loads(file.read())
    keyword_count = len(summary.keys())
    total_count = 0
    keyword_len_counts = dict()
    for keyword in summary.keys():
        total_count += summary[keyword]
        length = len(keyword)
        if keyword_len_counts.get(length, None) is None:
            keyword_len_counts[length] = (0, 0)
        en, zh = keyword_len_counts[length]
        if re.search('[\u4e00-\u9fff]+', keyword) is not None:
            zh += summary[keyword]
        else:
            en += summary[keyword]
        keyword_len_counts[length] = (en, zh)
    print(f'totally {keyword_count} keywords')
    print(f'totally {total_count} data')
    print(keyword_len_counts)

if __name__ == '__main__':
    # main2('summary.json')
    main2()
