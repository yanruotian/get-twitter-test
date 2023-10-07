'''
`twsrc`模块能接受的参数：

--accounts FILE_PATH: (default = <twsrc-path>/accounts.txt)
    指定读取的账号信息文件的路径。该文件应该每行包含一条账号信息，使用`----`分隔，依次是账号用户名、账号密码、账号邮箱、账号邮箱密码、`auth_token`。

--account-id ID: (default = None)
    可以通过这个参数指定仅使用账号信息文件的某个特定账号进行爬取。

--proxies FILE_PATH: (default = None)
    如果需要使用代理，则指定包含所有可用代理地址的文件路径。
    
--keywords FILE_PATH: (default = <keywords-path>)
    指定读取的关键词列表文件的路径。该文件应该每行包含一个关键词。

--output DIR_PATH: (default = <output-dir>)
    指定下载到的内容存储的文件夹。

此外，还能设置以下环境变量：

LOG_FILE: (default = tw.log)
    指定`logging`模块的日志文件的路径。由于在`__init__.py`中完成，故采用环境变量的方式进行设置。
'''

from argparse import ArgumentParser

def getArgs():
    parser = ArgumentParser()
    parser.add_argument('--proxies', type = str, default = None)
    parser.add_argument('--account-id', type = int, default = None)  # 仅用于单账号爬取模式
    parser.add_argument('--accounts', type = str, default = None)
    parser.add_argument('--keywords', type = str, default = None)
    parser.add_argument('--output', type = str, default = None)
    return parser.parse_args()

ARGS = getArgs()
