from datetime import datetime, timedelta

def genDate(start: tuple, end: tuple, step = timedelta(days = 1)):
    _start = datetime(*start)
    _end = datetime(*end)
    while _start < _end:
        yield _start
        _start += step

def formatDate(date: datetime):
    return '{:04d}-{:02d}-{:02d}'.format(
        date.year, date.month, date.day
    )

with open('keywords-wechat.txt', 'w') as file:
    for date in genDate((2021, 1, 1), (2023, 1, 1)):
        file.write(
            f"wechat since:{formatDate(date)} "
            f"until:{formatDate(date + timedelta(days = 1))}\n"
        )