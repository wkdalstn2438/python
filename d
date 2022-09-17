import sys
from collections import deque

n = int(sys.stdin.readline())

queue = deque([num for num in range(1, n-1)])

t = 1

while len(queue) != 1:
    k = t**3 % len(queue)
    for i in range(k):
        x = queue.popleft()
        queue.append(x)
    queue.pop()
    t += 1
print(queue[0])
