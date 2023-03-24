import pytz
import time
import datetime

from .log import Logger
from .args import get_args
from .divide import divide
from .download import download
from .transform import transform
from .pooled_download import pooled_download

def main(args):
    start_time = time.time()
    args.time = datetime.datetime.now(tz = pytz.UTC)
    args.logger = Logger(args)
    mode: str = args.mode
    if mode == 'transform':
        transform(args)
    elif mode == 'divide':
        divide(args)
    elif mode == 'download':
        args.logger.set_process_num(args.n)
        download(args)
    elif mode in {'pooled-download', 'threaded-download'}:
        pooled_download(args)
    end_time = time.time()
    args.logger.logln(f'download finished, time spent = {datetime.timedelta(seconds = int(end_time - start_time))}')
    args.logger.close()

if __name__ == '__main__':
    main(get_args())
    