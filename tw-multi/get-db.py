import os
import sqlite3

DB_PATH = '/root/wangxing_test/accounts.db'

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def main():
    accounts = set()
    conn = sqlite3.connect(DB_PATH)
    # conn.raw_factory = dict_factory
    cursor = conn.cursor()
    for result in cursor.execute('select * from accounts'):
        if int(result[5]) == 1:
            accounts.add(':'.join(result[: 4]))
    conn.close()
    print(f'accounts count = {len(accounts)}')
    for root, _, files in os.walk('splits'):
        continue
        for fileName in filter(lambda name: name == 'accounts.txt', files):
            path = os.path.join(root, fileName)
            print(path)
            with open(path, 'r') as file:
                accounts -= {':'.join(line.strip().split(':')[: 4]) for line in file}
    print(f'accounts count = {len(accounts)}')
    with open('accounts-all.txt', 'w') as file:
        for account in accounts:
            file.write(account + '\n')

if __name__ == '__main__':
    main()
