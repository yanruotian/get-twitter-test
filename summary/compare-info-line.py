import os
import json
import operator

from functools import reduce

INFO_LINE_PATHS = ('/root/get-twitter-test/summary/line-info.json', '/root/get-twitter-test/downloaded/china-tec-new-2023-05-12/line-info.json')

def main():
    infoDicts = dict()
    for path in INFO_LINE_PATHS:
        with open(path, 'r') as file:
            infoDicts[path] = json.load(file)
    for key in reduce(operator.or_, (set(map(os.path.basename, value.keys())) for value in infoDicts.values()), set()):
        values = set(filter(lambda value: True, (value.get(key, None) for value in infoDicts.values())))
        if len(values) >= 2:
            print(f'file name = "{key}"')
            for path in INFO_LINE_PATHS:
                print(f'    - "{path}": {infoDicts.get(path).get(key, None)}')

if __name__ == '__main__':
    main()
