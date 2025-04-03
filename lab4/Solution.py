from Crypto.Cipher import AES

class Solution:

    def createCipherECB(self, key):
        return AES.new(key, AES.MODE_ECB)

    def createCipherCBC(self, key, iv):
        return AES.new(key, AES.MODE_CBC, iv=iv)

    def createCipherCTR(self, key, nonce):
        return AES.new(key, AES.MODE_CTR, nonce=nonce)

    def encrypt(self, cipher, text):
        return cipher.encrypt(text)

    def decrypt(self, cipher, text):
        return cipher.decrypt(text)