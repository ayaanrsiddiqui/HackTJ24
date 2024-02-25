from dwave.samplers import SimulatedAnnealingSampler

def getClasses():
    with open('classes_teachers_periods.txt') as infile:
        raw = eval(infile.read())
        out = []
        for i in raw:
            line = i.split(',')
            className = line[0]
            period = int(line[2].split()[-1])
            name = line[1]
            room = int(line[-1].split()[-1])
            out.append([className,period,room,name])
    return out
def simulate(qubo,thing):
    out = 0
    for i in range(len(thing)):
        for j in range(len(thing)):
            out += qubo[(i,j)]*thing[i]*thing[j]
    return out
raw = open('main/qubo.txt').read()[1:-2]
temp = raw.split(',')
qubo = {}
for i in range(0,len(temp),2):
    line = temp[i]+','+temp[i+1]
    key,value = line.split(':')
    qubo[eval(key)] = float(value)
print('quboExtracted')
sampler = SimulatedAnnealingSampler()
sample = sampler.sample_qubo(qubo)
for i in sample.data():
    pass
x = i.sample
thingie = []
for i in x:
    thingie.append(x[i])
total = 0
classes = [0]*14*5
for i in range(len(thingie)):
    classes[i%(14*5)] += thingie[i]


schedules  = []
accClasses = getClasses()
for n in range(100):
    temp = []
    for i in range(70):
        if thingie[n*70+i]  == 1:
            temp.append(accClasses[i])
    schedules.append(temp)

with open('main/schedules.txt','w') as outfile:
    print(schedules,file=outfile)
