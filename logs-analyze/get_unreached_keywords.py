import os
import re

def get_one_file(file_path: str):
    reached = set()
    keys = None
    last_keyword = None
    with open(file_path, 'r') as file:
        contents = file.readlines()
    for line in contents:
        line = line.strip()
        keyword = re.search(r'begin scraping keyword "(.+?)"', line)
        if keyword is not None:
            keyword = keyword.group(1)
            reached.add(keyword)
            last_keyword = keyword
        elif keys is None:
            _keys = re.search(r'keys = (.*)', line)
            if _keys is not None:
                keys = set(eval(_keys.group(1)))
        elif 'scraping end, item count = ' in line:
            last_keyword = None
    reached = reached - {last_keyword}
    if keys is None:
        print(f'err: keys is None in file {file_path}')
        exit()
    return keys - reached

def main():
    DIR = os.path.dirname(os.path.abspath(__file__))
    unreached = set()
    for log_file in os.listdir(DIR):
        log_path = os.path.join(DIR, log_file)
        if log_file[-4 : ] == '.log' and os.path.isfile(log_path):
            print(f'dealing file {log_file}')
            unreached = unreached | get_one_file(log_path)
    with open('unreached.txt', 'w+') as file:
        file.writelines({f'{keyword}\n' for keyword in unreached})

if __name__ == '__main__':
    main()
