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
label=['No','Yes','NA']
decisionTree=[]

def calculateSeparatorValue(position):
    max=-1;min=100000000000
    for transaction  in transactionData[1:]:
        if(transaction[position]<min):
            min=transaction[position]
        elif(transaction[position] > max):
            max=transaction[position]
    return (max+min)/2

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
        return 0



def insertIntoTree(purity,position,seperatorvalue,leaf,side,nodeData=[]):
    if(leaf=='No'):
      node=[leaf,label[purity],position,seperatorvalue,side]
      decisionTree.append(node)




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
    if(leftNodePurity==0|leftNodePurity==1):
        insertIntoTree(leftNodePurity,position,seperatotValue,"yes","left")
    elif(leftNodePurity!=-1):
        if(end==1):
            #print("No attribute to traverse")
            maxLeafVal=calculateMaximun(leftNodeData)
            insertIntoTree(maxLeafVal, position, seperatotValue, "Yes", "left")
        else:
            insertIntoTree(leftNodePurity, position, seperatotValue, "No", "left",leftNodeData)
            createNodes(leftNodeData,position+1)


    if (rightNodePurity == 0 | rightNodePurity == 1):
        insertIntoTree(rightNodePurity, position, seperatotValue, "Yes", "right")
    elif (rightNodePurity != -1):
        if (end == 1):
           # print("No attribute to traverse")
           maxLeafVal = calculateMaximun(rightNodeData)
           insertIntoTree(maxLeafVal, position, seperatotValue, "Yes", "right")
        else:
            insertIntoTree(rightNodePurity, position, seperatotValue, "No", "right",rightNodeData)
            createNodes(rightNodeData, position + 1)

createNodes(transactionData[1:],0)

print(decisionTree)
