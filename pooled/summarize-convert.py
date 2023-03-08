'''
“繁->简”“简->繁”之后，是每一个名称/别名都有繁和简两个版本吗？可以整理一下吗？
保存成一个类似图中的形式，其中：字典的键为我们给你的名称/别名，字典的值为“繁->简”“简->繁”后的字典（包含简体、繁体）

{
    "清华大学": {"简体": "清华大学", "繁体": "清華大學"}
}
'''

import os
import json
import zhconv

from tqdm import tqdm

FILE_DIR = os.path.dirname(os.path.abspath(__file__))
TXT_PATH = os.path.join(FILE_DIR, 'unreached.txt')

def getJsonDir(dirPath: str = FILE_DIR):
    result = set()
    for fileName in os.listdir(dirPath):
        filePath = os.path.join(dirPath, fileName)
        if os.path.isfile(filePath) and fileName[-5 : ] == '.json':
            result |= getJsonFile(filePath)
    return result

def getJsonFile(filePath: str):
    result = set()
    with open(filePath, 'r') as file:
        obj = json.load(file)
        for keywords in obj.values():
            result |= set(keywords)
    return result

def getTxtFile(filePath: str = TXT_PATH):
    result = set()
    with open(filePath, 'r') as file:
        for line in file:
            result.add(line.strip())
    return result

def main():
    txtResult = getTxtFile()
    initialKeywords = getJsonDir()
    result = dict()
    for initialKeyword in tqdm(initialKeywords):
        simple = zhconv.convert(initialKeyword, 'zh-cn')
        tradition = zhconv.convert(initialKeyword, 'zh-tw')
        if simple in txtResult and tradition in txtResult:
            result[initialKeyword] = {
                '简体': simple,
                '繁体': tradition,
            }
    with open(os.path.join(FILE_DIR, 'result'), 'w+') as file:
        json.dump(result, file, ensure_ascii = False)

if __name__ == '__main__':
    main()
    