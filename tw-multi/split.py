import os

from tqdm import tqdm
from argparse import ArgumentParser

def getArgs():
    parser = ArgumentParser()
    parser.add_argument('-i', type = str, required = True, help = '输入文件')
    parser.add_argument('-o', type = str, required = True, help = '输出文件夹')
    parser.add_argument('-n', type = int, required = True, help = '均分数量')
    return parser.parse_args()

ARGS = getArgs()

def yieldLine():
    with open(ARGS.i, 'r') as file:
        for line in file:
            if len(_line := line.strip()) > 0:
                yield _line

def main():
    totalCount = sum(1 for _ in yieldLine())
    splitLen = totalCount // ARGS.n
    for count, line in tqdm(enumerate(yieldLine()), total = totalCount):
        i = count // splitLen
        outputPath = os.path.join(ARGS.o, f'split-{i :02d}', os.path.basename(ARGS.i))
        os.makedirs(os.path.dirname(outputPath), exist_ok = True)
        with open(outputPath, 'a') as file:
            file.write(line + '\n')

if __name__ == '__main__':
    main()
    