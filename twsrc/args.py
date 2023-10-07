'''
`twsrc`模块能接受的参数：

--accounts FILE_PATH: (default = <twsrc-path>/accounts.txt)
    指定读取的新增账号信息文件的路径。该文件应该每行包含一条账号信息，使用`----`分隔，依次是账号用户名、账号密码、账号邮箱、账号邮箱密码。

--account-id ID: (default = None)
    （已弃用）可以通过这个参数指定仅使用账号信息文件的某个特定账号进行爬取。

--proxies FILE_PATH: (default = None)
    如果需要使用代理，则指定包含所有可用代理地址的文件路径。
    
--keywords FILE_PATH: (required)
    指定读取的关键词列表文件的路径。该文件应该每行包含一个关键词。

--output DIR_PATH: (default = "downloads")
    指定下载到的内容存储的文件夹。

此外，还能设置以下环境变量：

LOG_FILE: (default = tw.log)
    指定`logging`模块的日志文件的路径。由于在`__init__.py`中完成，故采用环境变量的方式进行设置。
'''

from argparse import ArgumentParser, RawTextHelpFormatter

def getArgs():
    parser = ArgumentParser(formatter_class = RawTextHelpFormatter)
    parser.add_argument(
        '--keywords', type = str, required = True,
        help = '指定读取的关键词列表文件的路径。该文件应该每行包含一个关键词（包含since、until等筛选控制信息）。'
    )
    parser.add_argument(
        '--accounts', type = str, default = None,
        help = (
            '[可选，默认<twsrc-path>/accounts] 指定读取的新增账号信息文件的路径。\n'
            '该文件应该每行包含一条账号信息，使用----分隔，依次是账号用户名、账号密码、账号邮箱、账号邮箱密码。'
            '\n**注意**：如果账号信息已经注入爬取目录下的accounts.db，无需使用此选项。'
        )
    )
    parser.add_argument(
        '--proxies', type = str, default = None,
        help = '[可选] 如果需要使用代理，则指定包含所有可用代理地址的文件路径。'
    )
    parser.add_argument(
        '--account-id', type = int, default = None,
        help = '[已弃用] 可以通过这个参数指定仅使用账号信息文件的某个特定账号进行爬取。'
    )  # 仅用于单账号爬取模式
    parser.add_argument(
        '--output', type = str, default = "downloads",
        help = '[可选，默认downloads] 指定下载到的内容存储的文件夹。'
    )
    return parser.parse_args()

ARGS = getArgs()
