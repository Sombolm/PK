import random
import string
import numpy as np
import Solution
import matplotlib.pyplot as plt

def generateFilesOfSizes(fileSizes):
    for i in range(len(fileSizes)):
        yield generateRandomFileOfSizeInMB(fileSizes[i])

def printLine():
    print("-------------------------------------------------")

def loadFile(fileName: str):
    with open(fileName, "r") as f:
        return f.read()

def generateRandomFileOfSizeInMB(size: int):
    size_in_bytes = size * 1024 * 1024
    content = ''.join(random.choices(string.ascii_letters + string.digits, k=size_in_bytes))
    with open(str(size) + ".txt", 'w') as f:
        f.write(content)

    f.close()
    return str(size) + ".txt"


def plotTimes(times_list: list[dict]):
    plt.figure(figsize=(12, 7))  # Bigger figure for main plot
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']  # Colors for different functions
    markers = ['o', 's', 'D', '^', 'v', 'p', '*']  # Different markers for functions
    function_map = {}  # Map function names to colors & markers
    file_sizes = set()  # Store unique file sizes

    for times in times_list:
        for (hash_type, file_size, function_name), time_ns in times.items():
            file_sizes.add(int(file_size.rstrip('.txt')))  # Collect unique file sizes
            if function_name not in function_map:
                function_map[function_name] = (colors[len(function_map) % len(colors)],
                                               markers[len(function_map) % len(markers)])

    file_sizes = sorted(file_sizes)  # Sort file sizes for consistency

    ### MAIN PLOT (All file sizes together) ###
    plt.figure(figsize=(12, 7))
    for function_name, (color, marker) in function_map.items():
        x = []
        y = []
        for times in times_list:
            for (hash_type, file_size, func), time_ns in times.items():
                if func == function_name:
                    x.append(int(file_size.rstrip('.txt')))
                    y.append(time_ns)

        sorted_pairs = sorted(zip(x, y))
        x_sorted, y_sorted = zip(*sorted_pairs)

        plt.plot(x_sorted, y_sorted, marker=marker, markersize=8, linestyle='-', linewidth=2,
                 color=color, label=function_name)

    plt.xlabel("File size in MB", fontsize=14)
    plt.ylabel("Time in ns", fontsize=14)
    plt.title("Time of hashing for different file sizes and functions", fontsize=16)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=12)
    plt.grid(True, linestyle='--', linewidth=0.7, alpha=0.6)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    plt.show()

    ### SEPARATE PLOTS FOR EACH FILE SIZE ###
    fig, axes = plt.subplots(len(file_sizes), 1, figsize=(10, 5 * len(file_sizes)))

    if len(file_sizes) == 1:
        axes = [axes]  # Ensure axes is iterable if only one subplot

    for ax, file_size in zip(axes, file_sizes):
        for function_name, (color, marker) in function_map.items():
            x = []
            y = []
            for times in times_list:
                for (hash_type, f_size, func), time_ns in times.items():
                    if func == function_name and int(f_size.rstrip('.txt')) == file_size:
                        x.append(int(f_size.rstrip('.txt')))
                        y.append(time_ns)

            if x and y:
                ax.plot(x, y, marker=marker, markersize=8, linestyle='-', linewidth=2,
                        color=color, label=function_name)

        ax.set_xlabel("File size in MB", fontsize=12)
        ax.set_ylabel("Time in ns", fontsize=12)
        ax.set_title(f"Time of hashing for file size {file_size} MB", fontsize=14)
        ax.legend(fontsize=10)
        ax.grid(True, linestyle='--', linewidth=0.7, alpha=0.6)

    plt.tight_layout()
    plt.show()

def runSprawozdanie():
    solution = Solution.Solution()
    '''
    sizes = [150,200,250]
    fileNames = generateFilesOfSizes(sizes)
    
    print(fileNames)
    for fileNames in fileNames:
        print(fileNames)
    print("Files generated")
    
    #zad1
    
    timeList = []
    for fileName in fileNames:
        file = open(fileName, "r")
        text = file.read()
        _, times = solution.generateAll(text, fileName.lstrip(".txt"))
        timeList.append(times)
        printLine()

    plotTimes(timeList)
    
    smallText = loadFile(str(sizes[0]) + ".txt")
    

    #zad2
    print('SAC for small text')
    res = solution.testSAC(smallText.encode(), solution.generateSHA3Digest, 1)
    print('Bits changed with probability: ', res[0])
    '''
    smallText = "ko"
    #zad3
    print("Collision test for small text")
    res = solution.testCollision(smallText.encode(), 1000 , solution.generateMD5Digest, 2)
    print('Number of collisions in first 16 bits: ', res)
    printLine()
    res =solution.testCollision(smallText.encode(), 1000, solution.generateMD5Digest, 3)
    print('Number of collisions in first 24 bits: ', res)
    printLine()
    res =solution.testCollision(smallText.encode(), 1000, solution.generateMD5Digest, 4)
    print('Number of collisions in first 32 bits: ', res)
    printLine()

def main():
    runSprawozdanie()
    return

if __name__ == "__main__":
    main()