import math
import heapq
import sys

n = 0
(Sx, Sy) = (0, 0)
(Gx, Gy) = (0, 0)
arr = []
visited = set()
orderNeighbors = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]

def readArguments():
    if (len(sys.argv) != 3):
        print("1612843_1612869_Lab01.exe <input_file_directory> <output_file_directory>")
        exit()
    return (sys.argv[1], sys.argv[2])

def importFromFile(inputDir):
    global n
    global Sx
    global Sy
    global Gx
    global Gy
    global arr
     
    fInput = open(inputDir, "r")

    n = int(fInput.readline())
    Sx, Sy = [int(x) for x in next(fInput).split()]
    Gx, Gy = [int(x) for x in next(fInput).split()]
    arr = [[int(x) for x in line.split()] for line in fInput]

def sqr(a):
    return a * a

# euclidean distance
def heuristic(x, y):
    return math.sqrt(sqr(Gx - x) + sqr(Gy - y))

# cells that robot can go from (x, y)
def listCellsCanGoFrom(x, y):
    ans = []

    for (i, j) in orderNeighbors:
            (u, v) = (x + i, y + j)
            if (u in range(n)) and (v in range(n)) and \
               (arr[u][v] != 1) and ((u, v) not in visited):
                ans.append((u, v))
    return ans
                
def aStar(Sx, Sy, Gx, Gy):
    g = [x[:] for x in [[float("inf")] * n] * n]  
    h = [x[:] for x in [[0] * n] * n]  
    f = [x[:] for x in [[0] * n] * n] 
    tr = [x[:] for x in [[(0, 0)] * n] * n]   

    g[Sx][Sy] = 0
    for i in range(n):
        for j in range(n):
            h[i][j] = heuristic(i, j)
            f[i][j] = g[i][j] + h[i][j]

    heap = [(f[Sx][Sy], Sx, Sy)]
    heapq.heapify(heap)

    while (len(heap) != 0):
        (ff, x, y) = heapq.heappop(heap)

        if (x, y) == (Gx, Gy):
            path = []
            while (x, y) != (Sx, Sy):
                path.append((x, y))
                (x, y) = tr[x][y]
            path.append((Sx, Sy))
            path.reverse()
            return (ff + 1, path)

        if (x, y) not in visited:
            visited.add((x, y))

            listNextCells = listCellsCanGoFrom(x, y)
            for (u, v) in listNextCells:
                cost = g[x][y] + 1 
                if (cost < g[u][v]):
                    tr[u][v] = (x, y)
                    g[u][v] = cost
                    f[u][v] = cost + h[u][v]
                    heapq.heappush(heap, (f[u][v], u, v))
    
    return (-1, [])

def exportToFile(res, outputDir):
    fOutput = open(outputDir, "w")
    (len_path, path) = res

    if (len_path == -1):
        fOutput.write("-1")
        return

    ans = arr[:]
    for i in range(n):
        for j in range(n):
            if (ans[i][j] == 0):
                ans[i][j] = '-'
            elif (ans[i][j] == 1):
                ans[i][j] = 'o'
    for (x, y) in path:
        ans[x][y] = 'x'
    ans[Sx][Sy] = 'S'
    ans[Gx][Gy] = 'G'

    fOutput.write(str(int(len_path)))
    fOutput.write("\n")
    for (x, y) in path:
        fOutput.write("(" + str(x) + "," + str(y) + ") ")
    fOutput.write("\n")
    for i in range(n):
        for j in range(n):
            fOutput.write(ans[i][j] + " ")
        fOutput.write("\n")

    fOutput.close()

(inputDir, outputDir) = readArguments()
importFromFile(inputDir)
res = aStar(Sx, Sy, Gx, Gy)
exportToFile(res, outputDir)
