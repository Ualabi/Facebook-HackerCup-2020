import os
mydir = os.path.dirname(os.path.abspath(__file__))
mychar = '\\' if '\\' in mydir else '/'
mydir += mychar
entries = os.listdir(mydir)
samplein, validationin, finalin = None, None, None

for xfile in entries:
    if 'input' in xfile and '.txt' == xfile[-4:]:
        if 'sample' in xfile:
            samplein = xfile
        elif 'validation' in xfile:
            validationin = xfile
        else:
            finalin = xfile
        
if finalin:
    infile = finalin
    outfile = 'final-out.txt'
elif validationin:
    infile = validationin
    outfile = 'validation-out.txt'
else:
    infile = samplein
    outfile = 'sample-out.txt'

archivo = open(mydir+infile,'r',encoding='utf-8')
texto = archivo.read()
archivo.close()
text = texto.split('\n')
outtext = ''

class Solution():
    def __init__(self):
        self.intervals = []
    
    def findright(self,target): #logN complexity
        l,r = 0,len(self.intervals)-1
        while l<=r:
            m = (l+r)//2
            if target < self.intervals[m][0]:
                r = m-1  
            else:
                l = m+1
        return r

    def findleft(self,target): #logN complexity
        l,r = 0,len(self.intervals)-1
        while l<=r:
            m = (l+r)//2
            if self.intervals[m][1] < target:
                l = m+1
            else:
                r = m-1  
        return l

    def add(self,newInterval,height):
        start = newInterval[0]
        end = newInterval[1]
        left = self.findleft(start) #logN complexity
        right = self.findright(end) #logN complexity

        change = 0
        if right < left:
            change = 2*(end-start) + 2*(height)
            self.intervals.insert(left,[start, end]) #N/2 average complexity
        else:
            start = min(self.intervals[left][0],start)
            end = max(self.intervals[right][1],end)

            if newInterval[0] < self.intervals[left][0]:
                change += 2*(self.intervals[left][0] - newInterval[0])
            if self.intervals[right][1] < newInterval[1]:
                change += 2*(newInterval[1] - self.intervals[right][1])
            
            for x in range(left+1,right+1):
                change += 2*(self.intervals[x][0]-self.intervals[x-1][1])
                change -= 2*height
            self.intervals = self.intervals[:left] + [[start, end]] + self.intervals[right+1:] #N/2 average complexity
        return change

mod = 10**9+7
T = int(text[0])
for t in range(T):
    N, K = map(int,text[1+t*7].split())
    L = list(map(int,text[2+t*7].split()))
    AL,BL,CL,DL = map(int,text[3+t*7].split())
    W = list(map(int,text[4+t*7].split()))
    AW,BW,CW,DW = map(int,text[5+t*7].split())
    H = list(map(int,text[6+t*7].split()))
    AH,BH,CH,DH = map(int,text[7+t*7].split())
    # print(t+1,N)

    if K < N:
        for x in range(N-K):
            L.append( ( AL*L[-2] + BL*L[-1] + CL )%DL + 1 )
            W.append( ( AW*W[-2] + BW*W[-1] + CW )%DW + 1 )
            H.append( ( AH*H[-2] + BH*H[-1] + CH )%DH + 1 )

    suma = 0
    total = 1
    sol = Solution()
    for i in range(0,N):
        change = sol.add([L[i],L[i]+W[i]],H[i])
        suma += change
        total = (total*suma)%mod

    outtext += 'Case #{}: {}\n'.format(t+1,total)

#print(outtext)
archivo = open(mydir+outfile,'w+',encoding='utf-8')
archivo.write(outtext)
archivo.close()