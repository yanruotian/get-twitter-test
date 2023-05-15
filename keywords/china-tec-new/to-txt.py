'''
若天，想让你爬取“中国科技实体中英文推文数据集”，具体需求如下：

一、爬虫关键词

4个文件的所有关键词，但是注意无需爬取噪音文件的所有关键词（这些关键词不一定出现在4个文件中）

4个文件（0411去重版）
（1）en_label_lower
（2）en_alias_lower
（3）zh_label_simple（原文件仅为简体，需转换为繁体，繁简体均爬取）
（4）zh_alias_simple（原文件仅为简体，需转换为繁体，繁简体均爬取）

噪音文件：noise.csv（即其中的关键词无需爬取）

二、爬虫设置

（1）按月份爬取
（2）只要包含关键词就爬取该推文，无论其是否相邻
（3）数据采集时间：2011年1月1日-2022年12月31日
（4）不设置推文20000条/月的阈值截流，即直接爬取所有推文
（5）32进程

三、需要注意的细节/bug

（1）爬取推文文件缺失问题
（2）推文时间判断条件
（3）爬取中断如何处理
（4）log文件：根据log文件看每个关键词每月的爬取推文数量

四、其他设置尽量与之前爬整体的保持一致，辛苦若天仔细阅读并确认无误后再爬取，如有不确定的辛苦及时反馈
'''

import json

from typing import Set
from zhconv import convert

def getNoise(path: str = 'noise.csv') -> Set[str]:
    with open(path, 'r') as file:
        result = {line.strip().lower() for line in file}
    result |= {convert(keyword, 'zh-hant') for keyword in result}
    return result

def getKeywords(
    paths: Set[str] = {
        'en_alias_lower.json', 'en_label_lower.json',
        'zh_alias_simple.json', 'zh_label_simple.json',
    },
) -> Set[str]:
    result = set()
    for path in paths:
        with open(path, 'r') as file:
            obj = json.load(file)
            for keywordList in obj.values():
                result |= {keyword.strip().lower() for keyword in keywordList}
    result |= {convert(keyword, 'zh-hant') for keyword in result}
    return result

def main():
    keywords = getKeywords() - getNoise()
    with open('keywords.txt', 'w') as file:
        file.write('\n'.join(keywords))

if __name__ == '__main__':
    main()
    