__author__ = 'zephyryin'

import Queue
import nltk
import function
from nltk.corpus import treebank

size = 500
maxTagSize = 5
trainSet = treebank.tagged_sents()[0:size]                      # create train set
taggedTestSet = treebank.tagged_sents()[size:(size + size)]
testSet = treebank.sents()[size:(size + size)]                  # create test set

t0 = nltk.DefaultTagger('NN')
t1 = nltk.UnigramTagger(trainSet, backoff=t0)
t2 = nltk.BigramTagger(trainSet, backoff=t1)                    # train

wordCnt = 0
predictions = []
dict = {}
confutionMatrix = [[0 for col in range(maxTagSize)] for row in range(maxTagSize)]
tagList = []
dict = function.genDict()

file = open('Method-A-predictions.tsv', 'w')

for i in range(size):
    prediction = t2.tag(testSet[i])                                 # use the model to predict the given word
    contrastResult = [i, taggedTestSet[i], prediction]
    predictions.append(contrastResult)                              # contrastResult saves the actual tag and predict tag
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

                actualTag = function.toCoarseTag(dict, contrastResult[1][k][1])            # change the fine tag to coarse tag
                predictTag = function.toCoarseTag(dict,contrastResult[2][k][1])

                if not actualTag in tagList:                            # save tags in tag list
                    tagList.append(actualTag)
                if not predictTag in tagList:
                    tagList.append(predictTag)

                y = tagList.index(actualTag)                            # map the index from tag list to confusion matrix
                x = tagList.index(predictTag)
                confutionMatrix[y][x] = confutionMatrix[y][x] + 1       # update confusion matrix

            file.write(word[0] + '/' + word[1])
        file.write('\t')
    file.write('\n')
file.close()
print('preditions saved in Method-A-predictions.tsv')

# compute accuracy based on the confusion matrix

accurateQ = Queue.PriorityQueue()                            # use priority queue to rank the accuracy
accurateList = []
accuratePredictCnt = 0

for y in range(len(tagList)):
    accuratePredictCnt = accuratePredictCnt + confutionMatrix[y][y]                  # save the number of right predictions
    accurateQ.put((100.0 * float(confutionMatrix[y][y]) / float(sum(confutionMatrix[y])), tagList[y]))      # compute accuracy for each tag

overallAccuracy = 100.0 * float(accuratePredictCnt) / float(wordCnt)                # compute the overall accuracy

while not accurateQ.empty():
    accurateList.append(accurateQ.get())
accurateList.reverse()                                  # reverse the list to be descending

function.saveConfusionMatrix(confutionMatrix, tagList, 'part-II-A-confusionMatrix.txt')         # save to disk
function.saveAccuracy(accurateList, overallAccuracy, 'part-II-A-accuracy.txt')

function.readAndDisPlay('part-II-A-accuracy.txt')
function.readAndDisPlay('part-II-A-confusionMatrix.txt')                            # display




