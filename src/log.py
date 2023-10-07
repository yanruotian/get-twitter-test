import os
import pytz
import datetime

from typing import Iterable

class Logger:

    class FakeFile:
        def write(self, *args, **wargs):
            pass
        def close(self):
            pass

    def __init__(self, args, do_print: bool = True, process_num: int = None):
        log_file_path: str = args.log_path
        self.log_file_record = []
        if log_file_path:
            os.makedirs(os.path.dirname(log_file_path), exist_ok = True)
            if os.path.isfile(log_file_path):
                backup_file_path = 'log_backup'
                with open(log_file_path, 'r') as file:
                    with open(backup_file_path, 'w+') as backup_file:
                        for line in file:
                            backup_file.write(line.replace('\n', '') + '\n')
                self.log_file_record = open(backup_file_path, 'r')
            self.file = open(log_file_path, 'w+')
        else:
            self.file = Logger.FakeFile()
        self.mute = False
        self.do_print = do_print
        self.process_string = ''
        self.set_process_num(process_num)
        self.create_time = datetime.datetime.now(pytz.UTC)

    def set_process_num(self, process_num: int = None):
        self.process_num = process_num
        if self.process_num is not None:
            process_string = f'{self.process_num :2d}'.replace(' ', '0')
            self.process_string = f'[process {process_string}] '

    def open(self, log_file_path: str):
        self.file.close()
        self.file = open(log_file_path, 'w+')

    def close(self):
        self.file.close()

    def logln(self, content: str = ''):
        if not self.mute:
            content = f'{datetime.datetime.now(pytz.UTC)} - {content}'
            self.file.write(content + '\n')
            if self.do_print:
                print(self.process_string + content)

    def log_iter(self, iter: Iterable, max_length: int = 190, prefix: str = ''):
        self.logln(prefix + r'(')
        line = '    '
        for item in iter:
            line += f'"{item}", '
            if len(line) >= max_length:
                self.logln(line)
                line = '    '
        if len(line.strip()) > 0:
            self.logln(line)
        self.logln(r')')
