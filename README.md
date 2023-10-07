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
python3 -m twsrc -h
```

该命令会输出使用该模块的基本方式。在进一步运行代码之前，建议先完成后文<a name="一些注意事项">一些注意事项</a>中的步骤。

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

- 修改`twscrape`源码，使其支持推特的新域名（`x.com`）

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
