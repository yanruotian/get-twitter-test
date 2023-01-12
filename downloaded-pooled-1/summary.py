import os
import re
import sys
import json

import matplotlib.pyplot as plt

from typing import Dict, List, Tuple

def get_one_file(file_path: str):
    with open(file_path, 'r') as file:
        contents = file.readlines()
    result_dict: Dict[str, int] = dict()
    total = None
    for line in contents:
        line = line.strip()
        total_maybe = re.search(r'keys = (.+)$', line)
        if total_maybe is not None:
            total: List[str] = eval(total_maybe.group(1))
            continue
        # scraping end, keyword = "Yangtze Memory Technology Corp", month = 1, count = 0
        scraping_end_maybe = re.search(r'scraping end, keyword = "(.+?)", month = [0-9]+, count = ([0-9]+)', line)
        if scraping_end_maybe is not None:
            keyword = scraping_end_maybe.group(1)
            count = int(scraping_end_maybe.group(2))
            if keyword not in result_dict:
                result_dict[keyword] = 0
            result_dict[keyword] += count
            continue
    if total is None:
        print(f'total is None in file {file_path}')
        exit()
    return result_dict, len(total)

def do_count(summary: Dict[str, int]):
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
    return keyword_len_counts

def do_plot(result: Dict[str, Tuple[int, int]]):
    max_len = max(result.keys())
    max_len = 10
    xs = [i for i in range(1, max_len + 1)]
    ys = [result.get(x, (0, 0)) for x in xs]
    en_ys = [i[0] for i in ys]
    zh_ys = [i[1] for i in ys]
    _sum = sum(en_ys) + sum(zh_ys)
    en_ys = [y / _sum * 100 for y in en_ys]
    zh_ys = [y / _sum * 100 for y in zh_ys]
    xs = [str(i) for i in xs]
    font_dict = dict()
    plt.figure()
    plt.plot(xs, en_ys, 'b:o', label = 'en')
    plt.plot(xs, zh_ys, 'r:o', label = 'zh')
    plt.title('twitter data distribution', fontdict = font_dict)
    plt.xlabel('keyword length', loc = 'right', fontdict = font_dict)
    plt.ylabel('data amount precentage (%)', loc = 'top', fontdict = font_dict)
    plt.grid(axis = 'y')
    plt.legend()
    plt.savefig('plot.png')

def get_dir():
    if len(sys.argv) >= 2:
        return sys.argv[1]
    else:
        return os.path.dirname(os.path.abspath(__file__))

def main():
    DIR = get_dir()
    result_dicts = []
    totals = []
    for log_file in os.listdir(DIR):
        log_path = os.path.join(DIR, log_file)
        if log_file[-4 : ] == '.log' and os.path.isfile(log_path):
            print(f'dealing file {log_file}')
            result_dict, total = get_one_file(log_path)
            result_dicts.append(result_dict)
            totals.append(total)
            if len(result_dict) != total:
                print(f'file {log_file} not finished, dict size = {len(result_dict)}, total = {total}')
    result_dict = dict()
    for _result_dict in result_dicts:
        result_dict = result_dict | _result_dict
    with open('summary.json', 'w+') as file:
        json.dump(result_dict, file, ensure_ascii = False)
        
    keyword_len_counts = do_count(result_dict)
    
    do_plot(keyword_len_counts)

if __name__ == '__main__':
    main()
