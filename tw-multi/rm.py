import os

from tqdm import tqdm
from argparse import ArgumentParser

def getArgs():
    parser = ArgumentParser()
    parser.add_argument('-i', type = str, default = './', help = '需要从中删除文件的文件夹 (默认为当前目录)')
    parser.add_argument('-t', type = str, required = True, help = '需要删除的文件后缀名，多个后缀名以逗号分隔')
    return parser.parse_args()

ARGS = getArgs()
fileTypes = set(ARGS.t.split(','))

def main():
    for root, _, files in tqdm(os.walk(ARGS.i, followlinks = False)):
        for fileName in filter(lambda name: any(name.endswith(fileType) for fileType in fileTypes), files):
            filePath = os.path.join(root, fileName)
            os.system(f'rm "{filePath}"')

if __name__ == '__main__':
    print(f'args = {ARGS}')
    main()
