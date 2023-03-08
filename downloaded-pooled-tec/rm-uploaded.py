import os
import tqdm

for i in tqdm.tqdm(range(9453)):
    filePath = f'./downloaded/{i :06d}.jsonl'
    if os.path.isfile(filePath):
        os.system(f'rm "{filePath}"')
    else:
        print(f'path not a file: {filePath}')

