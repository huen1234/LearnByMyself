num = input().split(",")
l = []
for x in num:
    if int(x,2) % 5 == 0:
        l.append(x)
print(','.join(l))
