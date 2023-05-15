import json

JSON_FILES = ('zh_alias_simple.json', 'zh_label_simple.json')

for jsonPath in JSON_FILES:
    with open(jsonPath, 'r') as file:
        content = json.load(file)
    outputPath = jsonPath[: -len('.json')] + '-transed.json'
    with open(outputPath, 'w') as file:
        json.dump(content, file, ensure_ascii = False)
        