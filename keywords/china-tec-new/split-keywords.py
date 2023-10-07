'''
将关键词均分为若干部分，以其名字编号存储在一个文件夹中。
'''

import os

KEYWORDS_PATH = 'tw-keywords'
OUTPUT_DIR = 'keywords-splited'
SPLIT_NUM = 80
os.makedirs(OUTPUT_DIR, exist_ok = True)

def yieldLine(path: str):
    with open(path, 'r') as file:
        for line in file:
            yield line

def main():
    totalCount = sum(1 for _ in yieldLine(KEYWORDS_PATH))
    splitCount = totalCount // SPLIT_NUM + 1
    fOut = None
    fIndex = 0
    fCount = 0
    for line in yieldLine(KEYWORDS_PATH):
        if fOut is None:
            fOut = open(os.path.join(OUTPUT_DIR, f'{fIndex}.txt'), 'w')
            fCount = 0
        fOut.write(line)
        fCount += 1
        if fCount >= splitCount:
            fOut.close()
            fOut = None
            fIndex += 1
            fCount = 0

if __name__ == '__main__':
    main()
    