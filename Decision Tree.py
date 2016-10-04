'''
Course     : Data Mining
Professor  : Dr Hung Chi Su
Name       : Uday Talapaneni
Id         : 50484403
Home Work# : HW3(Hunts Algorithm Implementation)
********************Main File*******************
'''

import Actions

#Transaction Data
TransactionsData=[('n','n','c','l'),(1,1,125,0),(0,0,100,0),(0,1,70,0),(1,0,120,0),(0,2,95,1),
              (0,0,60,0),(1,2,220,0),(0,1,85,1),(0,0,75,0),(0,1,91,1)]
decisionTree=[]#Decision Tree Initialization
inputData=[] # Input Data list

#placing the decision nodes into the decision tree
def placeTheDecision(res,lispos,pos):
    if(res==1): # res==1 means the node was pure with 1
        if(lispos==0):
            decisionTree.append([pos,0,1])# if it is left node(ie attribute value is 0) put it on left side(0) and append to list
        else:
            decisionTree.append([pos,1,1])#else put it on right side(1) and append to list
    elif(res==2): # res==-1 means the node was impure
        if (lispos == 0):
            decisionTree.append([pos, 0, -1])# if it is left node(ie attribute value is 0) put it on left side(0) and append to list
        else:
            decisionTree.append([pos, 1, -1])#else put it on right side(1) and append to list
    else:  # res==0 means the node was pure with 0
        if (lispos == 0):
            decisionTree.append([pos, 0, 0])# if it is left node(ie attribute value is 0) put it on left side(0) and append to list
        else:
            decisionTree.append([pos, 1, 0])#else put it on right side(1) and append to list

#checking the pure/impure result from checkLists methods
def checkResult(res,transList,position,lispos):
    iTransData = [] #intermediate transaction data initialization
    if(res==2 and position<3):# checking if the result was impure(2) and checking if it has attributes to make decisions furthur
        iTransData=transList
        placeTheDecision(res,lispos,position)#placing the node in decision tree
        position += 1 #increment the position ie take the next attribute to make decision
        createNodesForTransactions(iTransData, position)#As the node was impure call create node on next attribute and the on the transactions till that node

    elif(res==1):#Result was pure with 1's
        placeTheDecision(res,lispos,position)#placing the node in decision tree
    else:#Result was pure with 0's
        placeTheDecision(res,lispos,position)#placing the node in decision tree
    return

# creating the nodes(decisions) for the transactions till that nodes
def createNodesForTransactions(transactions, position):
    if(TransactionsData[0][position]=='n'):#if the attribute is nominal
        lists = Actions.createListsForNominal(transactions, position)#call the method that creates lists for the nominal attribute
        lisPos = 0#Initialize the lisPos to 0 for placing the value left or right in the node(0-left,1-right)
        for tranList in lists:
            result=Actions.checkAttributes(tranList,TransactionsData)# method to check if the list is pure(0/1) or not(2)
            checkResult(result,tranList,position,lisPos)#checking the result if we need recusion that is furthur split or not
            lisPos+=1
    elif(TransactionsData[0][position]=='c'):#if the attribute is continuous
        lists = Actions.createListsForContinuous(transactions, position) #call the method that creates lists for the continuous attribute
        lisPos = 0#Initialize the lisPos to 0 for placing the value left or right in the node(0-left,1-right)
        for tranList in lists:
            result=Actions.checkAttributes(tranList,TransactionsData)# method to check if the list is pure(0/1) or not(2)
            checkResult(result,tranList,position,lisPos)#checking the result if we need recusion that is furthur split or not
            lisPos+=1

#Analyze the input againest the decision tree to find the lable
def checkDecisionTree(attr,pos):
    for node in range(pos,len(decisionTree)):#from the node position to the subsequent nodes only not the whole tree
        if (decisionTree[node][0] == attr):# Checking the node which makes decision on the given attribute only
            if(decisionTree[node][1]==inputData[attr]):#Checking the data in the input is equal to data in the node
                if(decisionTree[node][2]==1):#checking if the node child is pure(ie leaf) and has value of lable 1
                    print(1)
                    exit(1)#If we had leaf node stop the program
                elif(decisionTree[node][2]==-1):#checking if the node child is impurepure and furthur evaluation of input required
                    attr+=1
                    pos=node
                    checkDecisionTree(attr,pos)##Cal the checkDecion on next node and only taking the next decision nodes into consideration
                else:#checking if the node child is pure(ie leaf) and has value of lable 0
                    print(0)
                    exit(1)#If we had leaf node stop the program

createNodesForTransactions([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 0)#Create nodes for the transactions inital call
print (decisionTree)#Print the decision tree
print('Enter the refund status(1:yes,0:no)')#Take input from the User
inputData.append(int(input()))
print('Enter marriage status(0:married,1:single,2:divorce):')#Take input from the User
if(int(input())==0):#if single append 0 because of the constraints in the test data from the PPT
    inputData.append(0)
else:#if married or divorse append 1
    inputData.append(1)
print('Enter the taxable income:')#Take input from the User seperated by 'space'
if(int(input())<=80): # As we take the average of the transaction at the node for continuous attribute we are unable to create the list so we hardcoded
    inputData.append(0)
else:
    inputData.append(1)
print("The lable 'CHEAT' for the input data is(1:Yes,0:NO):")
checkDecisionTree(0,0)#Make the decion for the lable from the input