from itertools import *

stopWords = []
vocabulary = {}

# get stop words
fstop = open("stoplist.txt", 'r')
for stopWord in fstop:
    stopWords.append(stopWord.strip('\n'))
fstop.close()

# build vocabulary
#ffortune = open("traindata.txt", "r")
#flabel = open("trainlabels.txt", "r")
#for line in fvocab:
#    for item in line.split():
 #       if item in stopWords:
  #          continue
   #     else:
    #        if item not in vocabulary:
     #           vocabulary.append(item)
#vocabulary.sort()
#fvocab.close()

with open("traindata.txt", "r") as ffortune, open("trainlabels.txt", "r") as flabel:
    for data, label in zip(ffortune, flabel):
        for word in data.split():
            if word in stopWords:
                continue
            else:
                if word not in vocabulary.keys():
                    vocabulary[word] = label.strip('\n')

for item in range(0, 20):
    for word, label in vocabulary.items():
        print(word)
        