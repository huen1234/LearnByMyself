result = []
row,col = input().split(',')
for x in range(0,int(row)):
    tmp = []
    for y in range(0,int(col)):
        tmp.append(x*y)
    result.append(tmp)
print(result)

