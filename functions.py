import math as m

# calculate the cosine similarity between two users
def cosineSimCalc(a,b):
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

# calculate the pearson similarity between two users
def pearsonSimCalc(a,b,avgA,avgB):
    tracker = 0
    sizeA = 0
    sizeB = 0
    if(len(a) != len(b)):
        return "Error"
    for i in range(0,len(a)):
        tracker = tracker + ((a[i] - avgA) * (b[i] - avgB))
        sizeA = sizeA + ((a[i] - avgA) ** 2)
        sizeB = sizeB + ((b[i] - avgB) ** 2)
    sim = tracker / ((sizeA ** 0.5) * (sizeB ** 0.5))
    return sim

# calculate the item-based adjusted cosine similarity
def itemSimCalc(a,b,avg):
    tracker = 0
    sizeA = 0
    sizeB = 0
    if(len(a) != len(b)):
        return "Error"
    for i in range(0,len(a)):
        tracker = tracker + ((a[i] - avg[i]) * (b[i] - avg[i]))
        sizeA = sizeA + ((a[i] - avg[i]) ** 2)
        sizeB = sizeB + ((b[i] - avg[i]) ** 2)
    sim = tracker / ((sizeA ** 0.5) * (sizeB ** 0.5))
    return sim

# comparator function for cosine similarity
def diffCompare(a):
    if type(a) == tuple:
        return a[1]
    else:
        return a

# comparator function for pearson correlation
def pearsonCompare(a):
    if type(a) == tuple:
        return abs(a[1])
    else:
        return a

# calculate the Inverse User Frequency of a movie
def IUF(reviews,users):
    if(reviews == 0):
        return 1
    result = m.log(users/reviews)
    return result

# calculate case amplification
def caseAmp(a):
    result = a * (abs(a) ** 1.5)
    return result

# calculate Dirichlet smoothing
def dirichletSmooth(r,n,g):
    left = (n / float((1 + n))) * r
    right = (1 / float((1 + n))) * g
    newR = left + right
    return newR
