# 推特数据爬取

## 环境安装

需要安装`twscrape`库：

```cmd
pip3 install twscrape
```

## 运行

本仓库有两个模块的源代码，一个是`src`，另一个是`twsrc`。其中，`src`是基于`snscrape`写的爬取代码，由于2023年7月份推特政策的更新，无法以游客身份继续爬取数据，因此已不可用。`twsrc`是基于`twscrape`写的爬取代码，需要购买账号登录，以完成爬取。

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
