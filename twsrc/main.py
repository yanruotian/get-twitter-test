import os
import json
import time
import asyncio
import datetime

from twscrape import AccountsPool, API

from .log import info
from .config import (
    PROXIES, ACCOUNTS_PATH, KEYWORDS_PATH,
    OUTPUT_DIR, ACCOUNT_ID
)
from .writer import Writer

def getAccounts(path: str = ACCOUNTS_PATH):
    if not os.path.isfile(path):
        print(f'no account file ("{path}")')
        return
    with open(path, 'r') as file:
        for line in file:
            line = line.strip()
            yield line.split('----')[: 4]  # [用户名, 用户密码, 邮箱地址, 邮箱密码]

def getKeywords(keywordsPath: str = KEYWORDS_PATH):
    with open(keywordsPath, 'r') as file:
        for line in file:
            yield line.strip()


async def main():

    # 获得twscrape相关工具实例
    accountsPool = AccountsPool()
    api = API(accountsPool)

    # 如果有需要新注册的账号，则进行注册
    if (accountsCount := sum(1 for _ in getAccounts())):
        proxiesCount = len(PROXIES) if isinstance(PROXIES, list) else 0
        print(f'totally {accountsCount} accounts, {proxiesCount} proxies')
        for id, account in enumerate(getAccounts()):
            if ACCOUNT_ID is None or ACCOUNT_ID == id:
                proxy = PROXIES[id % proxiesCount] if proxiesCount else None
                await api.pool.add_account(
                    *(account[: 4]),
                    user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_3; nb-no) AppleWebKit/525.18 (KHTML, like Gecko) Version/3.1.1 Safari/525.20',
                    # cookies = '{"auth_token": "%s", "ct0": "2ca31b5ac2693002520fb065db2a5aa8882749f7a8a505872c3eb57ac08a037de17e730b0a3d8b28a51e496c6b8e12609f8754223df80ebf2c0c64793c327cc56160e2c029e058d07a2de33cabd5a4e3"}' % account[4],
                    proxy = proxy,
                )
        await accountsPool.login_all()

    keywordNum = sum(1 for _ in getKeywords())
    print(f'totally {keywordNum} keywords')
    startTime = time.time()
    tweetCountTotal = 0
    with Writer(OUTPUT_DIR) as writer:
        for i, keyword in enumerate(getKeywords(), start = 1):
            tweetCount = 0
            epsTime = time.time()
            info(f'starting download for keyword "{keyword}"')
            async for tweet in api.search(keyword):
                tweetDict = json.loads(tweet.json())
                tweetDict['keyword'] = keyword
                writer.writeLine(json.dumps(tweetDict, ensure_ascii = False) + '\n')
                tweetCount += 1
            tweetCountTotal += tweetCount
            endTime = time.time()
            epsTime = endTime - epsTime
            totalSeconds = endTime - startTime
            meanSeconds = totalSeconds / i
            meanTweetCount = tweetCountTotal / i
            info(
                f'scraping end, keyword = "{keyword}", count = {tweetCount} '
                f'({i} / {keywordNum} = {i / keywordNum * 100 :.2f}%), '
                f'time = {epsTime :.2f}s, '
                f'total time = {datetime.timedelta(seconds = int(totalSeconds))}, '
                f'average time = {meanSeconds :.2f}s, '
                f'average data = {meanTweetCount :.2f}'
            )

if __name__ == '__main__':
    asyncio.run(main())
