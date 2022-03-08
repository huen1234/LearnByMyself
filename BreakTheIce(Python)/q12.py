#Write a program, which will find all such numbers between 1000 and 3000 (both included) such that each digit of the number is an even number.
# The numbers obtained should be printed in a comma-separated sequence on a single line.
l = []
for x in range (1000,3001):
    x = str(x)
    if int(x[0])%2 == 0 and  int(x[1])%2 == 0 and int(x[2])%2 == 0 and int(x[3])%2 == 0:
        l.append(x)
print(",".join(l))