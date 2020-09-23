def bsearchright(mylist,target): #logN complexity
    l,r = 0,len(mylist)-1
    while l<=r:
        m = (l+r)//2
        if target < mylist[m]:
            r = m-1  
        else:
            l = m+1
    return r


def bsearchleft(mylist, target): #el indice del elemento que es igual o menor
    l = 0
    r = len(mylist)-1
    
    while l <= r:
        m = (l+r)//2
        if mylist[m] < target:
            l = m+1
        else:
            r = m-1
    return l

A = [1,2,3,4]
B = 0
print(bsearchright(A,B))