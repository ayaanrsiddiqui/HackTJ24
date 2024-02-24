import random

def readFile(filename):
    with open(filename) as infile:
        return infile.read()
def save(matrix,filename):
    with open(filename,'w') as outfile:
        outfile.write(str(matrix))

def temporaryMeasure():
    n = len(readFile('main/classes.txt').split())
    out = []
    for i in range(n):
        temp = []
        for j in range(n):
            temp.append(0)
        out.append(temp)
    for i in range(n):
        for j in range(i,n):
            out[i][j] = random.randint(0,100)
            out[j][i] = out[i][j]
    return out

if __name__ == '__main__':
    save(temporaryMeasure(),'main/distanceMatrix.txt')