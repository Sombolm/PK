import random


class NaiveSecretSharing:

    def __init__(self):
        pass

    def dividieSecret(self, secret: int, numberOfShares) -> tuple:
        print("Dividing secret:", secret)
        print("Number of shares:", numberOfShares)

        shares = []
        k = secret + 1

        for i in range(numberOfShares - 1):
            shares.append(
                random.randint(0, k - 1)
            )

        for share in shares:
            secret -= share

        shares.append(secret % k)

        print(f"Shares: {shares}, k: {k}")
        return shares, k

    def reconstructSecret(self, shares: list, k: int) -> int:
        secret = 0
        for share in shares:
            secret += share

        secret = secret % k
        print("Reconstructed secret:", secret)
        return secret