'''
将爬取中条目数多于预设的的关键词语料进行随机抽样
'''

import os
import re
import json

from tqdm import tqdm
from typing import Any, Set, Dict, List, Callable

DIR_PATH = '/root/get-twitter-test/downloaded-pooled-tec'
SAMPLE_PATH = os.path.join(DIR_PATH, 'too-much-new')
os.makedirs(SAMPLE_PATH, exist_ok = True)


class LogFileReader:

    def __init__(self, path: str, dealer: Callable[['LogFileReader', str], None]):
        self.logFilePath = path
        self.jsonFilePaths: List[str] = []
        self.dealer = dealer
        self.file = None
        self.open()

    def __enter__(self):
        return self

    def __exit__(self, *_a, **_w):
        self.close()

    def startRead(self):
        for line in tqdm(self.file, 'log file'):
            line = line.strip()
            self.dealer(self, line)
            openRe = re.search(r'opening file (.+) for write', line)
            if openRe is None:
                self.jsonFilePaths = self.jsonFilePaths[-1 : ]
            else:
                self.jsonFilePaths.append(openRe.group(1).strip())

    def open(self):
        if self.file is not None:
            self.close()
        self.file = open(self.logFilePath, 'r')

    def close(self):
        if self.file is not None:
            self.file.close()
        self.file = None


class Dealer:

    def __init__(self, outputDir: str, sampleNum: int = 20000):
        self.outputDir = outputDir
        self.sampleNum = sampleNum
        self.recordKeyword: str = ''
        self.sampledSet: Set[str] = set()

    def __call__(self, reader: LogFileReader, line: str):
        tooMuchRe = re.search(r'\[too much data\] keyword "(.+?)" .*until = ([0-9]+-[0-9]+-[0-9]+) .*since = ([0-9]+-[0-9]+-[0-9]+) ', line)
        if tooMuchRe is not None:
            keyword = tooMuchRe.group(1) + '@' + tooMuchRe.group(2) + '@' + tooMuchRe.group(3)
            if keyword not in self.sampledSet:
                self.recordKeyword = keyword
        keywordRe = re.search(r'scraping end, keyword = "(.+?)",', line)
        if keywordRe is not None:
            keyword = keywordRe.group(1)
            if keyword == self.recordKeyword.split('@')[0]:
                count = 0
                breakFlag = False
                with open(os.path.join(self.outputDir, f'{self.recordKeyword}.jsonl'), 'w+') as file:
                    for jsonFilePath in reader.jsonFilePaths:
                        with open(jsonFilePath, 'r') as jsonFile:
                            for line in tqdm(jsonFile, jsonFilePath):
                                line = line.strip()
                                obj: Dict[str, Any] = json.loads(line)
                                if obj.get('keyword', None) == keyword:
                                    file.write(line + '\n')
                                    count += 1
                                    if count >= self.sampleNum:
                                        breakFlag = True
                                if breakFlag:
                                    break
                        if breakFlag:
                            break
                self.sampledSet.add(keyword)
                self.recordKeyword = ''
                print(f'keyword "{keyword}" sample finished')


def main():
    for fileName in os.listdir(DIR_PATH):
        filePath = os.path.join(DIR_PATH, fileName)
        if os.path.isfile(filePath) and fileName[-4 : ] == '.log':
            with LogFileReader(filePath, Dealer(SAMPLE_PATH, 20000)) as reader:
                reader.startRead()

if __name__ == '__main__':
    main()
