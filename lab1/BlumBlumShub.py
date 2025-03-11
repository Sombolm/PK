import random
import sympy

class BlumBlumShub:
    def __init__(self, length=3, iterations=20000):
        self.p = self.generatePrimeNumber3Mod4(length=length)
        self.q = self.generatePrimeNumber3Mod4(length=length, start=self.p + 1)
        self.n = self.p * self.q
        self.iterations = iterations

    def generatePrimeNumber3Mod4(self,length: int, **kwargs) -> int:
        #start = kwargs.get("start", 10**(length - 1)) gets a good pair of primes (103, 107)
        start = kwargs.get("start", random.randint(10**(length - 1), 10**length))
        end = 10**length

        while True:
            prime = sympy.nextprime(start)
            if prime > end:
                raise Exception("No prime number found")
            elif prime % 4 == 3:
                return prime
            start = prime + 1

    def generate(self) -> list:
        print("Generating bits for p =", self.p, "q =", self.q)
        while True:
            x = sympy.randprime(1, self.n - 1)
            if sympy.gcd(x, self.n) == 1:
                break

        bits = []
        for _ in range(self.iterations):
            x = pow(x, 2, self.n)
            bits.append(x & 1)
        print("Generated", len(bits), "bits")
        print("First 10 bits:", bits[:10])
        return bits