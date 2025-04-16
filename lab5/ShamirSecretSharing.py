import random
import sympy as sp


class ShamirSecretSharing:

    def __init__(self):
        pass

    def getNextPrime(self, n: int) -> int:
        return sp.nextprime(n)

    def divideSecret(self, secret: int, numberOfShares: int, requiredNumberOfShares: int, prime: int) -> tuple:

        def polynomial(x):
            return sum(coef * (x ** i) for i, coef in enumerate(a)) % prime

        print("Dividing secret:", secret)
        print("Number of shares:", numberOfShares)

        if prime is None:
            prime = self.getNextPrime(max(secret, numberOfShares) ** 10)

        print("Using prime:", prime)
        a = [secret] + [random.randint(1, prime - 1) for _ in range(requiredNumberOfShares - 1)]
        shares = [(i, polynomial(i)) for i in range(1, numberOfShares + 1)]

        print(f"Shares: {shares}")
        return shares, prime

    def reconstructSecret(self, shares: list, prime: int) -> int:

        def lagrangeInterpolation(x, x_values, y_values):
            total = 0
            for i in range(len(x_values)):
                xi, yi = x_values[i], y_values[i]
                term = yi
                for j in range(len(x_values)):
                    if j != i:
                        term *= (x - x_values[j]) * pow(xi - x_values[j], -1, prime) % prime
                total += term
            return total % prime

        x_vals = [x for x, _ in shares]
        y_vals = [y for _, y in shares]

        secret = lagrangeInterpolation(0, x_vals, y_vals)

        print("Reconstructed secret:", secret)
        return secret