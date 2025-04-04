import random
import time
from collections import defaultdict
import matplotlib.pyplot as plt
import Solution
from Utils import Utils
from Crypto.Util.Padding import pad, unpad

solution = Solution.Solution()
utils = Utils.Utils()
def plotTimes(avgTimes):
    encryption_times = {}
    decryption_times = {}

    for (tag, filename, operation), time in avgTimes.items():
        size = int(filename.split(".")[0])  # Extract file size from filename
        if operation == "encrypted":
            if tag not in encryption_times:
                encryption_times[tag] = []
            encryption_times[tag].append((size, time))
        else:
            if tag not in decryption_times:
                decryption_times[tag] = []
            decryption_times[tag].append((size, time))

    # Sort values by file size
    for tag in encryption_times:
        encryption_times[tag].sort()
    for tag in decryption_times:
        decryption_times[tag].sort()

    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    for tag, values in encryption_times.items():
        sizes, times = zip(*values)
        plt.plot(sizes, times, marker='o', label=f"{tag} Encryption")
    plt.xlabel("File Size (mega bytes)")
    plt.ylabel("Time (ms)")
    plt.title("Encryption Time vs File Size")
    plt.legend()
    plt.grid()

    plt.subplot(1, 2, 2)
    for tag, values in decryption_times.items():
        sizes, times = zip(*values)
        plt.plot(sizes, times, marker='o', label=f"{tag} Decryption")
    plt.xlabel("File Size (mega bytes)")
    plt.ylabel("Time (ms)")
    plt.title("Decryption Time vs File Size")
    plt.legend()
    plt.grid()

    plt.tight_layout()
    plt.show()

def flipFirstBitOfMessage(message):
    flipped_message = bytearray(message)
    flipped_message[0] ^= 0b00000001
    return bytes(flipped_message)

def flipFirstBitOfCipher(cipher):
    flipped_cipher = bytearray(cipher)
    original = flipped_cipher.copy()
    flipped_cipher[0] ^= 0b00000001
    for i in range(len(original)):
        if original[i] != flipped_cipher[i]:
            print("Flipped byte at index", i, "from", original[i], "to", flipped_cipher[i])

    return bytes(flipped_cipher)


def compareBlockWiseError(original, damaged, blockSize=16):
    damaged_blocks = 0

    original = bytearray(original)
    damaged = bytearray(damaged)

    numBlocks = min(len(original), len(damaged)) // blockSize

    for i in range(numBlocks):
        blockStart = i * blockSize
        blockEnd = blockStart + blockSize

        originalBlock = original[blockStart:blockEnd]
        damagedBlock = damaged[blockStart:blockEnd]

        if originalBlock != damagedBlock:
            damaged_blocks += 1

    return damaged_blocks

def createAllCiphers(key, iv, nonce):
    cipherECB = solution.createCipherECB(key)
    cipherCBC = solution.createCipherCBC(key, iv)
    cipherCTR = solution.createCipherCTR(key, nonce)

    return cipherECB, cipherCBC, cipherCTR

def padMessage(message):
    return pad(message.encode('utf-8'), 16)

def plotErrors(sumErrors):
    scenario1 = {}
    scenario2 = {}

    for (tag, scenario), errors in sumErrors.items():
        if scenario == 's1':
            if tag not in scenario1:
                scenario1[tag] = errors
        else:
            if tag not in scenario2:
                scenario2[tag] = errors


    plt.figure(figsize=(12, 6))


    plt.subplot(1, 2, 1)
    bars = plt.bar(scenario1.keys(), scenario1.values(), color=['blue', 'green', 'red'])
    plt.xlabel("Encryption Mode")
    plt.ylabel("Error Percentage (%)")
    plt.title("Scenario 1: Errors in Encryption")
    plt.ylim(0, 100)
    plt.yticks(range(0, 101, 10))

    '''
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 2, f'{yval:.2f}%', ha='center', va='bottom')
    '''

    plt.subplot(1, 2, 2)
    bars = plt.bar(scenario2.keys(), scenario2.values(), color=['blue', 'green', 'red'])
    plt.xlabel("Encryption Mode")
    plt.ylabel("Error Percentage (%)")
    plt.title("Scenario 2: Errors in Decryption")
    plt.ylim(0, 100)
    plt.yticks(range(0, 101, 10))

    '''
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 2, f'{yval:.2f}%', ha='center', va='bottom')
    '''
    plt.tight_layout()
    plt.show()

def mesaureEncryptionTime(cipher, file):
    start = time.time_ns()
    encrypted = solution.encrypt(cipher, utils.loadFile(file).encode('utf-8'))
    end = time.time_ns()
    elapsed_time = ((end - start )) / 1_000_000
    return elapsed_time, encrypted

def mesaureDecryptionTime(cipher, encrypted):
    start = time.time_ns()
    decrypted = solution.decrypt(cipher, encrypted)
    end = time.time_ns()
    elapsed_time = ((end - start )) / 1_000_000
    return elapsed_time, decrypted

