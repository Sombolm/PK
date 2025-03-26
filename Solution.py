class Solution:

    def __init__(self) -> None:
        self.keys = []
        self.functionsNames = []


    def generateAll(self,text: str):
        res = dict()
        keys = self.keys
        functionNames = self.functionsNames

        for idx, functionName in enumerate(functionNames):
            res[keys[idx]]= functionName(text)

        return res



    def generateMD5(self,text: str) -> str:
        return text
    
    def generateSHA1(self, text: str) -> str:
        return text

    def generateSHA2(self, text: str) -> str:
        return text

    def generateSHA3(self, text: str) -> str:
        return text