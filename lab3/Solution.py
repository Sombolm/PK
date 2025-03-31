import hashlib
import random
import time
from Utils import Utils


class Solution:

    def __init__(self) -> None:
        self.keys = ["MD5", "SHA1", "SHA2", "SHA3"]
        self.functionNames = [self.generateMD5, self.generateSHA1, self.generateSHA2, self.generateSHA3]
        self.utils = Utils.Utils()

    def generateAll(self,text: str, fileSize: str):
        res = dict()
        keys = self.keys
        functionNames = self.functionNames
        times = dict()


        for idx, functionName in enumerate(functionNames):
            start = time.time_ns()
            res[keys[idx]]= functionName(text.encode())
            end = time.time_ns()
            times[(keys[idx], fileSize, functionName.__name__)] = end - start

        return res, times



    def generateMD5(self,text) -> str:
        return hashlib.md5(text).hexdigest()

    
    def generateSHA1(self, text) -> str:
        return hashlib.sha1(text).hexdigest()

    def generateSHA2(self, text) -> str:
        return hashlib.sha256(text).hexdigest()

    def generateSHA3(self, text) -> str:
        return hashlib.sha384(text).hexdigest()

    def testCollision(self, encodedText, numberOfTests,functionName, numberOfTestingBytes):
        textLen = len(encodedText)
        numberOfCollisions = 0
        testingHash = functionName(encodedText)[:numberOfTestingBytes]

        for i in range(1, numberOfTests + 1):
            randomString = self.utils.generateRandomStringOfLength(textLen).encode()
            if testingHash == functionName(randomString)[:numberOfTestingBytes]:
                numberOfCollisions += 1
        return numberOfCollisions

    def countBits(self,byteSeq):
        binary_representation = ''.join(bin(byte)[2:].zfill(8) for byte in byteSeq)
        numOnes = binary_representation.count('1')
        numZeros = binary_representation.count('0')
        return numZeros, numOnes

    def bitChangeProbability(self,originalHash, newHash):
        xor_result = bytes(a ^ b for a, b in zip(originalHash, newHash))

        _, changedBits = self.countBits(xor_result)

        totalBits = len(originalHash) * 8
        changeProbability = changedBits / totalBits

        return changeProbability

    def testSAC(self, encodedText, functionName, iterations):
        originalText = encodedText
        originalHash = functionName(originalText)
        textLen = len(encodedText)

        probabilities = dict()

        for i in range(iterations):

            randomPosition = random.randint(0, textLen-1)
            encodedTextArray = bytearray(encodedText)
            encodedTextArray[randomPosition] = encodedTextArray[randomPosition] ^ 1

            newText = bytes(encodedTextArray)
            newHash = functionName(newText)

            changeProbability = self.bitChangeProbability(bytes(originalHash.encode()), bytes(newHash.encode()))

            probabilities[i] = changeProbability

        return probabilities

