import Actions

transactions=(('n','n','c','l'),(1,0,125,0),(0,1,100,0),(0,0,70,0),(1,1,120,0),(0,2,95,1),
              (0,1,60,0),(1,2,220,0),(0,0,85,1),(0,1,75,0),(0,0,91,1))

for i in range(0,len(transactions[0])):
    if(transactions[0][i]=='n'):
        Actions.calForNominal(transactions,i)
    elif(transactions[0][i]=='c'):
        Actions.calForCountinuous(transactions,i)
    else:
        print("record of type l")