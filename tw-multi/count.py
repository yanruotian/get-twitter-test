import os
import re
import json
import datetime

SCRAPED_DIRS = [
    '/root/get-twitter-test/tw-multi/splits',
]

def getLogKeywords(paths: list[str]):
    results: set[str] = set()
    for path in paths:
        if os.path.isfile(path) and path.endswith('tw.log'):
            with open(path, 'r') as file:
                for line in file:
                    reResult = re.search(r'scraping end, keyword = "([^"]+)"', line)
                    if reResult is not None:
                        results.add(reResult.group(1))
        elif os.path.isdir(path):
            for fileName in os.listdir(path):
                filePath = os.path.join(path, fileName)
                results.update(getLogKeywords([filePath]))
        else:
            pass
    return results

keywordCount = len(getLogKeywords(SCRAPED_DIRS))
try:
    f = open('/root/get-twitter-test/tw-multi/count.txt', 'r')
    last_line = f.readlines()[-1]
    last_time = last_line.split(',')[0].replace('time: ', '')
    last_keywordCount = int(last_line.split(',')[1].split(':')[1].strip())

    totalKeywords = 1515923
    etc_time = (datetime.datetime.now() - datetime.datetime.strptime(last_time, "%Y-%m-%d %H:%M:%S")).total_seconds() / (keywordCount - last_keywordCount) / 60 / 60 / 24 * (totalKeywords - keywordCount)
    f.close()

    f = open('/root/get-twitter-test/tw-multi/count.txt', 'a')
    f.write(f"time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, keywordCount: {keywordCount}, etc_time: {etc_time: .2f} days. \n")
    f.close()
except Exception as e:
    print(e)

