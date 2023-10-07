import os


class Writer:

    def __init__(
        self, 
        outputDir: str, 
        lineNum: int = 20000, 
        startFileIndex: int = 0,
    ):
        self.outputDir = outputDir
        self.maxLineCount = lineNum
        self.fileIndex = startFileIndex
        self.lineCount = 0
        self.file = None
        os.makedirs(self.outputDir, exist_ok = True)

    def __enter__(self):
        return self
    
    def __exit__(self, *_a, **_w):
        self.close()

    @classmethod
    def fileIndexToName(cls, fileIndex: int):
        return f'{fileIndex :06d}.jsonl'

    def getFileName(self):
        while os.path.exists(os.path.join(
            self.outputDir, self.fileIndexToName(self.fileIndex),
        )):
            self.fileIndex += 1
        return self.fileIndexToName(self.fileIndex)
    
    def open(self):
        if self.file is not None:
            self.close()
        self.lineCount = 0
        self.file = open(os.path.join(
            self.outputDir, self.getFileName(),
        ), 'w')
    
    def close(self):
        if self.file is not None:
            self.file.close()
            self.file = None

    def writeLine(self, content: str):
        if self.file is None:
            self.open()
        self.file.write(content)
        self.lineCount += 1
        if self.lineCount >= self.maxLineCount:
            self.close()