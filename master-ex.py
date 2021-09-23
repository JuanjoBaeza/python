import numpy as np
import pandas as pd
from random import seed
from random import randint

a = 8
b = 3

print(a + b);
print(a/b);
print(int(a/b));

def mifuncion():
    c = "Hola"
    d = 5
    return type(c), type(d)

print(mifuncion());

count = 0
while count <= 5:
    print (count);
    count = count + 1

a = np.arange(1, 21).tolist()
print (a);

b = np.arange(0, 20).tolist()
for num in b:
    if (num % 2) == 0:
        print (num);

b = np.arange(1, 21).tolist()
for num in b:
    if (num  == 4 or num ==18):
        print (num);

b = np.arange(1, 21).tolist()
for num in b:
    if (num % 2) != 0:
        print (num);

seed(1)
for _ in range(10):
	value = randint(0, 10)
	print(value)
    
for lista in range(1,21,5):
    print('%d,%d,%d,%d,%d' % (lista,lista+1,lista+2,lista+3,lista+4))

pares = [x for x in range (1,11) if x %2 == 0]
print(pares)

