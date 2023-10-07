KEYWORDS_FILE = 'days.keywords'
SCRAPED_FILE = '/root/get-twitter-test/downloaded/china-tec-2023-06-21/scraped.keywords'
OUTPUT_FILE = 'keywords.renewed'

def getKeywords(filePath: str):
    with open(filePath, 'r') as file:
        result = {line.strip() for line in file}
    return result

TOTAL = getKeywords(KEYWORDS_FILE)
SCRAPED = getKeywords(SCRAPED_FILE)
assert len(SCRAPED - TOTAL) == 0

with open(OUTPUT_FILE, 'w') as file:
    for keyword in TOTAL - SCRAPED:
        file.write(keyword + '\n')
        