'''
Course     : Data Mining
Professor  : Dr Hung Chi Su
Name       : Uday Talapaneni
Id         : 50484403
Home Work# : HW5(Hunts Algorithm Implementation)
********************Main File*******************
'''

import math
import sys
transactionData=[('n','o','c','l'),(1,0,125,0),(0,1,100,0),(0,0,70,0),(1,1,120,0),(0,2,95,1),
              (0,1,60,0),(1,2,220,0),(0,0,85,1),(0,1,75,0),(0,0,90,1)]
tree=[]
sys.setrecursionlimit(1500)
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

def calculateGiniOrdinal(position,nodeTransactions):
    uniqVal=[]
    bestGini = 10
    bestSeperatorValue = 0
    bestLeftNode = []
    bestRightNode = []
    for transaction in nodeTransactions:
        if transaction[position] not in uniqVal:
            uniqVal.append(transaction[position])
    for val in uniqVal:
        values=calGini(position,nodeTransactions,val,1)
        if values[0] < bestGini:
            bestGini=values[0]
            bestSeperatorValue=values[1]
            bestLeftNode=values[2]
            bestRightNode=values[3]
    return [bestGini, bestSeperatorValue, bestLeftNode, bestRightNode]

def calGini(position,nodeTransactions,seperatorValue,ordinal=0):
    leftNodeData = []
    rightNodeData = []
    if(ordinal==0):
        for transaction in nodeTransactions:
            if (transaction[position] <= seperatorValue):
                leftNodeData.append(transaction)
            else:
                rightNodeData.append(transaction)
    else:
        for transaction in nodeTransactions:
            if (transaction[position] == seperatorValue):
                leftNodeData.append(transaction)
            else:
                rightNodeData.append(transaction)
    leftNodeOnes = calculateOnes(leftNodeData)
    rightNodeOnes = calculateOnes(rightNodeData)
    if len(leftNodeData) != 0:
        leftNodeGini = 1 - (math.pow(leftNodeOnes / len(leftNodeData), 2) + (math.pow(
            (len(leftNodeData) - leftNodeOnes) / len(leftNodeData), 2)))
    else:
        leftNodeGini = 0
    if len(rightNodeData) != 0:
        rightNodeGini = 1 - (math.pow(rightNodeOnes / len(rightNodeData), 2) + (math.pow(
            (len(rightNodeData) - rightNodeOnes) / len(rightNodeData), 2)))
    else:
        rightNodeGini = 0
    gini = ((len(leftNodeData) / len(nodeTransactions)) * leftNodeGini) + (
    (len(rightNodeData) / len(nodeTransactions)) * rightNodeGini)
    return [gini,seperatorValue,leftNodeData,rightNodeData]



def calculateGiniNominal(position,nodeTransactions):
    seperatorValue=calculateSeparatorValue(position)
    return calGini(position,nodeTransactions,seperatorValue)


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
        values=calGini(position,nodeTransactions,seperatorValue)
        if values[0] <= bestGini:
            bestGini=values[0]
            bestSeperatorValue=values[1]
            bestLeftNode=values[2]
            bestRightNode=values[3]
    return [bestGini,bestSeperatorValue,bestLeftNode,bestRightNode]




def calculateGini(position,nodeTransactions):
    attributeType=transactionData[0][position]
    values=[]
    if attributeType=='n':
        values=calculateGiniNominal(position,nodeTransactions)
    elif attributeType=='c':
        values=calculateGiniContinuous(position,nodeTransactions)
    elif attributeType == 'o':
        values = calculateGiniOrdinal(position, nodeTransactions)
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

def checkPurity(checkData):
    zeroCount=0;oneCount=0
    length = len(transactionData[0]) - 1
    if(len(checkData)==0):
        return -1
    for data in checkData:
      if(data[length]==0):
        zeroCount+=1
      elif(data[length]==1):
        oneCount+=1
    if(len(checkData)==zeroCount):
        return 0
    elif(len(checkData)==oneCount):
        return 1
    else:
        return 2

