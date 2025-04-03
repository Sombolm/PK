import random
import time
from collections import defaultdict
import matplotlib.pyplot as plt
import Solution
from Utils import Utils
from Crypto.Util.Padding import pad

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
    flipped_message = bytearray(message, 'utf-8')
    flipped_message[len(flipped_message) // 2] ^= 1
    return flipped_message.decode('utf-8', errors='ignore')

def flipFirstBitOfCipher(cipher):
    flipped_cipher = bytearray(cipher)
    flipped_cipher[0] ^= 1
    return flipped_cipher
def compareBitWiseError(original, damaged):
    numberOfErrors = 0

    original = bytearray(original)
    damaged = bytearray(damaged)

    for i in range(min(len(original), len(damaged))):
        xor = original[i] ^ damaged[i]
        numberOfErrors += bin(xor).count("1")

    return numberOfErrors

def createAllCiphers(key, iv, nonce):
    key = b'0123456789abcdef'
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


    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 2, f'{yval:.2f}%', ha='center', va='bottom')


    plt.subplot(1, 2, 2)
    bars = plt.bar(scenario2.keys(), scenario2.values(), color=['blue', 'green', 'red'])
    plt.xlabel("Encryption Mode")
    plt.ylabel("Error Percentage (%)")
    plt.title("Scenario 2: Errors in Decryption")
    plt.ylim(0, 100)
    plt.yticks(range(0, 101, 10))

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 2, f'{yval:.2f}%', ha='center', va='bottom')

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

    key = b'0123456789abcdef'
    nonce = random.getrandbits(64).to_bytes(8, 'big')
    iv = random.getrandbits(128).to_bytes(16, 'big')
    iterations = 40

    cipherECB, cipherCBC, cipherCTR = createAllCiphers(key, iv, nonce)

    ciphers = [cipherECB, cipherCBC, cipherCTR]
    tags = ["ECB", "CBC", "CTR"]
    times = dict()
    
    for i in range(iterations):
        print("Iteration", i)
        for idx, cipher in enumerate(ciphers):
            for file in filenames:

                cipher = solution.createCipherCBC(key, iv) if tags[idx] == "CBC" else cipher
                cipher = solution.createCipherCTR(key, nonce) if tags[idx] == "CTR" else cipher

                elapsedTime, encrypted = mesaureEncryptionTime(cipher, file)
                times[(tags[idx] , file, i,'encrypted')] = elapsedTime, encrypted
                #print(f"Encryption time for {file} using {tags[idx]}: {elapsedTime} ms")

                cipher = solution.createCipherCBC(key, iv) if tags[idx] == "CBC" else cipher
                cipher = solution.createCipherCTR(key, nonce) if tags[idx] == "CTR" else cipher

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
    for i in range(iterations):
        randomMessage = utils.generateRandomStringOfLength(50)

        cipherECB, cipherCBC, cipherCTR = createAllCiphers(key, iv, nonce)
        paddedMessage = padMessage(randomMessage)

        encryptedECB = solution.encrypt(cipherECB, paddedMessage)
        encryptedCBC = solution.encrypt(cipherCBC, paddedMessage)
        encryptedCTR = solution.encrypt(cipherCTR, paddedMessage)

        damagedMessage = flipFirstBitOfMessage(randomMessage)
        paddedDamagedMessage = padMessage(damagedMessage)

        damagedMessageEncryptedECB = solution.encrypt(cipherECB, paddedDamagedMessage)
        damagedMessageEncryptedCBC = solution.encrypt(cipherCBC, paddedDamagedMessage)
        damagedMessageEncryptedCTR = solution.encrypt(cipherCTR, paddedDamagedMessage)

        for tag, encrypted, damagedEncrypted in zip(["ECB", "CBC", "CTR"], [encryptedECB, encryptedCBC, encryptedCTR],
                                                    [damagedMessageEncryptedECB, damagedMessageEncryptedCBC, damagedMessageEncryptedCTR]):
            numberOfErrors = compareBitWiseError(encrypted, damagedEncrypted)
            sumErrors[tag, 's1'] += numberOfErrors

        #scenario 2
        randomMessage = utils.generateRandomStringOfLength(50)
        paddedMessage = padMessage(randomMessage)

        cipherECB, cipherCBC, cipherCTR = createAllCiphers(key, iv, nonce)

        #tworzenie szyfrogramu
        encryptedECB = solution.encrypt(cipherECB, paddedMessage)
        encryptedCBC = solution.encrypt(cipherCBC, paddedMessage)
        encryptedCTR = solution.encrypt(cipherCTR, paddedMessage)

        damagedEncryptionECB = flipFirstBitOfCipher(encryptedECB)
        damagedEncryptionCBC = flipFirstBitOfCipher(encryptedCBC)
        damagedEncryptionCTR = flipFirstBitOfCipher(encryptedCTR)


        #rozszyfrowanie
        cipherECB, cipherCBC, cipherCTR = createAllCiphers(key, iv, nonce)

        decryptedECB = solution.decrypt(cipherECB, encryptedECB)
        decryptedCBC = solution.decrypt(cipherCBC, encryptedCBC)
        decryptedCTR = solution.decrypt(cipherCTR, encryptedCTR)

        cipherECB, cipherCBC, cipherCTR = createAllCiphers(key, iv, nonce)

        decryptedDamagedECB = solution.decrypt(cipherECB, damagedEncryptionECB)
        decryptedDamagedCBC = solution.decrypt(cipherCBC, damagedEncryptionCBC)
        decryptedDamagedCTR = solution.decrypt(cipherCTR, damagedEncryptionCTR)
        for tag, decrypted, decryptedDamaged in zip(["ECB", "CBC", "CTR"], [decryptedECB, decryptedCBC, decryptedCTR],
                                                    [decryptedDamagedECB, decryptedDamagedCBC, decryptedDamagedCTR]):
            numberOfErrors = compareBitWiseError(decrypted, decryptedDamaged)
            sumErrors[tag, 's2'] += numberOfErrors

    byteLenght = len(decrypted)

    for key in sumErrors:
        sumErrors[key] = (sumErrors[key] / iterations) / (byteLenght * 8) * 100
    plotErrors(sumErrors)

if __name__ == "__main__":
    main()