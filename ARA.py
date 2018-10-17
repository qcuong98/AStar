import math
import heapq

fi = open("input.txt", "r")

n = int(fi.readline())
Sx, Sy = [int(x) for x in next(fi).split()]
Gx, Gy = [int(x) for x in next(fi).split()]
arr = [[int(x) for x in line.split()] for line in fi]

closed = set()
open_queue = []
incons = set()

g = {}
tr = {}

# cells that robot can go from (x, y)
def listCellsCanGoFrom(x, y):
    ans = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            (u, v) = (x + i, y + j)
            if (u in range(n)) and (v in range(n)) and (arr[u][v] != 1):
                ans.append((u, v))
    return ans

# new heuristic
def heuristic(x, y):
    return max(abs(Gx - x), abs(Gy - y))

def f_value(x, y, e):
    return g[(x,y)] + e * heuristic(x, y)

def improvePath(e):
    global open_queue
    global incons
    global closed
    global tr
    global g

    while (len(open_queue) != 0):
        (ff, x, y) = heapq.heappop(open_queue)

        if (g[(Gx, Gy)] <= ff):
            heapq.heappush(open_queue, (ff, x, y))
            break

        # if ((x, y) not in closed):
        closed.add((x, y))

        listNextCells = listCellsCanGoFrom(x, y)
        for (u, v) in listNextCells:
            if ((u, v) not in g):
                g[(u, v)] = float("inf")

            cost = g[(x, y)] + 1
            if (cost < g[(u, v)]):
                tr[(u, v)] = (x, y)
                g[(u, v)] = cost
                if ((u, v) not in closed):
                    heapq.heappush(open_queue, (f_value(u, v, e), u, v))
                else:
                    incons.add((u, v))

def moveFromOpenToIncons():
    while (len(open_queue) != 0):
        (ff, x, y) = heapq.heappop(open_queue)
        incons.add((x, y))

    min_g_h = float("inf")

    for (x, y) in incons:
        # print(x, y)
        min_g_h = min(min_g_h, g[(x, y)] + heuristic(x, y))
    # print()

    if (min_g_h == float("inf")):
        return 0
    else:
        return min_g_h

def updateFValue(e):
    while (len(incons) != 0):
        (x, y) = incons.pop()
        heapq.heappush(open_queue, (f_value(x, y, e), x, y))
    print(open_queue)


eps = 0.01
                
def ARA():
    global g
    global open_queue
    global closed

    g = {(Sx, Sy): 0, (Gx, Gy): float("inf")}
    e = 100
    heapq.heappush(open_queue, (f_value(Sx, Sy, e), Sx, Sy))

    while (e >= 1):
        improvePath(e)
        min_g_h = moveFromOpenToIncons()
        closed = set()

        if (min_g_h != 0):
            e = min(e, g[(Gx, Gy)] / (1.0 * min_g_h))
        ans = e
        e -= eps

        updateFValue(e)

    return ans

print(ARA())
