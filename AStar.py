import math
import heapq

f = open("input.txt", "r")

n = int(f.readline())
Sx, Sy = [int(x) for x in next(f).split()]
Gx, Gy = [int(x) for x in next(f).split()]
arr = [[int(x) for x in line.split()] for line in f]
visited = set()

def sqr(a):
    return a * a

# euclidean distance
def heuristic(x, y):
    return math.sqrt(sqr(Gx - x) + sqr(Gy - y))

# cells that robot can go from (x, y)
def listCellsCanGoFrom(x, y):
    ans = []
    for i in range(-1, 2):
        for j in range(-1, 2):
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
            return (ff, path)

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

def exportToFile(res, outputFile):
    fOutput = open(outputFile, "w")
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
    

res = aStar(Sx, Sy, Gx, Gy)
exportToFile(res, "output.txt")
