import numpy as np

pearsonData5 = np.loadtxt("pearsonTest5.txt", delimiter=" ")
itemData5 = np.loadtxt("itemTest5.txt", dtype=int)
cosineData5 = np.loadtxt("cosineTest5.txt", dtype =int)
pearsonData10 = np.loadtxt("pearsonTest10.txt", delimiter=" ")
itemData10 = np.loadtxt("itemTest10.txt", dtype=int)
cosineData10 = np.loadtxt("cosineTest10.txt", dtype =int)
pearsonData20 = np.loadtxt("pearsonTest20.txt", delimiter=" ")
itemData20 = np.loadtxt("itemTest20.txt", dtype=int)
cosineData20 = np.loadtxt("cosineTest20.txt", dtype =int)




pearsonData5 = pearsonData5.tolist()
itemData5 = itemData5.tolist()
cosineData5 = cosineData5.tolist()
pearsonData10 = pearsonData10.tolist()
itemData10 = itemData10.tolist()
cosineData10 = cosineData10.tolist()
pearsonData20 = pearsonData20.tolist()
itemData20 = itemData20.tolist()
cosineData20 = cosineData20.tolist()

output5 = []
output10 = []
output20 = []
value = 0.0
for i in range(len(pearsonData5)):
    value = (0.7 * pearsonData5[i][2] + 0.3 * itemData5[i][2]) / 2
    value = (value + cosineData5[i][2]) / 2
    value = int(round(value))
    output5.append((pearsonData5[i][0], pearsonData5[i][1], value))

for i in range(len(pearsonData10)):
    value = (0.7 * pearsonData10[i][2] + 0.3 * itemData10[i][2]) / 2
    value = (value + cosineData10[i][2]) / 2
    value = int(round(value))
    output10.append((pearsonData10[i][0], pearsonData10[i][1], value))

for i in range(len(pearsonData20)):
    value = (0.7 * pearsonData20[i][2] + 0.3 * itemData20[i][2]) / 2
    value = (value + cosineData20[i][2]) / 2
    value = int(round(value))
    output20.append((pearsonData20[i][0], pearsonData20[i][1], value))


textFile = open("itemPearson5.txt","w")
for i in range(len(output5)):
    textFile.write(str(output5[i][0]) + " " + str(output5[i][1]) + " " + str(output5[i][2]) + "\n")
textFile.close()

textFile = open("itemPearson10.txt","w")
for i in range(len(output10)):
    textFile.write(str(output10[i][0]) + " " + str(output10[i][1]) + " " + str(output10[i][2]) + "\n")
textFile.close()

textFile = open("itemPearson20.txt","w")
for i in range(len(output20)):
    textFile.write(str(output20[i][0]) + " " + str(output20[i][1]) + " " + str(output20[i][2]) + "\n")
textFile.close()
