__author__ = 'zephyryin'

import Queue

# names = [('NN','NN'), ('Bob','jack'), ('Tracy','jack'), ('jack','NN'), ('Bob','Bob'),('bob','NN')]
# print(names)
names = ['NN','JJ','NMB','fuck']
scores = [95, 75, 85, 56]


l = []
l.append((0.5,'a'))
l.append((0.34,'b'))
l.append((0.03,'c'))

print(l)

scores.reverse()
file = open('accuracy.txt', 'w')

for s in l:
    file.write(str(s[1]) + ' ' + str(s[0]))
    file.write('\n')
file.close()
#file.write(str(scores))

# list = queue.PriorityQueue
# for i in range(len(scores)):
#     list.put((scores[i], names[i]))
# print(list)

# dict = {}
# for i in range(len(names)):
#     if names[i] in dict:
#         dict[names[i]] =  dict[names[i]] + 1
#     else:
#         dict[names[i]] = 0
#     print(dict)
#
# matrix = [[0 for col in range(10)] for row in range(10)]
#
#
#
# l = []
# x = -1
# y = -1
# for n in names:
#     #print(n)
#     if not n[0] in l:
#        l.append(n[0])
#     if not n[1] in l:
#         l.append(n[1])
#     y = l.index(n[0])
#     x = l.index(n[1])
#
#
#     matrix[y][x] = matrix[y][x] + 1
#
#
# for m in matrix:
#     print(m)
#
# d = {}
# list = [1,2,3]
#
# print(sum(list))

