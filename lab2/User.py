import random


class User:
    def __init__(self, id, n, g):
        self.id = id

        self.x = random.randint(10**6, 10**7)
        self.n = n
        self.g = g

        self.privateKey = random.randint(10**6, 10**7)
        self.publicKey = pow(self.g, self.privateKey, self.n)

        self.sessionKeys = {}

    def addSessionKey(self, Userid, Publickey):
        self.sessionKeys[Userid] = pow(Publickey, self.privateKey, self.n)

    def getSessionKey(self, Userid):
        return self.sessionKeys[Userid]

    def getPublicKey(self):
        return self.publicKey