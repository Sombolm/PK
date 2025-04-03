import random
import string

import sympy as sp

class Utils:

    def generateNLenghtPrime(self, n):
        return sp.randprime(10**(n-1), 10**n-1)

    def generateRelativePrime(self, n):
        while True:
            e = sp.randprime(1, n-1)
            if sp.gcd(e, n) == 1:
                return e

    def stringToNumberArray(self, string):
        return [ord(char) for char in string]

    def numberToStringArray(self, number):
        return [chr(num) for num in number]

    def generateRandomStringOfLength(self, n):
        return ''.join([chr(random.randint(65, 122)) for i in range(n)])

    def loadFile(self,fileName: str):
        with open(fileName, "r") as f:
            return f.read()

    def generateRandomFileOfSizeInMB(self,size: int):
        #check if file exists
        try:
            with open(str(size) + ".txt", 'r') as f:
                return str(size) + ".txt"
        except FileNotFoundError:
            pass

        size_in_bytes = size * 1024 * 1024
        content = ''.join(random.choices(string.ascii_letters + string.digits, k=size_in_bytes))
        with open(str(size) + ".txt", 'w') as f:
            f.write(content)

        f.close()
        return str(size) + ".txt"

    def generateFilesOfSizes(self,fileSizes):
        for i in range(len(fileSizes)):
            self.generateRandomFileOfSizeInMB(fileSizes[i])
            yield str(fileSizes[i]) + ".txt"