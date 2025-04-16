import NaiveSecretSharing
import ShamirSecretSharing
def main():

    print("Naive Secret Sharing")
    nss = NaiveSecretSharing.NaiveSecretSharing()
    secret = 10
    numberOfShares = 5


    shares, k = nss.dividieSecret(secret, numberOfShares)
    print("-" * 50)
    secret = nss.reconstructSecret(shares, k)
    print("-" * 100)
    print("Shamir Secret Sharing")
    sss = ShamirSecretSharing.ShamirSecretSharing()
    secret = 10
    numberOfShares = 5
    requiredNumberOfShares = 3

    shares, prime = sss.divideSecret(secret, numberOfShares, requiredNumberOfShares, None)
    print("-" * 50)
    requiredShares = shares[:requiredNumberOfShares]
    print("Using shares:", requiredShares)
    secret = sss.reconstructSecret(requiredShares, prime)
    print("-" * 50)
    print("Using all shares")
    secret = sss.reconstructSecret(shares, prime)




if __name__ == "__main__":
    main()