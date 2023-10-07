import os
import re
import json

# TOTAL_KEYWORDS_FILE = 'keywords.renewed'
TOTAL_KEYWORDS_FILE = 'tw-keywords6'
SCRAPED_DIRS = [
    # '/root/get-twitter-test/accounts-10-output',
    # '/root/get-twitter-test/accounts-40-output',
    # '/root/get-twitter-test/tw-40.log',
    # '/root/get-twitter-test/tw-test.log',
    # '/root/get-twitter-test/tw.log',
    # '/root/get-twitter-test/multi-log',
    # '/root/get-twitter-test/100-accounts-log',
    '/root/get-twitter-test/tw-multi/splits',
]
JSON_FILE = 'wx-keywords-detailed.json'
# OUTPUT_FILE = 'tw-keywords'
OUTPUT_FILE = 'tw-keywords6-10'

with open(TOTAL_KEYWORDS_FILE, 'r') as file:
    KEYWORDS = {line.strip() for line in file}

with open(JSON_FILE, 'r') as file:
    JSON_KEYWORDS = set(json.load(file).keys())

def getLogKeywords(paths: list[str]):
    results: set[str] = set()
    for path in paths:
        if os.path.isfile(path) and path.endswith('tw.log'):
            print(f'path "{path}" is log file')
            with open(path, 'r') as file:
                for line in file:
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
