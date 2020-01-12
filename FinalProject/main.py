import csv
from GameProfile import GameProfile
from apyori import apriori
import pandas as pd 
import numpy as np

HighSalesAttributes = []
LowSaleAttributes = []
tempLow = []
tempHigh = []
FinalPositiveAttributes = []
FinalNegativeAttributes = []
Strengths = []
Suggestions = []

index = 0

data = pd.read_csv("steam.csv")

# mark empty attribute columns to be dropped
data['steamspy_tags'].replace('', np.nan, inplace=True)
data.dropna(subset=['steamspy_tags'], inplace=True)

rows = data.shape[0]
cols = data.shape[1]

f = open("output.txt", "w+")

#####################################################################################
#         Get attributes associated with games that have a high sales count         #
#####################################################################################
for i in range(0, rows):
    sales = data.values[i,16].split("-") # sales are categorized as a range
     # sales of at least 5 million AND positive rating is greater than negative
    if (int(sales[1]) > 4999999) and (data.values[i,12] > data.values[i,13]):         
        tempList = data.values[i,10].split(';') #semicolon separated attributes
        HighSalesAttributes.append(tempList)

#####################################################################################
#         Get attributes associated with games that have a low sales count          #
#####################################################################################
for i in range(0, rows):
    sales = data.values[i,16].split("-")
    #sales less than 50 thousand AND negative ratings are greater than positive
    if (int(sales[1]) < 1000000) and (data.values[i,13] > data.values[i,12]):           
        tempList = data.values[i,10].split(';') #semicolon separated attributes
        LowSaleAttributes.append(tempList)

#####################################################################################
#     Run apriori on games with high sales to find frequent pairs of attributes     #
#####################################################################################
HighAttrCountDict = {}
freqPairs = apriori(HighSalesAttributes, min_support=.003, min_confidence=0.7, min_length=3, max_length=3)
HighSaleResults = list(freqPairs)
for record in HighSaleResults:
    if len(record[0]) == 3:
        for item in record[0]:  
            #add to dictionary so the num of games containing attribute can be counted 
            if item not in HighAttrCountDict.keys():
                HighAttrCountDict[item] = 1
            else:
                HighAttrCountDict[item] += 1

#####################################################################################
#  Sort Dictionary to find which attributes occur most often in high selling games  #
#####################################################################################
SortedHighAttrCount = sorted(HighAttrCountDict.items(), key = 
             lambda kv:(kv[1], kv[0]), reverse=True)

#####################################################################################
#     Run apriori on games with high sales to find frequent pairs of attributes     #
#####################################################################################
LowAttrCountDict = {}
freqPairs = apriori(LowSaleAttributes, min_support=.003, min_confidence=0.3, min_length=2, max_length=2)
LowSaleResults = list(freqPairs)
for record in LowSaleResults:
    if len(record[0]) == 2:
        for item in record[0]:  
            #add to dictionary so the num of games containing attribute can be counted 
            if item not in LowAttrCountDict.keys():
                LowAttrCountDict[item] = 1
            else:
                LowAttrCountDict[item] += 1

#####################################################################################
#  Sort Dictionary to find which attributes occur most often in low selling games   #
#####################################################################################
SortedLowAttrCount = sorted(LowAttrCountDict.items(), key = 
             lambda kv:(kv[1], kv[0]), reverse=True)

#####################################################################################
# check if sorted dicts contain the same attributes and remove those (too broad)    #
# or adjust occurance                                                               #
#####################################################################################
for item in SortedHighAttrCount:
    for subItem in SortedLowAttrCount:
        if item[0] == subItem[0]:
            if item[1] > subItem[1]: # more frequent in high sales
                HighAttrCountDict[item[0]] = item[1] - subItem[1]
                del LowAttrCountDict[subItem[0]]
            elif item[1] < subItem[1]: #more frequent in low sales
                LowAttrCountDict[subItem[0]] = subItem[1] - item[1]
                del HighAttrCountDict[item[0]]
            else: #equal
                del HighAttrCountDict[item[0]]
                del LowAttrCountDict[subItem[0]]
# then resort dictionaries
SortedHighAttrCount = sorted(HighAttrCountDict.items(), key = 
             lambda kv:(kv[1], kv[0]), reverse=True)
SortedLowAttrCount = sorted(LowAttrCountDict.items(), key = 
             lambda kv:(kv[1], kv[0]), reverse=True)

#####################################################################################
#                   Find shorter list to keep comparisons even                      #
#####################################################################################
if len(SortedHighAttrCount) > len(SortedLowAttrCount):
    count = len(SortedLowAttrCount)
else:
    count = len(SortedHighAttrCount)

#####################################################################################
#       sum the total of all occurances for low and high selling attributes         #
#####################################################################################
temp1 = temp2 = count
lowSum = 0
for value in SortedLowAttrCount:
    tempLow.append(value)
    lowSum += value[1]
    temp1 -= 1
    if temp1 == 0:
        break
   
highSum = 0
for value in SortedHighAttrCount:
    tempHigh.append(value)
    highSum += value[1]
    temp2 -= 1
    if temp2 == 0:
        break

#####################################################################################
#       Store final list with all results and weights to be used for comparison     #
#####################################################################################
for item in tempHigh:
    weight = item[1] / highSum
    FinalPositiveAttributes.append((item[0], weight))

for item in tempLow:
    weight = item[1] / lowSum
    FinalNegativeAttributes.append((item[0], (weight * -1)))

#####################################################################################
#                      Run training data against proposed game                      #
#####################################################################################
ProposedGame = GameProfile()
for item in FinalPositiveAttributes:
    if item[0] in ProposedGame.attributes:
        Strengths.append(item)
        ProposedGame.projectedSuccessScore += item[1]
for item in FinalNegativeAttributes:
    if item[0] in ProposedGame.attributes:
        Suggestions.append(item)
        ProposedGame.projectedSuccessScore += item[1]

#####################################################################################
#                                      Results                                      #
#####################################################################################
f.write("**********************************RESULTS***********************************\n\n")
if ProposedGame.projectedSuccessScore > 0:
    f.write("Success! the projected score is: " + str(ProposedGame.projectedSuccessScore))
else:
    f.write("Rethink design. Outlook isn't promising with a projected score of: " + str(ProposedGame.projectedSuccessScore))
    
f.write("\n\n----------------------------------------------------------------------------")
f.write("\n\n\t\t\tStrengths:\n")
for item in Strengths:
    f.write("Attribute: " + str(item[0]) + " | Positive Impact: " + str(item[1]) + "\n")
f.write("\n\n\t\t\tSuggested Design Modifications:\n")
for item in Suggestions:
    f.write("Attribute: " + str(item[0]) + " | Negative Impact: " + str(item[1]) + "\n")
f.write("\n")

ProposedGame.printProfile(f)
f.close()