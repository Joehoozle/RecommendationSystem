import numpy as np
import operator as op
from functions import *
data = np.loadtxt("train.txt", delimiter="\t")
cosDiff = [[0 for x in range(300) for y in range(300)]
pearDiff = [[0 for x in range(300)] for y in range(300)]
for i in range(0,len(data)):
    for j in range(i,len(data)):
        if i == j or cosDiff[i][j] != 0:
            continue
        c = cosineSim(data[i],data[j])
        p = pearsonCorrelation(data[i],data[j])
        cosDiff[i][j] = (j,c)
        cosDiff[j][i] = (i,c)
        pearDiff[i][j] = (j,p)
        pearDiff[j][i] = (i,p)

for i in range(0,len(data)):
    cosDiff[i].sort(key = diffCompare, reverse = True)
    pearDiff[i].sort(key = diffCompare, reverse = True)

textFile = open("cosineSim.txt","w")
textFile.write(str(cosDiff))
textFile.close()

textFile = open("pearsonCorrelation.txt", "w")
textFile.write(str(pearDiff))
textFile.close()
