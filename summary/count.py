import os
import json
import operator

from typing import Set, Dict
from functools import reduce

INPUT_DIR = '/root/get-twitter-test/downloaded/china-tec-new-2023-05-12'
INPUT_DIR = '/root/get-twitter-test/downloaded/china-2023-05-26'
INFO_JSON_PATH = os.path.join(INPUT_DIR, 'keyword-distribution.json')
RESULT_PATH = os.path.join(INPUT_DIR, 'keyword-counts.txt')

with open(INFO_JSON_PATH, 'r') as file:
    INFO_DICT: Dict[str, Dict[str, int]] = json.load(file)

def summaryDateCount(dates: Set[str]):
    months = set(map(lambda date: date[: len('xxxx-xx')], dates))
    def _oneMonth(month: str):
        days = {int(date[-len('xx'): ]) for date in dates if date.startswith(month)}
        return max(max(days | {0}) - min(days | {50}) + 1, 0)
    return sum(map(_oneMonth, months))

def summaryKeyword(keyword: str, targetMonths: Set[str]):
    dateDict: Dict[str, int] = INFO_DICT[keyword]
    targetTotalDay = len(targetMonths) * 30
    collectedTotalDay = summaryDateCount(dateDict.keys())
    totalCount = sum(dateDict.values())
    if totalCount <= 1000:
        collectedTotalDay = targetTotalDay
    outputStr = (
        f'"{keyword}": count = {totalCount}, day = {collectedTotalDay} '
        f'({collectedTotalDay / targetTotalDay * 100 :.2f}%), '
        f'target = {int(totalCount / collectedTotalDay * targetTotalDay)}'
    )
    return (outputStr, {
        'target': int(totalCount / collectedTotalDay * targetTotalDay),
        'collected': totalCount,
    })

def main():
    targetMonths: Set[str] = reduce(operator.or_, (set(map(
        lambda dateStr: dateStr[: len('xxxx-xx')], dateDict.keys()
    )) for dateDict in INFO_DICT.values()), set())
    keywordResults = sorted(
        (summaryKeyword(keyword, targetMonths) for keyword in INFO_DICT.keys()),
        key = lambda result: -(result[-1].get('target') - result[-1].get('collected')),
    )
    with open(RESULT_PATH, 'w') as file:
        totalCount = sum(infoDict.get("collected") for _, infoDict in keywordResults)
        targetCount = sum(infoDict.get("target") for _, infoDict in keywordResults)
        file.write(
            f'total: count = {totalCount}, target = {targetCount}, '
            f'precentage = {totalCount / targetCount * 100 :.2f}%\n'
        )
        for resultStr, _ in keywordResults:
            file.write(resultStr + '\n')

if __name__ == '__main__':
    main()
