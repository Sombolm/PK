import RSA
import DH
from Utils import Utils

#zad 1
def test_rsa():
    rsa = RSA.RSA(4)
    utils = Utils.Utils()

    publicKey, privateKey = rsa.generateKey()

    message = utils.generateRandomStringOfLength(50)
    print(f"Message: {message}")

    messageArray = utils.stringToNumberArray(message)
    print(f"Message array: {messageArray}")

    encryptedMessage = rsa.encryptArray(messageArray, publicKey)
    print(f"Encrypted message: {encryptedMessage}")

    decryptedMessage = rsa.decryptArray(encryptedMessage, privateKey)
    print(f"Decrypted message: {decryptedMessage}")

    decryptedMessageString = utils.numberToStringArray(decryptedMessage)
    print(f"Decrypted message string: {''.join(decryptedMessageString)}")

def test_dh():
    dh = DH.DH()
    dh.run(4)

def main():
    test_rsa()
    test_dh()

if __name__ == "__main__":
    main()