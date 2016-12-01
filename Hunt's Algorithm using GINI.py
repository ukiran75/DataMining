
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
transactionData=[('n','n','c','l'),(1,0,125,0),(0,1,100,0),(0,0,70,0),(1,1,120,0),(0,2,95,1),
              (0,1,60,0),(1,2,220,0),(0,0,85,1),(0,1,75,0),(0,0,90,1)]
tree=[]
#calculating ones in the node for gini calculation
def calculateOnes(NodeData):
    length=len(transactionData[0])
    onesCount=0
    for data in NodeData:
        if data[length-1]==1:
            onesCount+=1
    return onesCount

#Method to calculate gini for ordinal attributes
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
        if values[0] < bestGini:# if the gini for a split is better than the other split in atrribute make that as the best split
            bestGini=values[0]
            bestSeperatorValue=values[1]
            bestLeftNode=values[2]
            bestRightNode=values[3]
    return [bestGini, bestSeperatorValue, bestLeftNode, bestRightNode]

#method to calculate the gini
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


#Method to calculate gini for nominal attributes
def calculateGiniNominal(position,nodeTransactions):
    uniqVal = []
    bestGini = 10
    bestSeperatorValue = 0
    bestLeftNode = []
    bestRightNode = []
    for transaction in nodeTransactions:
        if transaction[position] not in uniqVal:
            uniqVal.append(transaction[position])
    for val in uniqVal:
        values = calGini(position, nodeTransactions, val, 0)
        if values[0] < bestGini:# if the gini for a split is better than the other split in atrribute make that as the best split
            bestGini = values[0]
            bestSeperatorValue = values[1]
            bestLeftNode = values[2]
            bestRightNode = values[3]
    return [bestGini, bestSeperatorValue, bestLeftNode, bestRightNode]

#Method to calculate gini for continuous attributes
def calculateGiniContinuous(position,nodeTransactions):
    values=[]
    for transaction in nodeTransactions: #getting all the continuous values for iterating to find the best split
        values.append(transaction[position])
    values.sort()
    initial=values[0]-10
    bestGini=10
    bestSeperatorValue=0
    bestLeftNode = []
    bestRightNode = []
    for value in values:
        seperatorValue=(initial+value)/2 #getting the average for the previous value and current value for finding split value
        initial=value
        values=calGini(position,nodeTransactions,seperatorValue)
        if values[0] < bestGini:# if the gini for a split is better than the other split in atrribute make that as the best split
            bestGini=values[0]
            bestSeperatorValue=values[1]
            bestLeftNode=values[2]
            bestRightNode=values[3]
    return [bestGini,bestSeperatorValue,bestLeftNode,bestRightNode]



#calling the calculate gini based on the attribute type
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

# calculating the default value of the label from the data
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
#checking the purity of the node
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

#getting the node value
def getNodevalue(lOr,isleaf,attrposition,splitValue,label):
    value=[]
    value.append(lOr)
    value.append(isleaf)
    value.append(attrposition)
    value.append(splitValue)
    value.append(label)
    return value

