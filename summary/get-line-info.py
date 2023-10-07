'''
统计一个文件夹下所有的文件名和对应文件的行数，保存到一个json文件中。
'''

import os
import json

from tqdm import tqdm
from collections import defaultdict

INPUT_DIR = '/root/get-twitter-test/downloaded/china-tec-new-2023-05-12'
OUTPUT_FILE_PATH = os.path.join(INPUT_DIR, 'line-info.json')

def main(fileTypes = {'.jsonl'}):
    infoDict = defaultdict(int)
    for root, _, files in os.walk(INPUT_DIR):
        for fileName in filter(lambda fileName: (
            len(fileTypes) == 0 or 
            any(fileName.endswith(fileType) for fileType in fileTypes)
        ), files):
            filePath = os.path.join(INPUT_DIR, root, fileName)
            with open(filePath, 'r') as file:
                infoDict[os.path.join(root, fileName)] += sum(map(lambda _: 1, tqdm(file, filePath)))
    with open(OUTPUT_FILE_PATH, 'w') as file:
        json.dump(infoDict, file, ensure_ascii = False)

if __name__ == '__main__':
    main()
