# 推特数据爬取

## 环境安装

需要安装`snscrape`库：

```cmd
pip3 install snscrape
```

## 运行

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
