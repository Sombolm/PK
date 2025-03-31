from collections import defaultdict

class Tests:
    def __init__(self, bits: list):
        self.acceptableRanges = {
            1: (2315, 2685),
            2: (1114, 1386),
            3: (527, 723),
            4: (240, 384),
            5: (103, 209),
            6: (103, 209),
        }
        self.groupSize = 4
        self.bits = bits
        self.tests = [self.singleBitTest, self.seriesTest, self.longSeriesTest, self.pokerTest]

    def runTests(self) -> None:
        print("")
        flag = True
        for test in self.tests:
            print("Running test:", test.__name__)
            if not test():
                flag = False
                print("Test failed")
            else:
                print("Test passed")
            print("")
        if flag:
            print("All tests passed!")
    #sprawdza czy liczba jedynek jest w odpowiednim przedziale
    def singleBitTest(self) -> bool:
        return 9654 < self.bits.count(1) < 10346

    #sprawdza czy liczba serii jedynek i zer jest w odpowiednich przedziałach (mowi o losowosci)
    def seriesTest(self) -> bool:
        seriesOnesCount = defaultdict(int)
        seriesZeroesCount = defaultdict(int)

        def addValueToDict(number: int, seriesLength: int) -> None:
            if number == 1:
                seriesOnesCount[seriesLength] += 1
            else:
                seriesZeroesCount[seriesLength] += 1

        def checkAcceptableRanges(seriesOnesCount: dict, seriesZeroesCount: dict) -> bool:
            for key in range(1, 6):
                if not self.acceptableRanges[key][0] <= seriesOnesCount[key] <= self.acceptableRanges[key][1]:
                    print("Failed on ones for key =>", key)
                    return False
                if not self.acceptableRanges[key][0] <= seriesZeroesCount[key] <= self.acceptableRanges[key][1]:
                    print("Failed on zeroes for key =>", key)
                    return False

            sumCount = 0
            for key in range(6, max(seriesOnesCount.keys())):
                sumCount += seriesOnesCount[key]
            if not self.acceptableRanges[6][0] <= sumCount <= self.acceptableRanges[6][1]:
                print("Failed on ones for key => 6")
                return False

            sumCount = 0
            for key in range(6, max(seriesZeroesCount.keys())):
                sumCount += seriesZeroesCount[key]
            if not self.acceptableRanges[6][0] <= sumCount <= self.acceptableRanges[6][1]:
                print("Failed on zeroes for key => 6")
                return False
            return True

        prev = self.bits[0]
        seriesLength = 1
        for bit in self.bits[1:]:
            if bit == prev:
                seriesLength += 1
            else:
                addValueToDict(prev, seriesLength)
                seriesLength = 1
            prev = bit
        addValueToDict(prev, seriesLength)

        print("Ones series count:", seriesOnesCount)
        print("Zeroes series count:", seriesZeroesCount)

        if not checkAcceptableRanges(seriesOnesCount, seriesZeroesCount):
            return False
        return True

    #sprawdza czy nie ma serii dluzszej niz 26
    def longSeriesTest(self) -> bool:
        prev = self.bits[0]
        seriesLength = 1
        for bit in self.bits[1:]:
            if bit == prev:
                seriesLength += 1
                if seriesLength == 26:
                    return False
            else:
                seriesLength = 1
            prev = bit

        return True

    #sprawdza czy ciag bitow jest losowy na podstawie wystapienia poszczegolnych n bitowych serii
    #sprawdza liczbe wystapien wszystkich mozliwych segmentow o danej dlugosci
    def pokerTest(self) -> bool:
        def splitBitsIntoGroups() -> list:
            return [self.bits[i:i + self.groupSize] for i in range(0, len(self.bits), self.groupSize)]

        def countBitsGroups(groups: list) -> dict:
            count = defaultdict(int)
            for group in groups:
                count[tuple(group)] += 1
            return count

        def calculateX(count: dict) -> float:
            return 16/5000 * sum([value**2 for value in count.values()]) - 5000

        count = countBitsGroups(splitBitsIntoGroups())
        x = calculateX(count)
        print("X value:", x)

        return 2.16 < x < 46.17
