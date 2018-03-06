import numpy as np
import scipy.spatial.distance as sp
import operator as op
import math as m
from functions import *

# load all of my data
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

# calculate inverse user frequency for movies
iufs = [0 for x in range(1000)]
for i in range(1000):
    reviews = 0
    for j in range(300):
        if data[j][i] != 0:
            reviews = reviews + 1
    if reviews == 0:
        print "sorry, this movie was never reviewed. We will make up a review though!"
        iufs[i] = IUF(1,301)
    else:
        iufs[i] = IUF(reviews,300)

# apply iufs to data and calculate total number of reviews for each user to be
# used with Dirichlet Smoothing
iufData =  [[0 for x in range(1000)] for y in range(300)]
for i in range(300):
    for j in range(1000):
        if data[i][j] != 0:
            iufData[i][j] = data[i][j] * iufs[j]

# calculate average rating for all users
reviewCount = [0 for x in range(300)]
averages = [0 for x in range(300)]
totalCount = 0
totalSum = 0
g = 0
for i in range(len(data)):
    userCount = 0
    userSum = 0
    for j in range(1000):
        if data[i][j] != 0:
            userCount = userCount + 1
            userSum = userSum + data[i][j]
    # only want averages from initial data
    if i < 200:
        totalCount = totalCount + userCount
        totalSum = totalSum + userSum
    if userCount == 0:
        print "NOOOOOOO " + str(i)
    reviewCount[i] = userCount
    averages[i] = userSum / userCount
g = totalSum / totalCount

# apply Dirichlet Smoothing
for i in range(300):
    averages[i] = dirichletSmooth(averages[i],reviewCount[i],g)

# calculate cosine similarity of all pairs
pearsonDiff = [[0 for x in range(len(data))] for y in range(len(data))]
for i in range(len(data)):
    for j in range(200):
        if i == j or pearsonDiff[i][j] != 0:
            continue
        c = pearsonSimCalc(iufData[i],iufData[j],averages[i],averages[j])
        c = caseAmp(c)
        pearsonDiff[i][j] = (j,c)
        pearsonDiff[j][i] = (i,c)
    pearsonDiff[i].sort(key = pearsonCompare, reverse = True)

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
        neighbor = pearsonDiff[user][p][0]
        neighborDifference = pearsonDiff[user][p][1]
        if(data[neighbor][movie] != 0):
            weightN = weightN + (neighborDifference * (data[neighbor][movie] - averages[neighbor]))
            weightD = weightD + (abs(neighborDifference))
        else:
            weightD = weightD + abs(neighborDifference)
    prediction = averages[user] + (weightN / weightD)
    testRows[i][2] = int(round(prediction))
    output.append(testRows[i])

# save result file
textFile = open("pearsonTest20.txt","w")
for i in range(len(output)):
    textFile.write(str(output[i][0]) + " " + str(output[i][1]) + " " + str(output[i][2]) + "\n")
textFile.close()
