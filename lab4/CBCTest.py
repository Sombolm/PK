import CBC

key = b'0123456789abcdef'
iv = b'0123456789abcdef'

cbc = CBC.CBC(key, iv)
message = b'Czy dziala CBC?'
encrypted = cbc.encrypt(message)
print("Original:", message)
print("Encrypted:", encrypted)
decrypted = cbc.decrypt(encrypted)
print("Decrypted:", decrypted)
