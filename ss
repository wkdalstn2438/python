a = int(input())
count = 0
none = -1
for i in range(a):
    b = list(map(int, input().split()))
    c = b
    b.sort()
    e = c.index(b[0])
    print(e, none)
    if e == none:
        count += b[1]
        e = 1
        print(1)
    else:
        count += b[0]
        none = e
        print(2)
    print(count)
