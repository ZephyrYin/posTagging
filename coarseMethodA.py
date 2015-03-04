__author__ = 'zephyryin'

import Queue
import nltk
import function
from nltk.corpus import treebank


size = 500
maxTagSize = 5
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
dict = function.genDict()

file = open('Method-A-predictions.tsv', 'w')

for i in range(size):
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

                actualTag = function.toCoarseTag(dict, contrastResult[1][k][1])
                predictTag = function.toCoarseTag(dict,contrastResult[2][k][1])

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
    accurateQ.put((100.0 * float(confutionMatrix[y][y]) / float(sum(confutionMatrix[y])), tagList[y]))

overallAccuracy = 100.0 * float(accuratePredictCnt) / float(wordCnt)

print('words: ' + str(wordCnt))
print('right tag cnt: ' + str(accuratePredictCnt))
print('overallAccuraty: ' + str(overallAccuracy))
while not accurateQ.empty():
    accurateList.append(accurateQ.get())
accurateList.reverse()

function.saveConfusionMatrix(confutionMatrix, tagList, 'part-II-A-confusionMatrix.txt')
function.saveAccuracy(accurateList, overallAccuracy, 'part-II-A-accuracy.txt')




