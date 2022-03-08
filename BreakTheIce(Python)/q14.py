upper = 0
lower = 0

inx = input()
for x in inx:
    if x.isupper():
        upper += 1
    elif x.islower():
        lower +=1 
print("UPPER ",upper)
print("LOWER ",lower)