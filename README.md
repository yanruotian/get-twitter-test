# 推特数据爬取

## 环境安装

- 为避免`python`版本不一致导致的不兼容问题，建议在`python3.10`环境运行。

- 需要安装`twscrape`库：

  ```cmd
  pip3 install twscrape
  ```

## 运行

本仓库有两个模块的源代码，一个是`src`，另一个是`twsrc`。其中，`src`是基于`snscrape`写的爬取代码，由于2023年7月份推特政策的更新，无法以游客身份继续爬取数据，因此已不可用。`twsrc`是基于`twscrape`写的爬取代码，需要购买账号登录，以完成爬取。

### ~~运行模块`src`~~（已弃用）

运行脚本是`run-pooled.sh`，运行前需要设置相应的变量：

- `DIVIDE_DIR`应该是一个包含有若干`txt`文件的文件夹，其中每个`txt`文件的每一行是一个需要爬取的关键词。

- `DOWNLOAD_DIR`是下载到的数据与`log`文件存放的文件夹。

此外，需要在代码中修改爬取的时间段。具体来说如果爬取模式为多进程或者多线程下载，应该要修改`code/pooled_download.py`中的：

```python
def pooled_download(args: Namespace):

    ...

    def _get_configs(counter_callback = lambda: None):
        temp_count: int = 0
        used_keys = get_used_keys(args)
        download_configs: List[Tuple[tuple, int]] = []
        for key in keys:
            for month in range(12 * 12):
                if (key, month) not in used_keys:
                    until = datetime.datetime(*date_minus((2022, 12), month), day = 1)
                    since = datetime.datetime(*date_minus((2022, 12), month + 1), day = 1)
                    temp_file_path = os.path.join(temp_dir, f'{temp_count :06d}.jsonl')
                    download_configs.append(((key, temp_file_path, until, since), month))
                    temp_count += 1
                    counter_callback()
        return download_configs

    ...
```

设置好后使用命令`bash run-pooled.sh`即可开始运行。

### 运行模块`twsrc`

该模块基于`twscrape`库。该库是基于用户账号的推特爬取库，使用该库时，账号的登录信息会存储在当前目录的`accounts.db`（以`sqlite3`数据库格式）。安装`twscrape`后可以直接在终端调用`twscrape`，可以测试是否在正常工作，例：

```bash
twscrape search china --limit 5
```

**注**：以上命令需要在当前目录的`accounts.db`已经注册过账号后使用。

可以用模块调用的形式调用`twsrc`模块：

```
python3 -m twsrc --help
```

该命令会输出使用该模块的基本方式。在进一步运行代码之前，建议先完成后文[一些注意事项](https://github.com/yanruotian/get-twitter-test#%E4%B8%80%E4%BA%9B%E6%B3%A8%E6%84%8F%E4%BA%8B%E9%A1%B9)中的步骤。

在本仓库中，已经包含了几个默认的配置文件，分别是`twsrc/accounts.txt`，存储了测试用的账号信息；以及`twsrc/keywords-demo.txt`，存储了测试用的需要爬取的关键词。运行以下代码可以对该关键词进行爬取：

```bash
python3 -m twsrc --keywords twsrc/keywords-demo.txt
```

在登录账号后，程序应该会输出以下信息：

```
totally 1 keywords
starting download for keyword "deepin since:2017-08-09 until:2017-08-10"
scraping end, keyword = "deepin since:2017-08-09 until:2017-08-10", count = 71 (1 / 1 = 100.00%), time = 5.18s, total time = 0:00:05, average time = 5.18s, average data = 71.00
```

随后检查当前目录下的`downloads`文件夹，应该可以看到以`jsonl`格式存储的爬取数据。

#### 一些注意事项

- 修改`twscrape`源码，使其支持推特的新域名（`x.com`）。

  详见[github issue](https://github.com/vladkens/twscrape/pull/71)，在推特更改版本后修改了验证邮件信息的中的域名信息，会导致其邮件验证模块失效。当前`pip`源似乎没有同步最新版本的`twscrape`，可以手动在本地的`pip`文件夹处修改其源码，具体在`twscrape.imap._wait_email_code`函数，有以下内容：

  ```python3
  ...

  if min_t is not None and msg_time < min_t:
      return None

  if "info@twitter.com" in msg_from and "confirmation code is" in msg_subj:
      # eg. Your Twitter confirmation code is XXX
      return msg_subj.split(" ")[-1].strip()

  ...
  ```

  修改为：
  
  ```python3
  ...

  # if min_t is not None and msg_time < min_t:
  #     return None

  if "info@x.com" in msg_from and "confirmation code is" in msg_subj:
      # eg. Your Twitter confirmation code is XXX
      return msg_subj.split(" ")[-1].strip()

  ...
  ```

- [可选] 修改`twscrape`源码，减少其超速等待时间。

  由于推特政策的更改，每个账号的爬取速率存在一个限制。具体而言，发送的请求会返回一个`(88) Rate limit exceeded`错误信息。此时可以选择暂停该账号的使用，一段时间后再继续使用该账号爬取。在`twscrape`中该等待时间的默认值为4小时，实际上有点过于保守了，经实测可能设置为15分钟就足够。具体在`twscrape.queue_client.QueueClient._check_rep`函数，有以下内容：

  ```python3
  ...

  # possible new limits for tweets view per account
  if msg.startswith("(88) Rate limit exceeded") or rep.status_code == 429:
      await self._close_ctx(utc_ts() + 60 * 60 * 4)  # lock for 4 hours
      raise RateLimitError(msg)

  ...
  ```

  修改为：

  ```python3
  ...

  # possible new limits for tweets view per account
  if msg.startswith("(88) Rate limit exceeded") or rep.status_code == 429:
      await self._close_ctx(utc_ts() + 60 * 15)  # lock for 15 minutes
      raise RateLimitError(msg)

  ...
  ```

### 并行运行模块`twsrc`

由于`twscrape`是基于异步协程写的，直接在`python`脚本用`multiprocessing`等库开启多进程支持容易导致程序崩溃，因此建议使用`bash`脚本同时开启多个爬虫程序，以实现多进程爬取。

相关参考代码可见`tw-multi/twsrc-multi.sh`，大体思路是先确定多进程的并发数，然后用`split.py`脚本将原账号、代理和关键词文件均分到若干个子文件夹，然后在各个子文件中调用`twsrc`模块。

需要注意该脚本是爬取中国科技实体数据时编写，不一定适用于其它使用情况。

此外也可以基于上述思路用一个`python`主进程管理爬虫子进程，以实现动态分配给每个子进程需要爬取的内容，避免关键词划分不均衡。（没写相关脚本）
