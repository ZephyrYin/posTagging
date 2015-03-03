__author__ = 'zephyryin'

import Queue
import nltk
from nltk.corpus import treebank

def printMatrix(M):
    for m in M:
        print(m)

def saveConfusionMatrix(conM, tList):              # write the confusion matrix to local confusionMatrix.txt
    wordLen = 6
    file = open('confusionMatrix.txt', 'w')
    for i in range(wordLen):
        file.write(' ')

    for w in tList:
        file.write(' ')
        file.write(w)
        for i in range(wordLen - len(w)):
            file.write(' ')
    file.write('\n')

    for y in range(len(tList)):
        file.write(tList[y])
        for i in range(wordLen - len(tList[y])):
            file.write(' ')
        for x in range(len(tList)):
            file.write(' ')
            file.write(str(conM[y][x]))
            for i in range(wordLen - len(str(conM[y][x]))):
                file.write(' ')
        file.write('\n')

    file.close()

def saveAccuracy(accuList, overallAcu):
    wordLen = 6
    file = open('accuracy.txt', 'w')
    file.write('overall accuracy: ' + str(overallAcu) + '\n')
    for l in accuList:
        file.write(str(l[1]))
        for i in range(wordLen - len(str(l[1]))):
            file.write(' ')
        file.write(' ' + str(l[0]) + '\n')
    file.close()

size = 500
maxTagSize = 50
trainSet = treebank.tagged_sents()[0:size]
taggedTestSet = treebank.tagged_sents()[size:(size + size)]
testSet = treebank.sents()[size:(size + size)]

t0 = nltk.DefaultTagger('NN')                               # train
t1 = nltk.UnigramTagger(trainSet, backoff=t0)
t2 = nltk.BigramTagger(trainSet, backoff=t1)

wordCnt = 0
predictions = []
dict = {}
confutionMatrix = [[0 for col in range(maxTagSize)] for row in range(maxTagSize)]
tagList = []

file = open('part-I-predictions.txt', 'w')

for i in range(500):
    prediction = t2.tag(testSet[i])
    contrastResult = [i, taggedTestSet[i], prediction]
    predictions.append(contrastResult)
    #writeOneRecord(file, contrastResult)

    file.write(str(i))
    file.write('\t')
    for j in range(1, len(contrastResult)):
        for k in range(len(contrastResult[j])):
            if k > 0:
                file.write(' ')
            word = contrastResult[j][k]

            if j == 2:
                wordCnt = wordCnt + 1
                actualTag = contrastResult[1][k][1]
                predictTag = contrastResult[2][k][1]
                if not actualTag in tagList:
                    tagList.append(actualTag)
                if not predictTag in tagList:
                    tagList.append(predictTag)

                y = tagList.index(actualTag)
                x = tagList.index(predictTag)
                confutionMatrix[y][x] = confutionMatrix[y][x] + 1

            file.write(word[0] + '/' + word[1])
        file.write('\t')
    file.write('\n')
file.close()

# compute accuracy based on the confusion matrix

accurateQ = Queue.PriorityQueue()
accurateList = []
accuratePredictCnt = 0

for y in range(len(tagList)):
    accuratePredictCnt = accuratePredictCnt + confutionMatrix[y][y]
    accurateQ.put((float(confutionMatrix[y][y]) / float(sum(confutionMatrix[y])), tagList[y]))

overallAccuracy = float(accuratePredictCnt) / float(wordCnt)

print('words: ' + str(wordCnt) + '\n\n')
print('right tag cnt: ' + str(accuratePredictCnt) + '\n')
print('overallAccuraty: ' + str(overallAccuracy))
while not accurateQ.empty():
    accurateList.append(accurateQ.get())
accurateList.reverse()

saveConfusionMatrix(confutionMatrix, tagList)
saveAccuracy(accurateList, overallAccuracy)







