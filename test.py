import json
import datetime

from snscrape.modules.twitter import TwitterSearchScraper

def item_to_dict(item) -> dict:
    result = dict()
    result['content'] = item.content
    result['url'] = item.url
    result['username'] = item.username
    result['date'] = str(item.date)
    return result

def main():
    until = (datetime.datetime.now() - datetime.timedelta(days = 1)).strftime(r'%Y-%m-%d')
    since = (datetime.datetime.now() - datetime.timedelta(days = 2)).strftime(r'%Y-%m-%d')
    content = f'清洁剂 until:{until} since:{since}'
    print(content)
    scraper = TwitterSearchScraper(content)
    count = 10
    for item in scraper.get_items():
        print('!')
        result = json.loads(item.json())
        result['keyword'] = '---test---'
        print(f'[{count}]' + json.dumps(result, ensure_ascii = False))
        # print(json.dumps(item_to_dict(item), ensure_ascii = False))
        count -= 1
        if count <= 0:
            break

if __name__ == '__main__':
    main()
