import random

from Utils import Utils

class RSA:
    def __init__(self, primeLength):
        self.utils = Utils.Utils()
        self.p = self.utils.generateNLenghtPrime(primeLength)
        self.q = self.utils.generateNLenghtPrime(primeLength)

    def generateKey(self):
        n = self.p * self.q
        phi = (self.p - 1) * (self.q - 1)

        e = self.utils.generateRelativePrime(phi)
        d = pow(e, -1, phi)

        publicKey = (n, e)
        privateKey = (n, d)

        return publicKey, privateKey

    def encrypt(self, message: int, key):
        return pow(message, key[1], key[0])

    def decrypt(self, message: int, key):
        return pow(message, key[1], key[0])

    def encryptArray(self, message: list, key):
        return [self.encrypt(char, key) for char in message]

    def decryptArray(self, message: list, key):
        return [self.decrypt(char, key) for char in message]