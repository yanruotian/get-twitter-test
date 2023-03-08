import os
import json

from tqdm import tqdm
from zhconv import convert
from typing import Set, Dict, List

FILE_DIR = os.path.dirname(os.path.abspath(__file__))

def getJsonFile(path: str):
    result = set()
    with open(path, 'r') as file:
        content: Dict[str, List[str]] = json.load(file)
    for keywordList in content.values():
        result |= set(keywordList)
    return result

def getKeywords(dirPath: str) -> Set[str]:
    result = set()
    for fileName in os.listdir(dirPath):
        filePath = os.path.join(dirPath, fileName)
        if os.path.isfile(filePath) and fileName[-5 : ] == '.json':
            result |= getJsonFile(filePath)
    dealedResult = set()
    for keyword in tqdm(result):
        flag = True
        for _keyword in result:
            dealedKeyword = convert(keyword.lower(), 'zh-cn')
            _dealedKeyword = convert(_keyword.lower(), 'zh-cn')
            if (_dealedKeyword in dealedKeyword) and (dealedKeyword != _dealedKeyword):
                flag = False
                break
        if flag:
            dealedResult.add(convert(keyword, 'zh-cn'))
            dealedResult.add(convert(keyword, 'zh-tw'))
        else:
            print(f'abandoned keyword "{keyword}" (with _dealedKeyword = "{_dealedKeyword}")')
    return dealedResult

def main():
    keywords = getKeywords(FILE_DIR)
    def _iter():
        for keyword in keywords:
            yield keyword + '\n'
    with open(os.path.join(FILE_DIR, 'unreached.txt'), 'w+') as file:
        file.writelines(_iter())
    
if __name__ == '__main__':
    main()
