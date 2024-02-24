from dwave.samplers import SimulatedAnnealingSampler

mutuallyExlusive = [(0,1),(1,2)]
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



for i in mutuallyExlusive:
    qubo[i] += M
sampler = SimulatedAnnealingSampler()
print(sampler.sample_qubo(qubo))