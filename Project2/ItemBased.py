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

# put new data into a list to add to training data
newRows = [[0 for x in range(1000)] for y in range(100)]
for i in range(len(testData)):
    if testData[i][2] != 0:
        newRows[(testData[i][0] - 201 - offset)][testData[i][1]-1] = testData[i][2]

# combine full data with newly added rows
newRows = np.asarray(newRows)
data = np.vstack((data,newRows))

# flip dimensions to make movies rows and users columns
data = np.transpose(data)

# test data/test cases in list format
testRows = testData.tolist()

# calculate average rating for each user
averages = [0 for x in range(300)]
for i in range(300):
    count = 0
    avg = 0
    for j in range(1000):
        if data[j][i] != 0:
            count = count + 1
        avg = avg + data[j][i]
    averages[i] = avg / count

# calculate each rating
loading = True # flag to determine if data is being loaded
output = [] # list to keep track of calculated ratings
loadedReviews = [] # list of currently loaded initial ratings for a given new user
for i in range(len(testRows)):

    # if the rating is given, record it
    if testRows[i][2] != 0:
        if loading == False:
            # clear loaded reviews from previous new user
            del loadedReviews[:]
            loading = True
        loadedReviews.append((testRows[i][1],testRows[i][2]))
        continue;

    # make predictions on unknown data
    loading = False
    user = (testRows[i][0]- 1 - offset)
    movie = (testRows[i][1] - 1)
    cosineSim = [0 for x in range(len(loadedReviews))]

    # calculate adjusted cosine similarity between current movie and given movies
    for j in range(len(loadedReviews)):
        otherMovie = loadedReviews[j][0] - 1
        c = itemSimCalc(data[movie],data[otherMovie],averages,user)
        cosineSim[j] = (otherMovie,c)
    cosineSim.sort(key = pearsonCompare, reverse = True)

    # make prediction with known similarities
    weightN = 0 # sumation in numerator
    weightD = 0 # sumation in denominator
    for p in range(len(cosineSim)):
        neighbor = cosineSim[p][0]
        neighborDifference = cosineSim[p][1]
        if(data[neighbor][user] != 0):
            weightN = weightN + (neighborDifference * data[neighbor][user])
            weightD = weightD + neighborDifference
    prediction = (weightN / weightD)
    testRows[i][2] = int(round(prediction))
    output.append(testRows[i])

# write results to file
textFile = open("itemTest20.txt","w")
for i in range(len(output)):
    textFile.write(str(output[i][0]) + " " + str(output[i][1]) + " " + str(output[i][2]) + "\n")
textFile.close()
