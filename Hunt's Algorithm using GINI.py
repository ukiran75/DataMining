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
              (0,0,60,0),(1,2,220,0),(0,1,85,1),(0,0,75,0),(0,1,90,1)]

def calculateSeparatorValue(position):
    max=-10000000000;min=100000000000
    for transaction  in transactionData[1:]:
        if(transaction[position]<min):
            min=transaction[position]
        elif(transaction[position] > max):
            max=transaction[position]
    return (max+min)/2


def calculateOnes(NodeData):
    length=len(transactionData[0])
    onesCount=0
    for data in NodeData:
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
    if len(leftNodeData)!=0:
        leftNodeGini=1-(math.pow(leftNodeOnes/len(leftNodeData),2)+math.pow((len(leftNodeData)-leftNodeOnes)/len(leftNodeData),2))
    else:
        leftNodeGini=0
    if len(rightNodeData)!=0:
        rightNodeGini = 1 - (math.pow(rightNodeOnes / len(rightNodeData),2) + math.pow((len(rightNodeData) - rightNodeOnes) / len(rightNodeData),2))
    else:
        rightNodeGini=0
    gini=((len(leftNodeData)/len(nodeTransactions))*leftNodeGini)+((len(rightNodeData)/len(nodeTransactions))*rightNodeGini)
    return [gini,seperatorValue,leftNodeData,rightNodeData]


def calculateGiniContinuous(position,nodeTransactions):
    values=[]
    for transaction in nodeTransactions:
        values.append(transaction[position])
    values.sort()
    initial=values[0]-10
    bestGini=10
    bestSeperatorValue=0
    bestLeftNode = []
    bestRightNode = []
    for value in values:
        seperatorValue=(initial+value)/2
        initial=value
        leftNodeData = []
        rightNodeData = []
        for transaction in nodeTransactions:
            if (transaction[position] <= seperatorValue):
                leftNodeData.append(transaction)
            else:
                rightNodeData.append(transaction)
        leftNodeOnes = calculateOnes(leftNodeData)
        rightNodeOnes = calculateOnes(rightNodeData)
        if len(leftNodeData) != 0:
            leftNodeGini = 1 - (math.pow(leftNodeOnes / len(leftNodeData),2) + (math.pow(
                (len(leftNodeData) - leftNodeOnes) / len(leftNodeData),2)))
        else:
            leftNodeGini = 0;
        if len(rightNodeData) != 0:
            rightNodeGini = 1 - (math.pow(rightNodeOnes / len(rightNodeData),2) + (math.pow(
                (len(rightNodeData) - rightNodeOnes) / len(rightNodeData),2)))
        else:
            rightNodeGini = 0;
        gini=((len(leftNodeData)/len(nodeTransactions))*leftNodeGini)+((len(rightNodeData)/len(nodeTransactions))*rightNodeGini)
        if gini <= bestGini:
            bestGini=gini
            bestSeperatorValue=seperatorValue
            bestLeftNode=leftNodeData
            bestRightNode=rightNodeData

    return [bestGini,bestSeperatorValue,bestLeftNode,bestRightNode]




def calculateGini(position,nodeTransactions):
    attributeType=transactionData[0][position]
    values=[]
    if attributeType=='n':
        values=calculateGiniNominal(position,nodeTransactions)
    elif attributeType=='c':
        values=calculateGiniContinuous(position,nodeTransactions)
    return values


def calculateDefault(checkData):
    zeroCount = 0
    oneCount = 0
    length=len(transactionData[0])-1
    for data in checkData:
        if (data[length] == 0):
            zeroCount += 1
        elif (data[length] == 1):
            oneCount += 1
    if (zeroCount >= oneCount):
        return 0
    else:
        return 1


def calculateBestGini(nodeTransactions,omitAttributes):
    bestgini=10;
    bestPos=-1
    nextSplitValues=[]
    for position in range(0,(len(transactionData[0])-1)):
        if position not in omitAttributes:
            values=calculateGini(position,nodeTransactions)
            if(len(values)>0):
                gini=values[0]
                if gini <= bestgini:
                    bestgini=gini
                    bestPos=position
                    nextSplitValues=values
    print(nextSplitValues)
    omitAttributes.append(bestPos)
    print("omitAttributes:"+str(omitAttributes))
    omitAttributes2=omitAttributes
    if(len(omitAttributes)!=3 and len(nextSplitValues)>2):
       if len(nextSplitValues[2])!=0:
          print("Inside left split")
          calculateBestGini(nextSplitValues[2],omitAttributes)
       else:
          default=calculateDefault(nodeTransactions)
          print("default left:"+str(default))
       if (len(nextSplitValues[3]) != 0):
           print("Inside right split")
           calculateBestGini(nextSplitValues[3], omitAttributes2)
       else:
         default = calculateDefault(nodeTransactions)
         print("default right:" + str(default))

calculateBestGini(transactionData[1:],[])


