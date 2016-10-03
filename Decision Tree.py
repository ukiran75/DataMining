import Actions

transactions=[('n','n','c','l'),(1,0,125,0),(0,1,100,0),(0,0,70,0),(1,1,120,0),(0,2,95,1),
              (0,1,60,0),(1,2,220,0),(0,0,85,1),(0,1,75,0),(0,0,91,1)]
position=0;
tranList=[];
lists=Actions.createLists(transactions,position)
print(lists)
for list in lists:
    result=Actions.checkNominalAttributes(list,transactions)
    print(list)
    print(result)
    if(result==2):
        position+=1
        for i in list:
            tranList.append(transactions[i])
        print(tranList)
        lists2=Actions.createLists(tranList,position)
        print(lists2)
        for list in lists2:
            result = Actions.checkNominalAttributes(list, transactions)
            print(result)
    tranList=[]
