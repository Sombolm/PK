from collections import defaultdict
import User
from Utils import Utils

class DH:

    def run(self, numberOfUsers):
        UserList = []
        utils = Utils.Utils()

        n = utils.generateNLenghtPrime(5)
        g = utils.generateRelativePrime(n)

        for i in range(numberOfUsers):
            UserList.append(User.User(i, n, g))

        for i in range(numberOfUsers):
            for j in range(numberOfUsers):
                if i != j:
                    UserList[i].addSessionKey(j, UserList[j].getPublicKey())

        print(UserList[0].getSessionKey(1))
        print(UserList[1].getSessionKey(0))
