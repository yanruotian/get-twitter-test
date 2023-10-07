'''
运行方式：

```bash
python3 -m twsrc
```
'''

import os
import logging

from twscrape.logger import set_log_level

print(f'pwd = {os.environ.get("PWD")}')

logFilePath = os.environ.get('LOG_FILE', None) or 'tw-fix.log'
if (len(dirName := os.path.dirname(logFilePath)) > 0):
    os.makedirs(dirName, exist_ok = True)

logging.basicConfig(
    filename = logFilePath,
    format = '%(asctime)s - %(levelname)s - %(message)s',
    level = logging.INFO,
)

set_log_level("DEBUG")

