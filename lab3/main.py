import Solution
from Sprawozdanie import runSprawozdanie

def generateRandomStrings():
    import random
    import string
    testingStrings = []
    for i in range(4,100,10):
        testingStrings.append(''.join(random.choices(string.ascii_uppercase + string.digits, k = i)))
    return testingStrings

def main():
    #zad2
    testingStrings = generateRandomStrings()
    solution = Solution.Solution()
    timesDict = dict()
    results = dict()

    for string in testingStrings:
        res,times = solution.generateAll(string)
        results[len(string)] = {key: len(res[key]) for key in res}
        timesDict[len(string)] = times
    #Niezaleznie od dlugosci stringa, MD5: 32. SHA1: 40, SHA2: 64, SHA3: 96
    #Dodatkowo funkcje sa na tyle szybkie ze nie mozliwe jest zmierzenie ich czasu wykonania (za pomoca time_ns)

    #zad3
    generated = solution.generateMD5("test".encode())
    #print(generated)
    #wartosc wygenerowana: 098f6bcd4621d373cade4e832627b4f6 jest powszechnie znana jako hash dla slowa "test"
    #Skróty wygenerowane dla krótkich i popularnych haseł nie są bezpieczne ponieważ znajdują się w jawnych słownikach umożliwiających
    #zgadnięcie takiego hasła

    #zad4
    #Funkcje MD5 nie może zostać uznana za bezpieczną, juz w 2004, wraz z zespołem, Wang wykazał, że jest ona podatna na kolizje
    #Od tego czasu powstało wiele metod ataków na MD5, które umożliwiają złamanie hasła w krótkim czasie
    #Do tego MD5 jest szybka w porównaniu do SHA-2 i SHA-3, co sprawia, że jest ona bardziej podatna na ataki brute-force

    #zad5
    testedString = "verylongstring".encode()
    print(solution.testCollision(testedString, 100000, solution.generateMD5, 3))

    #zad6
    testedString = "verylongstring".encode()
    print(solution.testSAC(testedString, solution.generateMD5, 1))






if __name__ == "__main__":
    main()