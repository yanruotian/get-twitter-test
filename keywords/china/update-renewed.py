import os
import re
import json

from tqdm import tqdm

TOTAL_KEYWORDS_FILE = 'days.keywords'
SCRAPED_DIRS = [
    '/root/get-twitter-test/tw-multi-china/splits',
]
JSON_FILE = 'keywords-detailed.json'
OUTPUT_FILE = 'keywords1'

with open(TOTAL_KEYWORDS_FILE, 'r') as file:
    KEYWORDS = {line.strip() for line in file}

# with open(JSON_FILE, 'r') as file:
#     JSON_KEYWORDS = set(json.load(file).keys())

def getLogKeywords(paths: list[str]):
    results: set[str] = set()
    for path in paths:
        if os.path.isfile(path) and path.endswith('tw.log'):
            print(f'path "{path}" is log file')
            with open(path, 'r') as file:
                for line in tqdm(file, path):
                    reResult = re.search(r'scraping end, keyword = "([^"]+)"', line)
                    if reResult is not None:
                        results.add(reResult.group(1))
        elif os.path.isdir(path):
            # print(f'path "{path}" is dir')
            for fileName in os.listdir(path):
                filePath = os.path.join(path, fileName)
                results.update(getLogKeywords([filePath]))
        else:
            pass
            # print(f' path "{path}" skipped')
    return results

with open(OUTPUT_FILE, 'w') as file:
    for keyword in KEYWORDS - (logKeywords := getLogKeywords(SCRAPED_DIRS)):
    # for keyword in KEYWORDS - JSON_KEYWORDS:
        file.write(keyword + '\n')
    print('log keywords count = ', len(logKeywords))