def calculateBestGini(nodeTransactions,omitAttributes):
    if(len(omitAttributes)>3):
        default=calculateDefault(nodeTransactions)
        print("Defaut Node:"+str(default))
        return
    bestgini=10
    bestPos=-1
    nextSplitValues=[]
    for position in range(0,(len(transactionData[0])-1)):
        if position not in omitAttributes:
            values=calculateGini(position,nodeTransactions)
            if(len(values)>0):
                gini=values[0]
                #print("gini:"+str(gini))
                if gini < bestgini:
                    bestgini=gini
                    bestPos=position
                    nextSplitValues=values
    #print(nextSplitValues)
    omitAttributes.append(bestPos)
    #print("omitAttributes:"+str(omitAttributes))
    leftFlag=0;rightFlag=0
    if(len(omitAttributes)<=3):
       #print(len(omitAttributes))
       if (len(nextSplitValues[2])!=0):
          #print("Inside left split")
          purity=checkPurity(nextSplitValues[2])
          if(purity==2 and len(omitAttributes)<3 ):
              print("Left Node Needs Splitting(Position="+str(bestPos)+"),Split Value=("+str(nextSplitValues[1])+")")
              nodeVal = []
              nodeVal.append(0)
              nodeVal.append(1)
              nodeVal.append(bestPos)
              nodeVal.append(nextSplitValues[1])
              nodeVal.append(0)
              tree.append(nodeVal)
              #tree.append("("+str(0)+","+str(0)+","+str(bestPos)+","+str(nextSplitValues[1])+","+str(0)+")")
              leftFlag=1
              #calculateBestGini(nextSplitValues[2],omitAttributes)
          elif (len(omitAttributes)==3 and purity==2):
              default = calculateDefault(nodeTransactions)
              nodeVal = []
              nodeVal.append(0)
              nodeVal.append(1)
              nodeVal.append(bestPos)
              nodeVal.append(nextSplitValues[1])
              nodeVal.append(default)
              tree.append(nodeVal)
              #tree.append("(" + str(0) + "," + str(1) + "," + str(bestPos) + "," + str(nextSplitValues[1]) + "," + str(default) + ")")
              print("default left:" + str(default))
          else:
              #tree.append("(" + str(0) + "," + str(1) + "," + str(bestPos) + "," + str(nextSplitValues[1]) + "," + str(purity) + ")")
              nodeVal = []
              nodeVal.append(0)
              nodeVal.append(1)
              nodeVal.append(bestPos)
              nodeVal.append(nextSplitValues[1])
              nodeVal.append(purity)
              tree.append(nodeVal)
              print("LeftNode Pure with value:"+str(purity))
       else:
           default = calculateDefault(nodeTransactions)
           nodeVal = []
           nodeVal.append(0)
           nodeVal.append(1)
           nodeVal.append(bestPos)
           nodeVal.append(nextSplitValues[1])
           nodeVal.append(default)
           tree.append(nodeVal)
           #tree.append("(" + str(0) + "," + str(1) + "," + str(bestPos) + "," + str(nextSplitValues[1]) + "," + str(default) + ")")
           print("default left:" + str(default))


       if (len(nextSplitValues[3])!=0):
         # print("Inside right split")
          purity=checkPurity(nextSplitValues[3])
          if(purity==2 and len(omitAttributes)<3):
              print("Right Node Needs Splitting(Position="+str(bestPos)+"),Split Value=("+str(nextSplitValues[1])+")")
              #tree.append("(" + str(1) + "," + str(0) + "," + str(bestPos) + "," + str(nextSplitValues[1]) + "," + str(0) + ")")
              nodeVal = []
              nodeVal.append(1)
              nodeVal.append(0)
              nodeVal.append(bestPos)
              nodeVal.append(nextSplitValues[1])
              nodeVal.append(0)
              tree.append(nodeVal)
              rightFlag = 1
              #calculateBestGini(nextSplitValues[3],omitAttributes)
          elif (len(omitAttributes)==3 and purity==2):
              default = calculateDefault(nodeTransactions)
              nodeVal=[]
              nodeVal.append(1)
              nodeVal.append(1)
              nodeVal.append(bestPos)
              nodeVal.append(nextSplitValues[1])
              nodeVal.append(default)
              tree.append(nodeVal)
              #tree.append("(" + str(1) + "," + str(1)+ "," + str(bestPos) + "," + str(nextSplitValues[1]) + "," + str(default) + ")")
              print("default right:" + str(default))
          else:
              nodeVal = []
              nodeVal.append(1)
              nodeVal.append(1)
              nodeVal.append(bestPos)
              nodeVal.append(nextSplitValues[1])
              nodeVal.append(purity)
              tree.append(nodeVal)
              #tree.append("(" + str(1) + "," + str(1) + "," + str(bestPos) + "," + str(nextSplitValues[1]) + "," + str(purity) + ")")
              print("RightNode Pure with value:"+str(purity))
       else:
           default = calculateDefault(nodeTransactions)
           nodeVal = []
           nodeVal.append(1)
           nodeVal.append(1)
           nodeVal.append(bestPos)
           nodeVal.append(nextSplitValues[1])
           nodeVal.append(default)
           tree.append(nodeVal)
           #tree.append("(" + str(1) + "," + str(1) + "," + str(bestPos) + "," + str(nextSplitValues[1]) + "," + str(default) + ")")
           print("default right:" + str(default))
    if(leftFlag==1):
        calculateBestGini(nextSplitValues[2], omitAttributes)
    if (rightFlag == 1):
        calculateBestGini(nextSplitValues[3], omitAttributes)

print("Node Values(Left(0)OrRight(1),isLeaf,AttributePosition,SeperatorValue,Label)")


def traverse(input,i):
    while i < len(tree) :
        attPos = tree[i][2]
        if(input[attPos]<=tree[i][3]):
            if(tree[i][0]==1):
                print(tree[i][4])
            else:
                if(tree[i+1][0]==1):
                    i=+2
                    traverse(input,i)
                else:
                    i+=3
                    traverse(input, i)
        else:
            i=i+1
            if (tree[i][0] == 1):
                print(tree[i][4])
            else:
                if (tree[i - 1][0] == 1):
                    i = +1
                    traverse(input, i)
                else:
                    i+=2
                    traverse(input,i)


calculateBestGini(transactionData[1:],[])
print(str(tree))

traverse([0,1,150],0)