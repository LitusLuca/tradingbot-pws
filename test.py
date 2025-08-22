import numpy as np

file = open("Data files/microsoft.csv").read()
file = file.split('\n')
n = 0
for line in file: 
    n += 1
    line = line.split(',')
    if len(line) != 6:
        print(n)
print("done")