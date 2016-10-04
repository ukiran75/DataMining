#Transaction Data
TransactionsData=[('n','n','c','l'),(1,1,125,0),(0,0,100,0),(0,1,70,0),(1,0,120,0),(0,2,95,1),
              (0,0,60,0),(1,2,220,0),(0,1,85,1),(0,0,75,0),(0,1,91,1)]

#creating lists from the transactions till that node for ni=ominal attribute
def createListsForNominal(transactions,position):
    lists=[[],[]]#creating two lists one for (0) and one for other values for the values in the attribute
    for i in transactions:
        if (TransactionsData[i][position] == 0):#if attribute value is 0 in the transaction add to the first list
            lists[0].append(i)
        else:#if attribute value is other than 0  in the transaction add to the second list
            lists[1].append(i)
    return lists

#creating lists from the transactions till that node for continous attribute
def createListsForContinuous(transactions,position):
    lists=[[],[]]
    sum=0;count=0
    for i in transactions:
        sum+=TransactionsData[i][position]#Summing the contionous attribute values for finding the average (But we are not usiing it)
        count+=1
    sum=sum/count
    for i in transactions:
        if (TransactionsData[i][position] <= 80):# As we take the average of the transaction at the node for continuous
                                                # attribute we are unable to create the list so we hardcoded
            lists[0].append(i)
        else:
            lists[1].append(i)
    return lists

#Check For the purity of the list at the node
def checkAttributes(listTran,transactions):
    countZero = 0
    countOne = 0
    for i in listTran:
        if (transactions[i][3] == 0):#Checking the value of the lable is zero for the transation in the list
            countZero += 1
        else:#Checking the value of the lable is one for the transation in the list
            countOne += 1
    if (countOne == len(listTran)):#Checking if the list is pure with 1's
       return 1
    elif (countZero == len(listTran)):#Checking if the list is pure with 0's
        return 0
    else:#Retunring 2 if the list is impure
      return 2
