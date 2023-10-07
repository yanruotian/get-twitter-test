'''
这个脚本是将指定文件夹的特定类型文件都复制到另一文件夹。
'''

import os

from argparse import ArgumentParser

def getArgs():
    parser = ArgumentParser()
    parser.add_argument(
        '-i', type = str, required = True, 
        help = '输入文件夹',
    )
    parser.add_argument(
        '-o', type = str, required = True, 
        help = '输出文件夹',
    )
    parser.add_argument(
        '-t', type = str, default = '',
        help = '复制的文件类型，用逗号分隔（默认为空，则所有文件都复制）',
    )
    return parser.parse_args()

ARGS = getArgs()
FILE_TYPES = set(ARGS.t.split(','))
os.makedirs(ARGS.o, exist_ok = True)

def cp(relPath: str):
    absIn = os.path.join(ARGS.i, relPath)
    absOut = os.path.join(ARGS.o, relPath)
    if os.path.isdir(absIn):
        for name in os.listdir(absIn):
            cp(os.path.join(relPath, name))
    elif os.path.isfile(absIn) and (
        len(FILE_TYPES) == 0 or
        any(absIn.endswith(fileType) for fileType in FILE_TYPES)
    ):
        os.makedirs(os.path.dirname(absOut), exist_ok = True)
        os.system(f'cp "{absIn}" "{absOut}"')

if __name__ == '__main__':
    cp('')

