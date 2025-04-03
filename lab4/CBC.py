from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

class CBC:
    def __init__(self, key, iv):
        self.key = key
        self.iv = iv
        self.block_size = 16
        self.cipher = AES.new(key, AES.MODE_ECB)

    def encrypt(self, message):
        message = pad(message, self.block_size)

        previousBlock = self.iv
        encrypted = b''

        for i in range(0, len(message), self.block_size):
            block = message[i:i + self.block_size]
            block = bytes(a ^ b for a, b in zip(block, previousBlock))
            encryptedBlock = self.cipher.encrypt(block)
            encrypted += encryptedBlock
            previousBlock = encryptedBlock

        return encrypted

    def decrypt(self, encrypted):
        previousBlock = self.iv

        decrypted = b''

        for i in range(0, len(encrypted), self.block_size):
            block = encrypted[i:i + self.block_size]
            decryptedBlock = self.cipher.decrypt(block)
            decrypted += bytes(a ^ b for a, b in zip(decryptedBlock, previousBlock))
            previousBlock = block

        return unpad(decrypted, self.block_size)
