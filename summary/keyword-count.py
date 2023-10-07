'''
统计下载到的文件中每个关键词每日的爬取量。
'''

import os
import re
import json
import sqlite3
import operator

from tqdm import tqdm
from typing import Set, Dict, Iterable
from functools import reduce
from collections import defaultdict
from multiprocessing import Pool

INPUT_DIR = '/root/get-twitter-test/downloaded/china-tec-new-2023-05-12'
INPUT_DIR = '/root/get-twitter-test/downloaded/china-2023-05-26'
INPUT_DIR = '/root/wangxing_test/db'

InfoDict = Dict[str, int]


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
    return rawStr.strip()
    rawStr = re.sub(r'since:\S+', '', rawStr)
    rawStr = re.sub(r'until:\S+', '', rawStr)
    rawStr = re.sub(r'lang:\S+', '', rawStr)
    return rawStr.strip()

def collectFile(filePath: str) -> InfoDict:
    result = defaultdict(int)
    conn = sqlite3.connect(filePath)
    for keyword in tqdm(conn.cursor().execute('SELECT keyword from tweet'), filePath):
        result[dealKeyword(keyword[0])] += 1
    conn.close()
    return dict(result)

def processFunc(filePath: str):
    try:
        return collectFile(filePath)
    except Exception as e:
        print(f'{e.__class__}: {e}')
        print(f'    args = {(filePath, )}')

def joinDicts(dicts: Iterable[InfoDict]) -> InfoDict:
    dicts = (infoDict for infoDict in dicts if infoDict is not None)
    result = defaultdict(int)
    for infoDict in dicts:
        for keyword, count in infoDict.items():
            result[keyword] += count
    return result

def main():
    with Pool(32) as pool:
        result = joinDicts(tqdm(pool.imap_unordered(
            collectFile, yieldFiles(INPUT_DIR, {'.db'}),
        )))
    with open(os.path.join(INPUT_DIR, 'keyword-count.json'), 'w') as file:
        json.dump(result, file, ensure_ascii = False)

if __name__ == '__main__':
    main()
