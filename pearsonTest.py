import numpy as np
import scipy.spatial.distance as sp
import operator as op
import math as m
from functions import *

#load all of my data
data = np.loadtxt("train.txt", delimiter="\t")
testData = np.loadtxt("test20.txt", dtype=int)

# offset depending on test size as user ids need to be normalized
offset = 200

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

# calculate average rating for all users
averages = [0 for x in range(300)]
for i in range(len(data)):
    count = 0
    avg = 0
    for j in range(1000):
        if data[i][j] != 0:
            count = count + 1
        avg = avg + data[i][j]
    averages[i] = avg / count


# save Pearson Correlation similarity
textFile = open("averages.txt", "w")
textFile.write(str(averages))
textFile.close()


# calculate cosine similarity of all pairs
pearsonDiff = [[0 for x in range(len(data))] for y in range(len(data))]
for i in range(len(data)):
    for j in range(200):
        if i == j or pearsonDiff[i][j] != 0:
            continue
        c = pearsonCorrWeight(data[i],data[j],averages[i],averages[j])
        pearsonDiff[i][j] = (j,c)
        pearsonDiff[j][i] = (i,c)
    pearsonDiff[i].sort(key = pearsonCompare, reverse = True)

# calculate average of k-nearest neighbors
count1 = 0
count2 = 0
output = []
for i in range(len(testRows)):
    if(testRows[i][2] != 0):
        continue
    user = (testRows[i][0]- 1 - offset)
    movie = (testRows[i][1] - 1)
    weightN = 0
    weightD = 0
    for p in range(k):
        neighbor = pearsonDiff[user][p][0]
        neighborDifference = pearsonDiff[user][p][1]
        if(data[neighbor][movie] != 0):
            weightN = weightN + (neighborDifference * (data[neighbor][movie] - averages[neighbor]))
            weightD = weightD + (abs(neighborDifference))
        else:
        #     weightN = weightN + (neighborDifference * (dataint(round(averages[neighbor]))))
            weightD = weightD + (abs(neighborDifference))

    prediction = averages[user] + (weightN / weightD)
    testRows[i][2] = int(round(prediction))
    if(testRows[i][2] == 3):
        count1 = count1 + 1
    else:
        count2 = count2 + 1
    output.append(testRows[i])
print str(count1)
print str(count2)

# save result file
textFile = open("pearsonTest20.txt","w")
for i in range(len(output)):
    textFile.write(str(output[i][0]) + " " + str(output[i][1]) + " " + str(output[i][2]) + "\n")
textFile.close()
