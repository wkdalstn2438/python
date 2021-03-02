"""
import random
b = int(input())
a = []
for i in range(1, 101):
    a.append(i)
L = a[0]
R = a[99]
cnt = 1
while L <= R:
    M = (L + R) // 2
    if b == M:
        print("{}를 찾는데 {}번 탐색하였습니다.".format(a[b-1], cnt))
        break
    elif b < M:
        R = M - 1
        cnt += 1
    else:
        L = M + 1
        cnt += 1
"""
#슬라이싱
"""
#회문
a = [1,2,3,4,5,6,7]
print(a)
print(a[0:3])#[!:?]몇번째부터 몇번까지
"""
"""
a = input()
flag = 0
for i in range(len(a)//2):
    if a[i] != a[len(a)-1-i]:
        flag = 1
        break
if flag == 1:
    print("no")
else:
    print("yes")

"""
"""
#튜플 값을 바꿀 수 없는 리스트
a = [1,2,3]리스트
b = (1,2,3)튜플
print(type(a), type(b))
"""
"""
#딕셔너리 dictionary(사전형)
a = {'a' :170, 'b': 150, 'c': 200}

#a,b,c = key
#170,150,200 value
#key는 겹치면 안됨 value는 상관x
#key 값을 통해서 value값으로 접근
print(a.values())
"""

