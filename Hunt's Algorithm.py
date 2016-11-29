'''
Course     : Data Mining
Professor  : Dr Hung Chi Su
Name       : Uday Talapaneni
Id         : 50484403
Home Work# : HW3(Hunts Algorithm Implementation)
********************Main File*******************
'''

transactionData=[('n','n','c','l'),(1,1,125,0),(0,0,100,0),(0,1,70,0),(1,0,120,0),(0,2,95,1),
              (0,0,60,0),(1,2,220,0),(0,1,85,1),(0,0,75,0),(0,1,91,1)]
length=len(transactionData[0])-1
decisionTree=[]
defzeroCount = 0
defoneCount = 0
defVal=0;
label=['No','Yes','NA']

# calculating the default value of the label from the data
for data in transactionData[1:]:
     if (data[length] == 0):
          defzeroCount += 1
     elif (data[length] == 1):
         defoneCount += 1

if (defzeroCount > defoneCount):
  defVal=0;
elif (defzeroCount < defoneCount):
  defVal=1


#calculating the seperator value for node traversing
def calculateSeparatorValue(position):
    max=-10000000000;min=100000000000
    for transaction  in transactionData[1:]:
        if(transaction[position]<min):
            min=transaction[position]
        elif(transaction[position] > max):
            max=transaction[position]
    return (max+min)/2

#checking the purity of the node
def checkPurity(checkData):
    zeroCount=0;oneCount=0
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


#calculating the maximum lable value if there are no attribute to traverse
def calculateMaximun(checkData):
    zeroCount = 0;
    oneCount = 0
    for data in checkData:
        if (data[length] == 0):
            zeroCount += 1
        elif (data[length] == 1):
            oneCount += 1
    if (zeroCount>oneCount):
        return 0
    elif (zeroCount<oneCount):
        return 1
    else:
        return defVal

#inserting nodes into the decision tree
def insertIntoTree(purity,position,seperatorvalue,leaf,side,nodeData=[]):
      node=[leaf,label[purity],position,seperatorvalue,side]
      decisionTree.append(node)

#creating the nodes recursively
def createNodes(nodeData,position):
    seperatotValue=calculateSeparatorValue(position)
    end=0;
    if(position==(length-1)):
      end=1;
    leftNodeData=[]
    rightNodeData=[]
    for data in nodeData:
        if(data[position]<=seperatotValue):
            leftNodeData.append(data)
        else:
            rightNodeData.append(data)
    leftNodePurity=checkPurity(leftNodeData)
    rightNodePurity=checkPurity(rightNodeData)
    if(leftNodePurity==0 or leftNodePurity==1):
        insertIntoTree(leftNodePurity,position,seperatotValue,"Yes","left") #if the node is pure that is all the node data having the same label
    elif(leftNodePurity!=-1):
        if(end==1):
            #print("No attribute to traverse")
            maxLeafVal=calculateMaximun(leftNodeData) #if the node is not pure but we have no attributes to traverse we use the default max label value of the data
            insertIntoTree(maxLeafVal, position, seperatotValue, "Yes", "left")
        else:
            insertIntoTree(leftNodePurity, position, seperatotValue, "No", "left",leftNodeData)#if data is not pure insert it as a parent node and do recursion
            createNodes(leftNodeData,position+1)
    else:
        insertIntoTree(defVal, position, seperatotValue, "Yes", "left")#if  there is no data for the node insert the default node with label value as maxlabel value

    if (rightNodePurity == 0 or rightNodePurity == 1):
        insertIntoTree(rightNodePurity, position, seperatotValue, "Yes", "right") #if the node is pure that is all the node data having the same label
    elif (rightNodePurity != -1):
        if (end == 1):
           # print("No attribute to traverse")
           maxLeafVal = calculateMaximun(rightNodeData)#if the node is not pure but we have no attributes to traverse we use the default max label value of the data
           insertIntoTree(maxLeafVal, position, seperatotValue, "Yes", "right")
        else:
            insertIntoTree(rightNodePurity, position, seperatotValue, "No", "right",rightNodeData)#if data is not pure insert it as a parent node and do recursion
            createNodes(rightNodeData, position + 1)
    else:
        insertIntoTree(defVal,position,seperatotValue,"Yes","right")#if  there is no data for the node insert the default node with label value as maxlabel value

createNodes(transactionData[1:],0)

#printing the nodes of the decision tree including the default nodes
print("[isLeaf,lableValue,attributePos,seperatorvalue,nodeSide]");
for node in decisionTree:
  print(node)

fromPos=0
#traversing the tree for ouput
def traverse(input,position=0,fromPos=0):
    for node in decisionTree[fromPos:]:
        fromPos+=1
        if(node[2]==position):
            if ((input[position] <= node[3]) and (node[4] == 'left')):
               if (node[0] == "Yes"):
                print(node[1])
               else:
                traverse(input, position + 1,fromPos)
            elif((input[position]>node[3]) and (node[4]=='right')):
                if(node[0]=="Yes"):
                    print(node[1])
                else:
                    traverse(input,position+1,fromPos)


traverse([1,2,220])#change the list to different transaction






