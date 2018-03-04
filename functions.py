import math as m

def cosineDiff(a,b):
    tracker = 0
    sizeA = 0
    sizeB = 0
    if(len(a) != len(b)):
        return "Error"
    for i in range(0,len(a)):
        tracker = tracker + (a[i] * b[i])
        sizeA = sizeA + (a[i] ** 2)
        sizeB = sizeB + (b[i] ** 2)
    sim = tracker / ((sizeA ** 0.5) * (sizeB ** 0.5))
    return sim

def diffCompare(a):
    if type(a) == tuple:
        return a[1]
    else:
        return a

def pearsonCorrWeight(a,b,avgA,avgB):
    tracker = 0
    sizeA = 0
    sizeB = 0
    if(len(a) != len(b)):
        return -2
    for i in range(0,len(a)):
        tracker = tracker + ((a[i] - avgA) * (b[i] - avgB))
        sizeA = sizeA + ((a[i] - avgA) ** 2)
        sizeB = sizeB + ((b[i] - avgB) ** 2)
    sim = tracker / ((sizeA ** 0.5) * (sizeB ** 0.5))
    return sim


def pearsonCompare(a):
    if type(a) == tuple:
        return abs(a[1])
    else:
        return a

def IUF(reviews,users):
    if(reviews == 0):
        return 1
    result = m.log(users/reviews)
    return result

def caseAmp(a):
    result = a * (abs(a) ** 1.5)
    return result
