def getDists():
    with open('main/distanceMatrix.txt') as infile:
        return eval(infile.read())
def getClasses():
    return [('physics',1,0),('physics',2,0),('lit',2,10)]
from dwave.samplers import SimulatedAnnealingSampler

classes = getClasses()

mutuallyExclusive = []
for i in range(len(classes)):
    for j in range(len(classes)):
        if i == j:
            continue
        if classes[i][0] == classes[j][0] or classes[i][1] == classes[j][1]:
            mutuallyExclusive.append((i,j))

classesTotal = 3
individualTotals = 2

qubo = {}
T = individualTotals
M = 500

#Normalization, essentially each student can only be in 7 classes
for i in range(classesTotal):
    for j in range(classesTotal):
        qubo[(i,j)] = M
for i in range(classesTotal):
    qubo[(i,i)] -= 2*T*M

distMat = getDists()

for i in range(len(classes)):
    for j in range(len(classes)):
        if abs(classes[i][1]-classes[j][1]) == 1:
            qubo[(i,j)] += distMat[classes[i][2]][classes[j][2]]
for i in mutuallyExclusive:
    qubo[i] += M

sampler = SimulatedAnnealingSampler()
print(sampler.sample_qubo(qubo))