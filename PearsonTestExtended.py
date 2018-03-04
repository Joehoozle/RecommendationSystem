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

# calculate inverse user frequency for movies
iufs = [0 for x in range(1000)]
for i in range(1000):
    reviews = 0
    for j in range(300):
        if data[j][i] != 0:
            reviews = reviews + 1
    #print "reviews: " + str(reviews)
    if reviews == 0:
        print "sorry, this movie was never reviewed. We will make up a review though!"
        iufs[i] = IUF(1,301)
    else:
        iufs[i] = IUF(reviews,300)

# apply iufs to data
iufData =  [[0 for x in range(1000)] for y in range(300)]
for i in range(300):
    for j in range(1000):
        if data[i][j] != 0:
            iufData[i][j] = data[i][j] * iufs[j]


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
textFile = open("movieWeights.txt", "w")
textFile.write(str(iufs))
textFile.close()


# calculate cosine similarity of all pairs
pearsonDiff = [[0 for x in range(len(data))] for y in range(len(data))]
for i in range(len(data)):
    for j in range(200):
        if i == j or pearsonDiff[i][j] != 0:
            continue
        c = pearsonCorrWeight(iufData[i],iufData[j],averages[i],averages[j])
        c = caseAmp(c)
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
            # weightN = weightN + (iufs[movie] * neighborDifference
            weightD = weightD + abs(neighborDifference)

    prediction = averages[user] + (weightN / weightD)
    testRows[i][2] = int(round(prediction))
    if testRows[i][2] == 1:
        print "got a 1!"
    if testRows[i][2] < 1 or testRows[i][2] > 5:
        print "NO! " + str(testRows[i][2]) + " i: " + str(i)
        testRows[i][2] = 5
    output.append(testRows[i])

print str(count1)
print str(count2)

# save result file
textFile = open("pearsonTest200.txt","w")
for i in range(len(output)):
    textFile.write(str(output[i][0]) + " " + str(output[i][1]) + " " + str(output[i][2]) + "\n")
textFile.close()
