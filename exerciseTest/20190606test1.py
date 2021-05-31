total=0
for i in range(1,61):
    for j in range(1,i):
        if((4/5)< (j/i) < (5/6) ):
            print(str(j)+' / '+str(i))
            total+=1

print(total)