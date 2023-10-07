import os
import re
import json
import operator

import numpy as np

from tqdm import tqdm
from typing import Set, Dict
from functools import reduce 

INPUT_DIR = '/root/get-twitter-test/downloaded/china-2023-05-26'
INPUT_DIR = '/root/get-twitter-test/downloaded/china-tec-new-2023-05-12'
INFO_TXT_PATH = os.path.join(INPUT_DIR, 'keyword-counts.txt')
DOWNLOAD_DIR = os.path.join(INPUT_DIR, 'downloaded')
SAMPLE_DIR = os.path.join(INPUT_DIR, 'sampled')
os.makedirs(SAMPLE_DIR, exist_ok = True)

SAMPLE_NUM = 100000

def dealKeyword(rawStr: str):
    rawStr = re.sub(r'since:\w+', '', rawStr)
    rawStr = re.sub(r'until:\w+', '', rawStr)
    return rawStr.strip()

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

def yieldLines(rootPath: str, fileTypes: Set[str] = set()):
    for filePath in yieldFiles(rootPath, fileTypes):
        with open(filePath, 'r') as file:
            for line in file:
                yield line

with open(INFO_TXT_PATH, 'r') as file:
    INFO_LINES = list(file)[1: ]

def getLineInfo(line: str):
    infoParts = re.match(r'"([^"]+)": count = ([0-9]+)', line)
    keyword = infoParts.group(1)
    count = int(infoParts.group(2))
    return keyword, count

def main():
    infos = list(map(getLineInfo, INFO_LINES[: 100]))
    files = {keyword: open(os.path.join(SAMPLE_DIR, f'{keyword}.jsonl'), 'w') for keyword, _ in infos}
    counts = {keyword: count for keyword, count in infos}
    for line in tqdm(yieldLines(DOWNLOAD_DIR, {'.jsonl'})):
        obj = json.loads(line)
        keyword = dealKeyword(obj.get('keyword', ''))
        if keyword in files:
            if np.random.uniform(0, 1) < SAMPLE_NUM / counts[keyword]:
                files[keyword].write(line)
    for writer in files.values():
        writer.close()

if __name__ == '__main__':
    main()
