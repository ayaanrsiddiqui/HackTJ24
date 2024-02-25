
import numpy.linalg

raw = open('main/ising.txt').read()[1:-2]
temp = raw.split(',')
qubo = {}
for i in range(0,len(temp),2):
    line = temp[i]+','+temp[i+1]
    key,value = line.split(':')
    qubo[eval(key)] = float(value)
print('ising extracte')
import numpy as np
out = np.zeros((7000,7000))
for i in qubo:
    out[i[0],i[1]] = qubo[i]

vals,vects = numpy.linalg.eig(out)
index = 0
for i in range(len(vals)):
    if min(vals) == vals[i]:
        index = i
        break
print(vects[i])