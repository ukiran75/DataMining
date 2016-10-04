import Actions

TransactionsData=[('n','n','c','l'),(1,1,125,0),(0,0,100,0),(0,1,70,0),(1,0,120,0),(0,2,95,1),
              (0,0,60,0),(1,2,220,0),(0,1,85,1),(0,0,75,0),(0,1,91,1)]
decisionTree=[];
position=0;
tranList=[];
iTransData=TransactionsData;
def checkResult(res,transList,position):
    iTransData=[];
    if(res==2 and position<4):
        for i in transList:
            iTransData.append(TransactionsData[i])
        create(iTransData,position+1)
    elif(res==1):
        print('decision made')
    else:
        print('decision made')

    return

def create(transactionsData,position):
    if(transactionsData[0][position]=='n'):
        lists = Actions.createListsForNominal(iTransData, position)
        for tranList in lists:
            result=Actions.checkAttributes(tranList,position,transactionsData)
            checkResult(result,tranList,position)
    elif(transactionsData[0][position]=='c'):
        lists = Actions.createListsForContinuous(iTransData, position)
        for tranList in lists:
            result=Actions.checkAttributes(tranList,position,transactionsData)
            checkResult(result,tranList,position)
create(TransactionsData,0)

