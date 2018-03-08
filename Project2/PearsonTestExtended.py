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
k = 30

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
    for j in range(200):
        if data[j][i] != 0:
            reviews = reviews + 1
    if reviews == 0:
        # apply a sort of linear smoothing for iufs
        iufs[i] = IUF(1,301)
    else:
        iufs[i] = IUF(reviews,300)

# calculate variance of each movie
variance = [0 for x in range(1000)]
sumSquare = 0.0
sumTotal = 0.0
count = 0
vari = 0
mean = 0
for i in range(1000):
    for j in range(200): # only want to deal with training data
        count = count + 1
        sumTotal = sumTotal + data[j][i]
        sumSquare = sumSquare + (data[j][i] ** 2)
    mean = sumTotal/count
    vari = (sumSquare/count) - (mean ** 2)
    variance[i] = vari

# apply iufs and variance to data
adjustedData =  [[0 for x in range(1000)] for y in range(300)]
for i in range(300):
    for j in range(1000):
        if data[i][j] != 0:
            adjustedData[i][j] = data[i][j] * iufs[j] #variance[j]

# calculate average rating for all users in real data and adjusted data
reviewCount = [0 for x in range(300)]
averages = [0 for x in range(300)]
adjustedAverages = [0 for x in range(300)]
totalCount = 0
totalSum = 0
adTotalSum = 0
g = 0
adG = 0
for i in range(300):
    userCount = 0
    userSum = 0
    adUserSum = 0
    for j in range(1000):
        if data[i][j] != 0:
            userCount = userCount + 1
            userSum = userSum + data[i][j]
            adUserSum = adUserSum + adjustedData[i][j]
    # only want averages from initial data
    if i < 200:
        totalCount = totalCount + userCount
        totalSum = totalSum + userSum
        adTotalSum = adTotalSum + adUserSum
    reviewCount[i] = userCount
    averages[i] = userSum / userCount
    adjustedAverages[i] = adUserSum / userCount
g = totalSum / totalCount
adG = adTotalSum / totalCount

# apply Dirichlet Smoothing to real averages and adjusted averages
for i in range(300):
    averages[i] = dirichletSmooth(averages[i],reviewCount[i],g)
    adjustedAverages[i] = dirichletSmooth(adjustedAverages[i],reviewCount[i],adG)

# calculate cosine similarity of all pairs
pearsonDiff = [[0 for x in range(len(data))] for y in range(len(data))]
for i in range(len(data)):
    for j in range(200):
        if i == j or pearsonDiff[i][j] != 0:
            continue
        c = pearsonSimCalc(adjustedData[i],adjustedData[j],adjustedAverages[i],adjustedAverages[j])
        #c = caseAmp(c)
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
    p = 0 # make sure to not count over data
    chosen = 0 # how many data points have been accounted for
    while chosen < k and p < 199 and type(pearsonDiff[user][p]) == tuple:
        neighbor = pearsonDiff[user][p][0]
        weight = pearsonDiff[user][p][1]
        if data[neighbor][movie] == 0:
            p = p + 1
            continue
        else:
            weightN = weightN + (weight * (data[neighbor][movie] - averages[neighbor]))
            weightD = weightD + (abs(weight))
            p = p + 1
            chosen = chosen + 1
    if weightD == 0:
        prediction = averages[user]
    else:
        prediction = averages[user] + (weightN / weightD)
    # handle rounding errors
    if int(round(prediction)) < 1:
        prediction = 1
    if int(round(prediction)) > 5:
        prediction = 5
    testRows[i][2] = int(round(prediction))
    output.append(testRows[i])

# save result file
textFile = open("pearsonTest20.txt","w")
for i in range(len(output)):
    textFile.write(str(output[i][0]) + " " + str(output[i][1]) + " " + str(output[i][2]) + "\n")
textFile.close()
