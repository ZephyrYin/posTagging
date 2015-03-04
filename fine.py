__author__ = 'zephyryin'

import Queue
import function
import nltk
from nltk.corpus import treebank

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

file = open('part-I-predictions.tsv', 'w')

for i in range(size):
    prediction = t2.tag(testSet[i])
    contrastResult = [i, taggedTestSet[i], prediction]
    predictions.append(contrastResult)

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
print('preditions saved in part-I-predictions.tsv')

# compute accuracy based on the confusion matrix

accurateQ = Queue.PriorityQueue()
accurateList = []
accuratePredictCnt = 0

for y in range(len(tagList)):
    accuratePredictCnt = accuratePredictCnt + confutionMatrix[y][y]
    accurateQ.put((100.0 * float(confutionMatrix[y][y]) / float(sum(confutionMatrix[y])), tagList[y]))

overallAccuracy = 100.0 * float(accuratePredictCnt) / float(wordCnt)

while not accurateQ.empty():
    accurateList.append(accurateQ.get())
accurateList.reverse()

function.saveConfusionMatrix(confutionMatrix, tagList, 'part-I-confusionMatrix.txt')
function.saveAccuracy(accurateList, overallAccuracy, 'part-I-accuracy.txt')

#function.readAndDisPlay('part-I-confusionMatrix.tsv')
function.readAndDisPlay('part-I-accuracy.txt')







