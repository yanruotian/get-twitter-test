import os
import json

from tqdm import tqdm
from typing import Dict, List
from argparse import Namespace

def transform(args: Namespace) -> None:
    
    load_path: str = args.load_path
    output_path: str = args.output_path
    os.makedirs(output_path, exist_ok = True)

    for file_name in os.listdir(load_path):
        if file_name[-5 : ] == '.json':
            f_in = open(os.path.join(load_path, file_name), 'r')
            f_out = open(os.path.join(output_path, f'{file_name[ : -5]}-transformed.txt'), 'w+')
            args.logger.logln(f'begin dealing file: {file_name}')
            json_dict: Dict[str, List[str]] = json.loads(f_in.read())
            for key_list in tqdm(json_dict.values()):
                for key in key_list:
                    key = key.strip()
                    f_out.write(f'{key}\n')
            f_in.close()
            f_out.close()
