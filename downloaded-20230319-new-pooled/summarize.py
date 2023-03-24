'''
收集各关键词在各月份的数据量分布
'''

import os
import json

from tqdm import tqdm
from collections import defaultdict

INPUT_DIR = './downloaded'
OUTPUT_DIR = './summary'
os.makedirs(OUTPUT_DIR, exist_ok = True)

def oneFile(path: str, resultDict):
    with open(path, 'r') as file:
        for line in tqdm(file, path):
            try:
                obj = json.loads(line)
                keyword = str(obj['keyword'])
                date = str(obj['date'])
            except Exception as e:
                print(f'exception in file "{path}"')
                print(f'    line = "{line}"')
                print(f'    e = {e}')
                continue
            year, month = date.split('-')[ : 2]
            resultDict[keyword][f'{int(year) :4d}-{int(month) :02d}'] += 1

def oneProcess():
    resultDict = defaultdict(lambda: defaultdict(lambda: 0))
    for fileName in tqdm(os.listdir(INPUT_DIR)):
        filePath = os.path.join(INPUT_DIR, fileName)
        if os.path.isfile(filePath) and fileName[-6 : ] == '.jsonl':
            oneFile(filePath, resultDict)
    with open(os.path.join(OUTPUT_DIR, 'result.json'), 'w+') as file:
        json.dump(resultDict, file, ensure_ascii = False)

if __name__ == '__main__':
    oneProcess()
