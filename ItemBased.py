import numpy as np
import scipy.spatial.distance as sp
import operator as op
import math as m
from functions import *

#load all of my data
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

# flip dimensions
data = np.transpose(data)

# test data/test cases in list format
testRows = testData.tolist()

# calculate average rating for all users
averages = [0 for x in range(300)]
for i in range(300):
    count = 0
    avg = 0
    for j in range(1000):
        if data[j][i] != 0:
            count = count + 1
        avg = avg + data[j][i]
    averages[i] = avg / count

# calculate cosine similarity of all pairs
cosineSim = [[0 for x in range(len(data))] for y in range(len(data))]
for i in range(len(data)):
    for j in range(len(data)):
        if i == j or cosineSim[i][j] != 0:
            continue
        c = itemSimCalc(data[i],data[j],averages)
        cosineSim[i][j] = (j,c)
        cosineSim[j][i] = (i,c)
    cosineSim[i].sort(key = pearsonCompare, reverse = True)

# calculate average of k-nearest neighbors
count1 = 0
count2 = 0
output = []
for i in range(len(testRows)):
    if testRows[i][2] != 0:
    user = (testRows[i][0]- 1 - offset)
    movie = (testRows[i][1] - 1)
    weightN = 0
    weightD = 0
    for p in range(k):
        neighbor = cosineSim[user][p][0]
        neighborDifference = cosineSim[user][p][1]
        if(data[neighbor][user] != 0):
            weightN = weightN + (neighborDifference * data[neighbor][user])
            weightD = weightD + neighborDifference
        else:
            weightD = weightD + neighborDifference

    if weightN == 0:
        count1 = count + 1
        prediction = averages[user]
    else:
        prediction = (weightN / weightD)

    testRows[i][2] = int(round(prediction))
    if testRows[i][2] == 1:
        print "got a 1!"
    if testRows[i][2] < 1 or testRows[i][2] > 5:
        print "NO! " + str(testRows[i][2]) + " i: " + str(i)
        testRows[i][2] = 5
    output.append(testRows[i])

# save result file
textFile = open("itemTest5.txt","w")
for i in range(len(output)):
    textFile.write(str(output[i][0]) + " " + str(output[i][1]) + " " + str(output[i][2]) + "\n")
textFile.close()
print "got here"
