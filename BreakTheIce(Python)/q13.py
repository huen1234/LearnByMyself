digit = 0
alpha = 0

inx = input()
for x in inx:
    if x.isalpha():
        alpha += 1
    elif x.isdigit():
        digit +=1 
print("DIGIT ",digit)
print("ALPHA ",alpha)