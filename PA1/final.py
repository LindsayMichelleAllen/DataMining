import csv
import operator
import pandas as pd
from  apyori import apriori

index = 0
temp = 0

outputFile = ''

with open("browsing-data.txt", "r") as csvfile:
    hw1reader = csv.reader(csvfile, delimiter=' ')
    for row in hw1reader:
        if index == 0:
            temp = len(row)
        elif len(row) > temp:
            temp = len(row)
        index += 1

maxlength = temp

index = 0
temp = 0

print("building csv file...")
new_file = ' '
with open("browsing-data.txt", "r") as csvfile:
    hw1reader = csv.reader(csvfile, delimiter=' ')
    for row in hw1reader:
        newstr = ' '
        index += 1
        for x in range(len(row)):
            if(row[x] != ' '):
                newstr += row[x]
                newstr += ', '
            
        if len(row) < maxlength:
            diff = maxlength - len(row)
            for x in range(len(row), maxlength):
                newstr += ", "

        new_file = new_file + '\n' + newstr + '\n'

with open("newinput.txt", "w+") as f:
    f.write(new_file)
print("csv file created...")
data = pd.read_csv("newinput.txt", header=None)

data.head()
data.info()

records = []
rows = data.shape[0]
cols = data.shape[1]


for i in range(0, rows):
    records.append([str(data.values[i,j]) for j in range(0, cols)])

for lis in records:
    i=0 
    length = len(lis)   
    while(i<length):
	    if(lis[i]==' '):
		    lis.remove(lis[i])
		    length -= 1  
		    continue
	    i += 1

final2 = []
outputA = []
print("starting apriori length 2...")
hw2rules = apriori(records, min_support=.003, min_confidence=0.4, min_length=2, max_length=2)
hw2results = list(hw2rules)
for record in hw2results:
    item = record[0]
    items = [x for x in item]
    if len(items) == 2:     # only add length of 2
        ltup = (items[0], items[1])
        cscore = record[2][0][2]
        tup = (ltup, cscore)
        final2.append(tup)

final2.sort(key = operator.itemgetter(1, 0), reverse=True)

outputFile += "OUTPUT A\n"

i = 0
for item in final2:
    if i < 5:
        outputFile += str(item[0][0]) + " " + str(item[0][1]) + " " + str(item[1]) + '\n'
    else:
        break
    i += 1


final3 = []
print("starting apriori length 3...")
hw3rules = apriori(records, min_support=.003, min_confidence=0.4, min_length=3, max_length=3)
hw3results = list(hw3rules)
for record in hw3results:
    item = record[0]
    items = [x for x in item]
    if len(items) == 3:
        ltup = (items[0], items[1], items[2])
        cscore = record[2][0][2]
        tup = (ltup, cscore)
        final3.append(tup)   #only add length of 3

final3 = sorted(final3, key = operator.itemgetter(1, 0), reverse=True)

outputFile += "\nOUTPUT B\n"
i = 0
for item in final3:
    if i < 5:
        outputFile += str(item[0][0]) + " " + str(item[0][1]) + " " + str(item[0][2]) + " " + str(item[1]) + '\n'
    else:
        break
    i += 1

with open("output.txt", "w+") as f:
    f.write(outputFile)

print("output file created")