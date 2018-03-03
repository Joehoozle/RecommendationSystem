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

def pearsonCorrelation(a,b):
    avgA = 0
    avgB = 0
    tracker = 0
    sizeA = 0
    sizeB = 0
    if(len(a) != len(b)):
        return -2
    for i in range(0,len(a)):
        avgA = avgA + a[i]
        avgB = avgB + b[i]
    avgA = avgA / len(a)
    avgB = avgB / len(b)
    for i in range(0,len(a)):
        tracker = tracker + ((a[i] - avgA) * (b[i] - avgB))
        sizeA = sizeA + ((a[i] - avgA) ** 2)
        sizeB = sizeB + ((b[i] - avgB) ** 2)
    sim = tracker / ((sizeA ** 0.5) * (sizeB ** 0.5))
    return sim
