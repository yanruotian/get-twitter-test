import os
import re
import json

from tqdm import tqdm
from typing import Dict, List
from argparse import Namespace

def transform(args: Namespace) -> None:
    load_path: str = args.load_path
    output_path: str = args.output_path
    os.makedirs(output_path, exist_ok = True)

    instance_labels: Dict[str, List[str]] = dict()
    args.logger.logln(f'building instance label dict...')
    f_label = open(os.path.join(load_path, 'instance-label.ttl'), 'r')
    for line in f_label:
        line = line.strip()
        parts = line.split(' ')
        if len(parts) >= 3:
            wd = parts[0]
            if wd[ : 3] != 'wd:':
                continue
            wd = wd[3 : ]
            type = parts[1]
            content = ' '.join(parts[2 : ])
            content = re.sub(r'@[^@"]+?$', '', content)
            try:
                content = json.loads(content)
            except: 
                args.logger.logln(f'! json error in line: {parts} (content = {content})')
                continue
            if 'label' in type.lower():
                if instance_labels.get(wd, None) is None:
                    instance_labels[wd] = []
                instance_labels[wd].append((type, content))
    f_label.close()
    
    for file_name in os.listdir(load_path):
        if file_name[-4 : ] == '.txt':
            f_in = open(os.path.join(load_path, file_name), 'r')
            f_out = open(os.path.join(output_path, f'{file_name[ : -4]}-transformed.txt'), 'w+')
            args.logger.logln(f'begin dealing file: {file_name}')
            for line in tqdm(f_in):
                line = line.strip()
                possible_contents = instance_labels.get(line, None)
                if possible_contents is not None:
                    for _, content in possible_contents:
                        f_out.write(f'{content}\n')
            f_in.close()
            f_out.close()
