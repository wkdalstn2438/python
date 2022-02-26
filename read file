from glob import glob

files = glob("*.txt")
count = 0
for file in files:
    f = open("{}".format(str(files[count])), 'r', encoding='cp949')
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        temp = line.split(' : ')
        print(temp)
    count += 1
