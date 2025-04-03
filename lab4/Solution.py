from Crypto.Cipher import AES

class Solution:

    def createCipher(self, key, mode):
        cipher = AES.new(key, mode)
        nonce = cipher.nonce

        return cipher, nonce

    def encrypt(self, cipher, text):
        return cipher.encrypt(text)

    def decrypt(self, cipher, text):
        return cipher.decrypt(text)