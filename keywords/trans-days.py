import os
import json
import datetime

from tqdm import tqdm 
from typing import Dict

INPUT_DIR = 'china'
OUTPUT_FILE = os.path.join(INPUT_DIR, 'days.keywords')

KEYWORDS_DICT_PATH = '/root/get-twitter-test/downloaded/china-tec-new-2023-05-12/keyword-distribution.json'
KEYWORDS_DICT_PATH = None
if KEYWORDS_DICT_PATH is not None:
    with open(KEYWORDS_DICT_PATH, 'r') as file:
        KEYWORDS_DICT: Dict[str, Dict[str, int]] = json.load(file)
else:
    KEYWORDS_DICT = dict()

def yieldLines(path: str, fileTypes = set()):
    for root, _, files in os.walk(path):
        for fileName in files:
            if (
                fileName != os.path.basename(OUTPUT_FILE) and (
                    len(fileTypes) == 0 or 
                    any(fileName.endswith(fileType) for fileType in fileTypes)
                )
            ):
                with open(os.path.join(root, fileName), 'r') as file:
                    for line in file:
                        yield line

def main():
    with open(OUTPUT_FILE, 'w') as file:
        for line in tqdm(yieldLines(INPUT_DIR, {'.txt'})):
            line = line.strip()
            if not ('since:' in line or 'until:' in line):
                since = datetime.datetime(2010, 1, 1)
                until = datetime.datetime(2023, 1, 1)
                dateDict = KEYWORDS_DICT.get(line, dict())
                while since < until:
                    date = since.strftime(r"%Y-%m-%d")
                    if not dateDict.get(date, 0) > 0:
                        file.write(
                            f'{line} since:{since.strftime(r"%Y-%m-%d")}'
                            f' until:{(since + datetime.timedelta(days = 1)).strftime(r"%Y-%m-%d")}\n'
                        )
                    since += datetime.timedelta(days = 1)

if __name__ == '__main__':
    main()
