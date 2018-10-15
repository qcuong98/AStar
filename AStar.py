import math
import heapq

f = open("input.txt", "r")

n = int(f.readline())
Sx, Sy = [int(x) for x in next(f).split()]
Gx, Gy = [int(x) for x in next(f).split()]
arr = [[int(x) for x in line.split()] for line in f]

def sqr(a):
    return a * a

# euclidean distance
def heuristic(x, y):
    return math.sqrt(sqr(Gx - x) + sqr(Gy - y))

def aStar(Sx, Sy, Gx, Gy, arr):
    return -1

print(n)
print(Sx, Sy)
print(Gx, Gy)
print(arr)
print(heuristic(3, 5))
