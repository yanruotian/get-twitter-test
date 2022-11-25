import json

from snscrape.modules.twitter import TwitterSearchScraper

def item_to_dict(item) -> dict:
    result = dict()
    result['content'] = item.content
    result['url'] = item.url
    result['username'] = item.username
    result['date'] = str(item.date)
    return result

def main():
    scraper = TwitterSearchScraper('什么')
    count = 10
    for item in scraper.get_items():
        print('!')
        result = json.loads(item.json())
        result['keyword'] = '---test---'
        print(json.dumps(result, ensure_ascii = False))
        # print(json.dumps(item_to_dict(item), ensure_ascii = False))
        count -= 1
        if count <= 0:
            break

if __name__ == '__main__':
    main()
