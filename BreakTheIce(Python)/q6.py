#Write a program that calculates and prints the value according to the given formula: Q = Square root of [(2 _ C _ D)/H]

#Following are the fixed values of C and H:

#C is 50. H is 30.

import math

c = 50
h = 30
result = []
n = input().split(',')

for x in n:
    result.append(str(int(round(math.sqrt((2*c*float(x))/h)))))
print(','.join(result))
