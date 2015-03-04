__author__ = 'zephyryin'

import copy

def genDict():
    dict = {}
    snnList = ['NN', 'NNS', 'NNP', 'NNPS', 'PRP', 'PRP$']
    svbList = ['VB', 'VBP', 'VBD', 'VBN', 'VBZ', 'VBG']
    sjjList = ['JJ', 'JJR', 'JJS']
    srbList = ['RB', 'RBR', 'RBS']

    for l in snnList:
        dict[l] = 'SNN'

    for l in svbList:
        dict[l] = 'SVB'

    for l in sjjList:
        dict[l] = 'SJJ'

    for l in srbList:
        dict[l] = 'SRB'

    return dict

def toCoarseTag(dict, actualTag):
    if actualTag in dict:
        return dict[actualTag]
    else:
        return 'misc'


def saveConfusionMatrix(conM, tList, fileName):              # write the confusion matrix to local confusionMatrix.txt
    wordLen = 6
    file = open(fileName, 'w')
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

def saveAccuracy(accuList, overallAcu, fileName):
    wordLen = 6
    file = open(fileName, 'w')
    file.write('overall accuracy: ' + str(overallAcu) + '\n\n')
    for l in accuList:
        file.write(str(l[1]))
        for i in range(wordLen - len(str(l[1]))):
            file.write(' ')
        file.write(' ' + str(l[0]) + '\n')
    file.close()

def toCoarseTaggedSet(dict, sents):
    cTaggedSents = []
    for sent in sents:
        #print(sent)
        newSent = []
        for wordTag in sent:
            newWordTag = (wordTag[0], toCoarseTag(dict, wordTag[1]))
            newSent.append(newWordTag)
        cTaggedSents.append(newSent)
    return cTaggedSents
