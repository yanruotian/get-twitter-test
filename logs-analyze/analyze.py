import os
import re
import sys
import json

import matplotlib.pyplot as plt

def has_chinese(keyword: str):
    return re.search('[\u4e00-\u9fff]', keyword) is not None
    
def get_dir():
    if len(sys.argv) >= 2:
        return sys.argv[1]
    else:
        return os.path.dirname(os.path.abspath(__file__))

def judge_len(length: int):
    def _judge_len(keyword: str):
        if len(keyword) <= length:
            return 1
        else:
            return 0
    return _judge_len

def plot_count_distr(results: dict, png_path: str):
    LEN_RANGE = 40
    def get_count_num(count: int):
        result = 0
        for value in results.values():
            if value <= count:
                result += 1
        return result
    length_dict = {length: get_count_num(length) / len(results) * 100 for length in range(LEN_RANGE)}
    xs = list(range(LEN_RANGE))
    plt.figure()
    plt.plot(xs, [length_dict[x] for x in xs], 'r:o')
    plt.title('twitter data count distribution')
    plt.xlabel('count no more than', loc = 'right')
    plt.ylabel('keyword num', loc = 'top')
    plt.grid(axis = 'y')
    plt.savefig(png_path)

def main():
    DIR = get_dir()
    with open(os.path.join(DIR, 'total_summary.json'), 'r') as file:
        result: dict = json.load(file)
    total_keyword_count = len(result)
    total_data_count = sum(result.values())
    print(f'totally {total_keyword_count} keywords')
    print(f'totally {total_data_count} datas')
    result_list = list(result.items())
    result_list.sort(key = lambda item: -item[1])
    with open(os.path.join(DIR, 'rank.txt'), 'w+') as file:
        for keyword, count in result_list:
            file.write(keyword + ('\t') + f'{count}\n')

    en_result = dict()
    zh_result = dict()
    for keyword, count in result.items():
        if has_chinese(keyword):
            zh_result[keyword] = count
        else:
            en_result[keyword] = count

    plot_count_distr(zh_result, os.path.join(DIR, 'zh_count_distr.png'))
    plot_count_distr(en_result, os.path.join(DIR, 'en_count_distr.png'))

if __name__ == '__main__':
    main()
