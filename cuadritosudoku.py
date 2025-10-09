
lista =[0]*72
c=0; p=2; rep=0
while (c<72):
    if((c-4)%9==0):
        lista[c]=5

    if(rep==2):
        p+=2
        rep=0
    if(c%9==0 ):
        lista[c]=p
        rep+=1
        num=int((15-p)/2)
        if(num%2==0):
            par=num
            imp=15-p-num
        else:
            imp=num
            par=15-p-num
        if(imp==5):
            imp+=2
            par-=2
        if(par==p):
            par+=4
            imp-=4
        if((c/9)%2==0):
            lista[c+8]=15-p-5
            lista[c+1]=imp
            lista[c+2]=par
            lista[c+5]=(15-lista[c+2]-lista[c+8])
            lista[c+3]=(15-5-lista[c+5])
            lista[c+6]=15-p-lista[c+3]
            lista[c+7]=15-lista[c+6]-lista[c+8]
        else:
            lista[c+8]=15-p-5
            lista[c+3]=imp
            lista[c+6]=par
            lista[c+7]=(15-lista[c+6]-lista[c+8])
            lista[c+1]=(15-5-lista[c+7])
            lista[c+2]=15-p-lista[c+1]
            lista[c+5]=15-lista[c+2]-lista[c+8]
            
    c+=1
h=0
for i in lista:
    if(h%3==0 and h%9!=0 and h!=0):
        print("\n")
    if(h%9==0 and h!=0):
        print("\n\n")
    print(i, end=" ")
    h+=1
