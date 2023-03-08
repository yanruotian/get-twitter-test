import os

def main():
    dirPath = './downloaded'
    outputFile = './upload.sh'
    file = open(outputFile, 'w+')
    fileNames = os.listdir(dirPath)
    fileNames.sort()
    for fileName in fileNames:
        file.write(f'scp {os.path.join(dirPath, fileName)} 117:/data_new/private/yanruotian/get-twitter-data/china-tec-new/{fileName}\n')
    file.close()

if __name__ == '__main__':
    main()

