def createListsForNominal(transactions,position):
    lists=[[],[]]
    for i in range(1, len(transactions)):
        if (transactions[i][position] == 0):
            lists[0].append(i)
        else:
            lists[1].append(i)
    return lists

def createListsForContinuous(transactions,position):
    print(transactions)
    print(position)
    lists=[[],[]]
    sum=0;count=0
    for i in range(1, len(transactions)):
        sum+=transactions[i][position]
        count+=1
    sum=sum/count
    for i in range(1, len(transactions)):
        if (transactions[i][position] <= 80):
            lists[0].append(i)
        else:
            lists[1].append(i)
    return lists

def checkAttributes(listTran,position,transactions):
    countZero = 0
    countOne = 0
    for i in listTran:
        if (transactions[i][3] == 0):
            countZero += 1
        else:
            countOne += 1
    if (countOne == len(listTran)):
       return 1
    elif (countZero == len(listTran)):
        return 0
    else:
      return 2
