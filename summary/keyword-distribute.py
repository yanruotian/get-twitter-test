'''
统计下载到的文件中每个关键词每日的爬取量。
'''

import os
import re
import json
import operator

from tqdm import tqdm
from typing import Set, Dict, Iterable
from functools import reduce
from collections import defaultdict
from multiprocessing import Pool

INPUT_DIR = '/root/get-twitter-test/downloaded/china-tec-new-2023-05-12'
INPUT_DIR = '/root/get-twitter-test/downloaded/china-2023-05-26'
INPUT_DIR = '/root/get-twitter-test/downloaded/china-tec-2023-06-21'

InfoDict = Dict[str, Dict[str, int]]


def yieldFiles(rootPath: str, fileTypes: Set[str] = set()):
    if (os.path.isfile(rootPath) and (
        len(fileTypes) == 0 or 
        any(rootPath.endswith(fileType) for fileType in fileTypes)
    )):
        yield rootPath
    elif os.path.isdir(rootPath):
        for fileName in os.listdir(rootPath):
            for filePath in yieldFiles(os.path.join(rootPath, fileName), fileTypes):
                yield str(filePath)

def dealKeyword(rawStr: str):
    rawStr = re.sub(r'since:\S+', '', rawStr)
    rawStr = re.sub(r'until:\S+', '', rawStr)
    rawStr = re.sub(r'lang:\S+', '', rawStr)
    return rawStr.strip()

def collectFile(filePath: str) -> InfoDict:
    result = defaultdict(lambda: defaultdict(int))
    with open(filePath, 'r') as file:
        for line in file:
            try:
                obj = json.loads(line)
                result[dealKeyword(obj.get('keyword'))][obj.get('date')[: len('xxxx-xx-xx')]] += 1
            except Exception as e:
                print(f'err in line "{line.strip()}"')
                print(f'    exception = {e}')
                print(f'    file = {filePath}')
    return {key: {key: value for key, value in value.items()} for key, value in result.items()}

def processFunc(filePath: str):
    try:
        return collectFile(filePath)
    except Exception as e:
        print(f'{e.__class__}: {e}')
        print(f'    args = {(filePath, )}')

def joinDicts(dicts: Iterable[InfoDict]) -> InfoDict:
    dicts = (infoDict for infoDict in dicts if infoDict is not None)

    result = defaultdict(lambda: defaultdict(int))
    for infoDict in dicts:
        for keyword, dateDict in infoDict.items():
            for date, count in dateDict.items():
                result[keyword][date] += count
    return result

    # result = defaultdict(dict)
    # keywords: Set[str] = reduce(operator.or_, (infoDict.keys() for infoDict in dicts), set())
    # for keyword in keywords:
    #     dates = reduce(operator.or_, (infoDict.get(keyword, dict()).keys() for infoDict in dicts), set())
    #     for date in dates:
    #         result[keyword][date] = sum(infoDict.get(keyword, dict()).get(date, 0) for infoDict in dicts)
    # return result

    # def _joinDicts(dictA: InfoDict, dictB: InfoDict) -> InfoDict:
    #     result = defaultdict(lambda: defaultdict(int))
    #     for keyword in dictA.keys() | dictB.keys():
    #         for date in dictA.get(keyword, dict()).keys() | dictB.get(keyword, dict()).keys():
    #             result[keyword][date] = sum((
    #                 dictA.get(keyword, dict()).get(date, 0),
    #                 dictB.get(keyword, dict()).get(date, 0),
    #             ))
    #     return result
    # return reduce(_joinDicts, dicts, dict())

def main():
    with Pool(32) as pool:
        result = joinDicts(tqdm(pool.imap_unordered(
            collectFile, yieldFiles(INPUT_DIR, {'.jsonl'}),
        )))
    with open(os.path.join(INPUT_DIR, 'keyword-distribution.json'), 'w') as file:
        json.dump(result, file, ensure_ascii = False)

if __name__ == '__main__':
    main()
