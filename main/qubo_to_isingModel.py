import dimod
raw = open('main/qubo.txt').read()[1:-2]
temp = raw.split(',')
qubo = {}
for i in range(0,len(temp),2):
    line = temp[i]+','+temp[i+1]
    key,value = line.split(':')
    qubo[eval(key)] = float(value)
print('quboExtracted')

ising =  dimod.qubo_to_ising(qubo)
with open('main/ising.txt','w') as outfile:
    print(qubo,file=outfile)
