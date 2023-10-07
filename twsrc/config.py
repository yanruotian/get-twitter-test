'''
对log文件的配置在__init__.py。
'''

import os
import string

from .log import info
from .args import ARGS

def getProxies(filePath: str | None):
    if not filePath or not os.path.isfile(filePath):
        return None
    with open(filePath, 'r') as file:
        proxies = [line.strip() for line in file]
    return proxies

# PROXY = 'http://yanruotian:123456@dc.visitxiangtan.com:10000'
PROXIES: list[str] | None = getProxies(ARGS.proxies)
ACCOUNT_ID: int | None = ARGS.account_id
ACCOUNTS_PATH: str = ARGS.accounts or os.path.join(os.path.dirname(os.path.abspath(__file__)), 'accounts.txt')
KEYWORDS_PATH: str = ARGS.keywords or '/root/get-twitter-test/keywords/china-tec-new/keywords.renewed'
OUTPUT_DIR: str = ARGS.output or '/root/get-twitter-test/downloaded/china-tec-2023-07-15/downloaded'

# info('config: ' + str({
#     key: value for key, value in globals().items() if (
#         all(char in string.ascii_uppercase + '_' for char in key)
#     )
# }))
