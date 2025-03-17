import random
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