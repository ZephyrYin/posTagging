__author__ = 'zephyryin'

import Queue
import nltk
import function
from nltk.corpus import treebank


size = 500
maxTagSize = 5
dict = function.genDict()

originalTaggedSents = treebank.tagged_sents()[0:size+size]
coaseTaggedSet = function.toCoarseTaggedSet(dict, originalTaggedSents)          # change the fine tag to coarse tag

trainSet = coaseTaggedSet[0:size]
taggedTestSet = coaseTaggedSet[size:(size + size)]
testSet = treebank.sents()[size:(size + size)]

t0 = nltk.DefaultTagger('SNN')
t1 = nltk.UnigramTagger(trainSet, backoff=t0)
t2 = nltk.BigramTagger(trainSet, backoff=t1)            # train

wordCnt = 0
predictions = []
confutionMatrix = [[0 for col in range(maxTagSize)] for row in range(maxTagSize)]
tagList = []

file = open('Method-B-predictions.tsv', 'w')

for i in range(size):
    prediction = t2.tag(testSet[i])                         # use the model to predict the given word
    contrastResult = [i, taggedTestSet[i], prediction]
    predictions.append(contrastResult)                      # contrastResult saves the actual tag and predict tag

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
                    tagList.append(predictTag)                      # save tags in tag list

                y = tagList.index(actualTag)
                x = tagList.index(predictTag)
                confutionMatrix[y][x] = confutionMatrix[y][x] + 1           # update confusion matrix

            file.write(word[0] + '/' + word[1])
        file.write('\t')
    file.write('\n')
file.close()
print('preditions saved in Method-B-predictions.tsv')

# compute accuracy based on the confusion matrix

accurateQ = Queue.PriorityQueue()                               # use priority queue to rank the accuracy
accurateList = []
accuratePredictCnt = 0

for y in range(len(tagList)):
    accuratePredictCnt = accuratePredictCnt + confutionMatrix[y][y]             # save the number of right predictions
    accurateQ.put((100.0 * float(confutionMatrix[y][y]) / float(sum(confutionMatrix[y])), tagList[y]))      # compute accuracy for each tag

overallAccuracy = 100.0 * float(accuratePredictCnt) / float(wordCnt)            # compute the overall accuracy

while not accurateQ.empty():
    accurateList.append(accurateQ.get())
accurateList.reverse()

function.saveConfusionMatrix(confutionMatrix, tagList, 'part-II-B-confusionMatrix.txt')             # save to disk
function.saveAccuracy(accurateList, overallAccuracy, 'part-II-B-accuracy.txt')

function.readAndDisPlay('part-II-B-accuracy.txt')
function.readAndDisPlay('part-II-B-confusionMatrix.txt')            # display




