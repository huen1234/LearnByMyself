lst = []

while True:
    x = input()
    if len(x)==0:
        break
    lst.append(x.upper())

for line in lst:
    print(line)