def main():


    #zad 1
    sizes = [10, 15, 20]
    filenames = [str(size) + ".txt" for size in sizes]
    print(filenames)
    files = utils.generateFilesOfSizes(sizes)

    for file in files:
        print(f"File {file} generated")

    keyForCypher = b'0123456789abcdef'
    nonce = random.getrandbits(64).to_bytes(8, 'big')
    iv = random.getrandbits(128).to_bytes(16, 'big')
    iterations = 40

    cipherECB, cipherCBC, cipherCTR = createAllCiphers(keyForCypher, iv, nonce)

    ciphers = [cipherECB, cipherCBC, cipherCTR]
    tags = ["ECB", "CBC", "CTR"]
    times = dict()
    
    for i in range(0):
        print("Iteration", i)
        for idx, cipher in enumerate(ciphers):
            for file in filenames:

                cipher = solution.createCipherCBC(keyForCypher, iv) if tags[idx] == "CBC" else cipher
                cipher = solution.createCipherCTR(keyForCypher, nonce) if tags[idx] == "CTR" else cipher

                elapsedTime, encrypted = mesaureEncryptionTime(cipher, file)
                times[(tags[idx] , file, i,'encrypted')] = elapsedTime, encrypted
                #print(f"Encryption time for {file} using {tags[idx]}: {elapsedTime} ms")

                cipher = solution.createCipherCBC(keyForCypher, iv) if tags[idx] == "CBC" else cipher
                cipher = solution.createCipherCTR(keyForCypher, nonce) if tags[idx] == "CTR" else cipher

                elapsedTime, decrypted = mesaureDecryptionTime(cipher, encrypted)
                times[(tags[idx] , file,i ,'decrypted')] = elapsedTime, decrypted
                #print(f"Decryption time for {file} using {tags[idx]}: {elapsedTime} ms")

    sum = defaultdict(float)
    for key in times:
        sum[key[0], key[1], key[3]] = sum[key[0], key[1], key[3]] + times[key][0]
    avgTimes = defaultdict(float)
    for key in sum:
        avgTimes[key] = sum[key] / iterations
    plotTimes(avgTimes)


    # zad 2
    sumErrors = defaultdict(float)
    for i in range(1):
        iv = random.getrandbits(128).to_bytes(16, 'big')
        randomMessage = utils.generateRandomStringOfLength(50)

        cipherECB, cipherCBC, cipherCTR = createAllCiphers(keyForCypher, iv, nonce)
        paddedMessage = padMessage(randomMessage)

        encryptedECB = solution.encrypt(cipherECB, bytearray(paddedMessage))
        encryptedCBC = solution.encrypt(cipherCBC, bytearray(paddedMessage))
        encryptedCTR = solution.encrypt(cipherCTR, bytearray(paddedMessage))

        damagedMessage = flipFirstBitOfMessage(bytearray(paddedMessage))
        paddedDamagedMessage = damagedMessage

        cipherECB, cipherCBC, cipherCTR = createAllCiphers(keyForCypher, iv, nonce)

        damagedMessageEncryptedECB = solution.encrypt(cipherECB, bytearray(paddedDamagedMessage))
        damagedMessageEncryptedCBC = solution.encrypt(cipherCBC, bytearray(paddedDamagedMessage))
        damagedMessageEncryptedCTR = solution.encrypt(cipherCTR, bytearray(paddedDamagedMessage))

        for tag, encrypted, damagedEncrypted in zip(["ECB", "CBC", "CTR"], [encryptedECB, encryptedCBC, encryptedCTR],
                                                    [damagedMessageEncryptedECB, damagedMessageEncryptedCBC, damagedMessageEncryptedCTR]):
            numberOfErrors = compareBlockWiseError(encrypted, damagedEncrypted)
            sumErrors[tag, 's1'] += numberOfErrors

        #scenario 2
        randomMessage = utils.generateRandomStringOfLength(50)
        paddedMessage = padMessage(randomMessage)

        cipherECB, cipherCBC, cipherCTR = createAllCiphers(keyForCypher, iv, nonce)

        #tworzenie szyfrogramu
        encryptedECB = solution.encrypt(cipherECB, bytearray(paddedMessage))
        encryptedCBC = solution.encrypt(cipherCBC, bytearray(paddedMessage))
        encryptedCTR = solution.encrypt(cipherCTR, bytearray(paddedMessage))

        damagedEncryptionECB = flipFirstBitOfCipher(encryptedECB)
        damagedEncryptionCBC = flipFirstBitOfCipher(encryptedCBC)
        damagedEncryptionCTR = flipFirstBitOfCipher(encryptedCTR)


        #rozszyfrowanie
        cipherECB, cipherCBC, cipherCTR = createAllCiphers(keyForCypher, iv, nonce)

        decryptedECB = solution.decrypt(cipherECB, bytearray(encryptedECB))
        decryptedCBC = solution.decrypt(cipherCBC, bytearray(encryptedCBC))
        decryptedCTR = solution.decrypt(cipherCTR, bytearray(encryptedCTR))

        cipherECB, cipherCBC, cipherCTR = createAllCiphers(keyForCypher, iv, nonce)

        decryptedDamagedECB = solution.decrypt(cipherECB, bytearray(damagedEncryptionECB))
        decryptedDamagedCBC = solution.decrypt(cipherCBC, bytearray(damagedEncryptionCBC))
        decryptedDamagedCTR = solution.decrypt(cipherCTR, bytearray(damagedEncryptionCTR))
        for tag, decrypted, decryptedDamaged in zip(["ECB", "CBC", "CTR"], [decryptedECB, decryptedCBC, decryptedCTR],
                                                    [decryptedDamagedECB, decryptedDamagedCBC, decryptedDamagedCTR]):
            numberOfErrors = compareBlockWiseError(decrypted, decryptedDamaged)
            sumErrors[tag, 's2'] += numberOfErrors

    byteLenght = len(bytes(decrypted))

    for key in sumErrors:
        sumErrors[key] = (sumErrors[key]) / (byteLenght / 16) * 100
    plotErrors(sumErrors)

if __name__ == "__main__":
    main()