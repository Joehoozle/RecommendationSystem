import numpy as np
import scipy.spatial.distance as sp
import operator as op
import math as m
from functions import *

# load all of my data
data = np.loadtxt("train.txt", delimiter="\t")
testData = np.loadtxt("test5.txt", dtype=int)

# offset depending on test size as user ids need to be normalized
offset = 0

# this is how many neighbors I need
k = 5

# put new data into a list
newRows = [[0 for x in range(1000)] for y in range(100)]
for i in range(len(testData)):
    if testData[i][2] != 0:
        newRows[(testData[i][0] - 201 - offset)][testData[i][1]-1] = testData[i][2]

# combine full data with added new rows
newRows = np.asarray(newRows)
data = np.vstack((data,newRows))

# test data/test cases in list format
testRows = testData.tolist()

# calculate cosine similarity of all pairs
cosSim = [[0 for x in range(len(data))] for y in range(len(data))]
for i in range(len(data)):
    for j in range(200):
        if i == j or cosSim[i][j] != 0:
            continue
        c = cosineSimCalc(data[i],data[j])
        cosSim[i][j] = (j,c)
        cosSim[j][i] = (i,c)
    cosSim[i].sort(key = diffCompare, reverse = True)

# calculate average of k-nearest neighbors
output = []
for i in range(len(testRows)):
    if(testRows[i][2] != 0):
        continue
    user = (testRows[i][0]- 1 - offset)
    movie = (testRows[i][1] - 1)
    weightN = 0
    weightD = 0
    for p in range(k):
        neighbor = cosSim[user][p][0]
        neighborDifference = cosSim[user][p][1]
        if(data[neighbor][movie] != 0):
            weightN = weightN + (data[neighbor][movie] * neighborDifference)
            weightD = weightD + (neighborDifference)
        else:
            weightN = weightN + (3 * neighborDifference)
            weightD = weightD + (neighborDifference)

    prediction = weightN / weightD
    testRows[i][2] = int(round(prediction))
    output.append(testRows[i])

# save edited
textFile = open("cosineTest5.txt","w")
for i in range(len(output)):
    textFile.write(str(output[i][0]) + " " + str(output[i][1]) + " " + str(output[i][2]) + "\n")
textFile.close()
