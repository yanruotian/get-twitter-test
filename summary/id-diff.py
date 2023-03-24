'''
对两个jsonl结果文件夹的数据进行差异分析。

得到INPUT_DIR_1的数据对INPUT_DIR_2的数据的差集。
'''

import os
import json

from tqdm import tqdm
from redis import StrictRedis

INPUT_DIR_2 = '/root/get-twitter-test/downloaded-20230319-new/downloaded'
INPUT_DIR_1 = '/root/get-twitter-test/downloaded-20230319-new-pooled/downloaded'

idServer = StrictRedis('localhost', 9000, 0)

def getId(line: str):
    try:
        return int(json.loads(line).get('id'))
    except Exception as e:
        print(f'no id in line "{line}"')
        print(f'    exception = {e}')
        return 0
    
def load(path: str):
    global idServer
    if os.path.isfile(path) and path[-6 : ] == '.jsonl':
        with open(path, 'r') as file:
            for line in tqdm(file, path):
                idServer.set(getId(line), 1)
    elif os.path.isdir(path):
        for fileName in os.listdir(path):
            load(os.path.join(path, fileName))

def judge(path: str):
    global idServer
    if os.path.isfile(path) and path[-6 : ] == '.jsonl':
        with open(path, 'r') as file:
            for line in tqdm(file, path):
                id = getId(line)
                if idServer.get(id) is None:
                    idServer.set(id, 1)
                    yield id
    elif os.path.isdir(path):
        for fileName in os.listdir(path):
            for id in judge(os.path.join(path, fileName)):
                yield int(id)

def main():
    load(INPUT_DIR_1)
    with open('./id-diff-result.txt', 'w+') as file:
        for id in judge(INPUT_DIR_2):
            file.write(f'{id}\n')

if __name__ == '__main__':
    main()
