from Crypto.Cipher import AES

class AES():
    def __init__(self, key):
        self.key = key

    def encrypt(self, plaintext):
        return "encrypted"

    def decrypt(self, ciphertext):
        return "decrypted"