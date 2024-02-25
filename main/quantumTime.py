def getDists():
    with open('main/distanceMatrix.txt') as infile:
        return eval(infile.read())
def getClasses():
    with open('main/classes_teachers_periods.txt') as infile:
        raw = eval(infile.read())
        out = []
        for i in raw:
            line = i.split()
            className = line[0]
            period = int(line[-1])
            name = ''.join(line[1:-2])
            out.append([className,period,0])
    return out

from dwave.samplers import SimulatedAnnealingSampler

classes = getClasses()
classesTotal = len(classes)
courseRequests = ['physics','lit']

mutuallyExclusive = []
for i in range(len(classes)):
    for j in range(len(classes)):
        if i == j:
            continue
        if classes[i][0] == classes[j][0] or classes[i][1] == classes[j][1]:
            mutuallyExclusive.append((i,j))


numStudents = 1
individualTotals = 7
qubo = {}
T = individualTotals
M = 500
R = 20 #Reward for matched class

#Normalization, essentially each student can only be in 7 classes
for i in range(classesTotal):
    for j in range(classesTotal):
        qubo[(i,j)] = M
for i in range(classesTotal):
    qubo[(i,i)] -= 2*T*M
    if classes[i][0] in courseRequests:
        qubo[(i,i)] -= R

distMat = getDists()

for i in range(len(classes)):
    for j in range(len(classes)):
        if abs(classes[i][1]-classes[j][1]) == 1:
            qubo[(i,j)] += distMat[classes[i][2]][classes[j][2]]
for i in mutuallyExclusive:
    qubo[i] += M
for i in qubo:
    if qubo[i] < 0 and i[0] != i[1]:
        print(i,qubo[i])

sampler = SimulatedAnnealingSampler()
x = sampler.sample_qubo(qubo)
for i in x.data():
    pass
x = i.sample
for i in x:
    if x[i] == 1:
        print(classes[i])