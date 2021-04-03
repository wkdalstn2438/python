f = open("temp.txt", "r")

lines = f.readlines()

for line in lines:
    temp = line.split(',')
    temp[1] = temp[1].split('\n')[0]
    print(temp)

c = []
c.append(input())
c.append(input())
if c == temp:
    print("success")
else:
    print("fail")

print(c)

