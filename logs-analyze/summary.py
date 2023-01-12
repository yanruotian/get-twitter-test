import os
import re
import sys
import json

import matplotlib.pyplot as plt

from typing import Dict, Tuple

def get_one_file(file_path: str):
    with open(file_path, 'r') as file:
        contents = file.readlines()
    result_dict = dict()
    now_keyword = None
    total = None
    for line in contents:
        line = line.strip()
        # begin scraping keyword "沈伯洋" (1 of 275)...
        result = re.search(r'begin scraping keyword "(.+?)" \(([0-9]+) of ([0-9]+)\)...', line)
        if result is not None:
            now_keyword, _, total = result.groups()
            total = int(total)
        else:
            # scraping end, item count = 2594703
            result = re.search(r'scraping end, item count = ([0-9]+)', line)
            if result is not None:
                num = int(result.group(1))
                if now_keyword is None:
                    print(f'err dealing file {file_path}, now_keyword = {now_keyword}, num = {num}')
                    exit(0)
                result_dict[now_keyword] = num
                now_keyword = None
    return result_dict, total, now_keyword

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

def do_plot(result: Dict[str, Tuple[int, int]], png_path: str = 'plot.png'):
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
    plt.savefig(png_path)

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
            result_dict, total, last_keyword = get_one_file(log_path)
            result_dicts.append(result_dict)
            totals.append(total)
            if len(result_dict) != total:
                print(f'file {log_file} not finished, dict size = {len(result_dict)}, total = {total}, last keyword = "{last_keyword}"')
    result_dict = dict()
    for _result_dict in result_dicts:
        result_dict = result_dict | _result_dict
    with open(os.path.join(DIR, 'summary.json'), 'w+') as file:
        json.dump(result_dict, file, ensure_ascii = False)
        
    keyword_len_counts = do_count(result_dict)
    
    do_plot(keyword_len_counts, os.path.join(DIR, 'plot.png'))

if __name__ == '__main__':
    main()
