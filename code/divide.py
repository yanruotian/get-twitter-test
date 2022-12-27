import os
import random

from tqdm import tqdm
from typing import Set
from argparse import Namespace

def divide(args: Namespace) -> None:

    load_path: str = args.load_path
    output_path: str = args.output_path
    os.makedirs(output_path, exist_ok = True)

    contents: Set[str] = set()
    args.logger.logln(f'gathering contents...')
    for file_name in tqdm(os.listdir(load_path)):
        if file_name[-4 : ] == '.txt':
            with open(os.path.join(load_path, file_name), 'r') as f_in:
                contents = contents | {line.strip() for line in f_in}

    content_count = len(contents)
    args.logger.logln(f'content count = {content_count}, n = {args.n}')
    num_pre_process = (content_count + 1) // args.n

    args.logger.logln(f'creating process txts...')
    contents = list(contents)
    random.shuffle(contents)
    for process_num in tqdm(range(args.n)):
        process_contents = contents[num_pre_process * process_num : num_pre_process * (process_num + 1)]
        f_out = open(os.path.join(output_path, f'{process_num :2d}.txt'.replace(' ', '0')), 'w+')
        for content in process_contents:
            f_out.write(content.strip() + '\n')
        f_out.close()
