def getDists():
    with open('main/distanceMatrix.txt') as infile:
        return eval(infile.read())

def getClasses():
    with open('main/classes_teachers_periods.txt') as infile:
        raw = eval(infile.read())
        out = []
        for i in raw:
            line = i.split(',')
            className = line[0]
            period = int(line[2].split()[-1])
            name = line[1]
            room = int(line[-1].split()[-1])
            out.append([className,period,room])
    return out


classes = getClasses()
print(len(classes))
classesTotal = len(classes)
actualClasses = {i[0] for i in classes}
courseRequests = [['physics','lit'],[]*10]

mutuallyExclusive = []
for i in range(len(classes)):
    for j in range(len(classes)):
        if i == j:
            continue
        if classes[i][0] == classes[j][0] or classes[i][1] == classes[j][1]:
            mutuallyExclusive.append((i,j))
print('mutually excluded')

numStudents = 100
individualTotals = 7
qubo = {}
T = individualTotals
M = 500000
R = 20 #Reward for matched class
#Normalization, essentially each student can only be in 7 classes
for n in range(numStudents):
    for i in range(classesTotal):
        for j in range(classesTotal):
            qubo[(n*classesTotal+i,n*classesTotal+j)] = M**2
    for i in range(classesTotal):
        qubo[(n*classesTotal+i,n*classesTotal+i)] -= 2*T*M**2
        if classes[i][0] in courseRequests:
            qubo[(n*classesTotal+i,n*classesTotal+i)] -= R
print('normalized')

#Only so many in a class
classLimit = 10
for i in range(classesTotal*numStudents):
    for j in range(classesTotal*numStudents):
        if i%classesTotal == j%classesTotal:
            if (i,j) not in qubo: qubo[(i,j)] = 0
            qubo[(i,j)] += M
        if i == j:
            qubo[(i,i)] -= 2*classLimit*M
print('out classed')

distMat = getDists()

for n in range(numStudents):
    for i in range(len(classes)):
        for j in range(len(classes)):
            if abs(classes[i][1]-classes[j][1]) == 1:
                qubo[(n*classesTotal+i,n*classesTotal+j)] += distMat[classes[i][2]][classes[j][2]]
    for i in mutuallyExclusive:
        qubo[(n*classesTotal+i[0],n*classesTotal+i[1])] += M
    for i in qubo:
        if qubo[i] < 0 and i[0] != i[1]:
            print(i,qubo[i])
print('distant')
print('done?')
with open('main/qubo.txt','w') as outfile:
    print(qubo,file=outfile)
print('done')