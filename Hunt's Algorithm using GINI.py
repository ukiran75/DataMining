'''
Course     : Data Mining
Professor  : Dr Hung Chi Su
Name       : Uday Talapaneni
Id         : 50484403
Home Work# : HW5(Hunts Algorithm Implementation)
********************Main File*******************
'''

import math
transactionData=[('n','n','c','l'),(1,1,125,0),(0,0,100,0),(0,1,70,0),(1,0,120,0),(0,2,95,1),
              (0,0,60,0),(1,2,220,0),(0,1,85,1),(0,0,75,0),(0,1,91,1)]


def calculateSeparatorValue(position):
    max=-10000000000;min=100000000000
    for transaction  in transactionData[1:]:
        if(transaction[position]<min):
            min=transaction[position]
        elif(transaction[position] > max):
            max=transaction[position]
    return (max+min)/2


def calculateOnes(leftNodeData):
    length=len(transactionData[0])
    onesCount=0
    for data in leftNodeData:
        if data[length-1]==1:
            onesCount+=1
    return onesCount




def calculateGiniNominal(position,nodeTransactions):
    seperatorValue=calculateSeparatorValue(position)
    leftNodeData = []
    rightNodeData = []
    for transaction in nodeTransactions :
        if (transaction[position] <= seperatorValue):
            leftNodeData.append(transaction)
        else:
            rightNodeData.append(transaction)
    leftNodeOnes=calculateOnes(leftNodeData)
    rightNodeOnes=calculateOnes(rightNodeData)
    leftNodeGini=1-(math.pow(leftNodeOnes/len(leftNodeData))+math.pow((len(leftNodeData)-leftNodeOnes)/len(leftNodeData)))
    rightNodeGini = 1 - (math.pow(rightNodeOnes / len(rightNodeData)) + math.pow((len(rightNodeData) - rightNodeOnes) / len(rightNodeData)))
    return ((len(leftNodeData)/len(nodeTransactions))*leftNodeGini)+((len(rightNodeData)/len(nodeTransactions))*rightNodeGini)


def calculateGiniContinuous(position):
    pass


def calculateGini(position,nodeTransactions):
    gini=0;
    attributeType=transactionData[0][position]
    if attributeType=='n':
        gini=calculateGiniNominal(position,nodeTransactions)
    elif attributeType=='c':
        gini=calculateGiniContinuous(position,nodeTransactions)


def calculateDefault(nodeTransactions):
    pass


def calculateBestGini(nodeTransactions,omitAttributes):
    if omitAttributes==(len(transactionData[0]-1)):
        calculateDefault(nodeTransactions)
    bestgini=10;
    pos=-1;
    for position in range(len(transactionData)-1):
        if position not in omitAttributes:
            gini=calculateGini(position,nodeTransactions)
            if gini <= bestgini:
                bestgini=gini
                pos=position;