#calculating the bestgini for the attributes in the nodeData
def calculateBestGini(nodeTransactions,omitAttributes):
    if(len(omitAttributes)>3):#continue if we didnt split all the attribute(ie no attributes left to split)
        default=calculateDefault(nodeTransactions)#if so make the a default node
        print("Defaut Node:"+str(default))
        return
    bestgini=10
    bestPos=-1
    nextSplitValues=[]
    for position in range(0,(len(transactionData[0])-1)):#calculating the best gini split from the attributes left
        if position not in omitAttributes:
            values=calculateGini(position,nodeTransactions)
            if(len(values)>0):
                gini=values[0]
                print("gini:"+str(gini))
                if gini <= bestgini:
                    bestgini=gini
                    bestPos=position
                    nextSplitValues=values
    omitAttributes.append(bestPos)#if we find an attribute having best gini split omit that attribute for furthur splitting
    leftFlag=0;rightFlag=0
    if(len(omitAttributes)<=3):
       if (len(nextSplitValues[2])!=0):
          #print("Inside left split")
          purity=checkPurity(nextSplitValues[2])#check if the node id pure
          if(purity==2 and len(omitAttributes)<3 ):#if the node is not pure we still have attributes to split recurse the calculateBestGini()
              print("Left Node Needs Splitting(Position="+str(bestPos)+"),Split Value=("+str(nextSplitValues[1])+")")
              nodeVal = getNodevalue(0,0,bestPos,nextSplitValues[1],0)
              tree.append(nodeVal)
              leftFlag=1
          elif (len(omitAttributes)==3 and purity==2):#if the node is not pure we do not  have attributes to split calculate the default node
              default = calculateDefault(nodeTransactions)
              nodeVal = nodeVal = getNodevalue(0,1,bestPos,nextSplitValues[1],default)
              tree.append(nodeVal)
              print("default left(No attribute to split):" + str(default))
          else:#if the  node is pure
              nodeVal = getNodevalue(0,1,bestPos,nextSplitValues[1],purity)
              tree.append(nodeVal)
              print("LeftNode Pure with value:"+str(purity))
       else:
           default = calculateDefault(nodeTransactions)#if the node do not  have any data to split calculate the default node
           nodeVal = nodeVal = getNodevalue(0, 1, bestPos, nextSplitValues[1], default)
           tree.append(nodeVal)
           print("default left(No node data):" + str(default))


       if (len(nextSplitValues[3])!=0):
         # print("Inside right split")
          purity=checkPurity(nextSplitValues[3])#check if the node id pure
          if(purity==2 and len(omitAttributes)<3):#if the node is not pure we still have attributes to split recurse the calculateBestGini()
              print("Right Node Needs Splitting(Position="+str(bestPos)+"),Split Value=("+str(nextSplitValues[1])+")")
              nodeVal = getNodevalue(1, 0, bestPos, nextSplitValues[1], 0)
              tree.append(nodeVal)
              rightFlag = 1
          elif (len(omitAttributes)==3 and purity==2):#if the node is not pure we do not  have attributes to split calculate the default node
              default = calculateDefault(nodeTransactions)
              nodeVal = nodeVal = getNodevalue(1, 1, bestPos, nextSplitValues[1], default)
              tree.append(nodeVal)
              print("default Right(No attribute to split):" + str(default))
          else:#if the  node is pure
              nodeVal = nodeVal = getNodevalue(1, 1, bestPos, nextSplitValues[1], purity)
              tree.append(nodeVal)
              print("RightNode Pure with value:"+str(purity))
       else:
           default = calculateDefault(nodeTransactions)#if the node do not  have any data to split calculate the default node
           nodeVal = nodeVal = getNodevalue(1, 1, bestPos, nextSplitValues[1], default)
           tree.append(nodeVal)
           print("default left(No node data)" + str(default))
    if(leftFlag==1):# if the leftnode is not pure call recursion
        calculateBestGini(nextSplitValues[2], omitAttributes)
    if (rightFlag == 1):# if the rightnode is not pure call recursion
        calculateBestGini(nextSplitValues[3], omitAttributes)



stop=0
def traverse(input,i):
    global stop
    while (i < len(tree)) and (stop==0) :
        attPos = tree[i][2]
        flag=0
        flag2=0
        if(tree[i][0]==1):
            flag2=1
        if(transactionData[0][attPos]=='o'):
            flag=1
        if(input[attPos]<=tree[i][3] and flag==0 and flag2==0):
            if(tree[i][1]==1):
                print('\nThe class label for input is: '+str(tree[i][4]))
                stop=1
            else:
                if(tree[i+1][1]==1):
                    i+=2
                    traverse(input,i)
                else:
                    i+=3
                    traverse(input, i)
        elif (input[attPos] == tree[i][3] and flag==1 and flag2==0):
            if (tree[i][1] == 1):
                print(tree[i][4])
                exit(1)
            else:
                if (tree[i + 1][1] == 1):
                    i += 2
                    traverse(input, i)
                else:
                    i += 3
                    traverse(input, i)
        else:
            i=i+1
            if(flag2==1):
                i=i-1
            if (i<len(tree)):
                if (tree[i][1] == 1):
                    print('\nThe class label for input is: ' + str(tree[i][4]))
                    stop=1
                else:
                    if (tree[i - 1][1] == 1):
                        i  +=1
                        traverse(input, i)
                    else:
                        i+=2
                        traverse(input,i)


calculateBestGini(transactionData[1:],[])
print("\n*****************************************Tree*****************************************")
print("Node Values Layout:  (Left(0)OrRight(1),isLeaf,AttributePosition,SeperatorValue,Label) \n")
print(str(tree))
traverse([1,2,90],0)
print("\n**************************************************************************************")