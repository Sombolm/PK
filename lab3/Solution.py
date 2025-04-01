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

    def generateMD5Digest(self,text):
        return hashlib.md5(text).digest()

    
    def generateSHA1(self, text) -> str:
        return hashlib.sha1(text).hexdigest()

    def generateSHA1Digest(self, text):
        return hashlib.sha1(text).digest()

    def generateSHA2(self, text) -> str:
        return hashlib.sha256(text).hexdigest()

    def generateSHA2Digest(self, text):
        return hashlib.sha256(text).digest()

    def generateSHA3(self, text) -> str:
        return hashlib.sha384(text).hexdigest()

    def generateSHA3Digest(self, text):
        return hashlib.sha384(text).digest()

    def testCollision(self, encodedText, numberOfTests,functionName, numberOfTestingBytes):
        textLen = len(encodedText)
        numberOfCollisions = 0
        testingHash = functionName(encodedText)[:numberOfTestingBytes]

        for i in range(1, numberOfTests + 1):
            randomString = self.utils.generateRandomStringOfLength(textLen).encode()
            randomHash = functionName(randomString)[:numberOfTestingBytes]

            xorResult = bytes(a ^ b for a, b in zip(testingHash, randomHash))

            if xorResult == b'\x00' * numberOfTestingBytes:
                numberOfCollisions += 1

        return numberOfCollisions

    def countBits(self,byteSeq):
        binaryRepresentation = ''.join(bin(byte)[2:].zfill(8) for byte in byteSeq)
        numOnes = binaryRepresentation.count('1')
        numZeros = binaryRepresentation.count('0')
        return numZeros, numOnes

    def bitChangeProbability(self,originalHash, newHash):
        xorResult = bytes(a ^ b for a, b in zip(originalHash, newHash))

        _, changedBits = self.countBits(xorResult)

        totalBits = len(originalHash) * 8
        changeProbability = changedBits / totalBits

        return changeProbability

    def testSAC(self, encodedText, functionName, iterations):
        originalText = encodedText
        originalHash = functionName(originalText)

        probabilities = dict()

        for i in range(iterations):

            encodedTextArray = bytearray(encodedText)

            randomPosition = random.randint(0, len(encodedTextArray) - 1)
            randomBitIndex = random.randint(0, 7)

            encodedTextArray[randomPosition] ^= (1 << randomBitIndex)

            newText = bytes(encodedTextArray)
            newHash = functionName(newText)

            changeProbability = self.bitChangeProbability(bytes(originalHash), bytes(newHash))

            probabilities[i] = changeProbability

        return probabilities

