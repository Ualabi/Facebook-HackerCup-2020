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

# infile = samplein
# outfile = 'sample-out.txt'

archivo = open(mydir+infile,'r',encoding='utf-8')
texto = archivo.read()
archivo.close()
text = texto.split('\n')
outtext = ''

class Solution():
    def __init__(self):
        self.intervals = []
        self.levels = []
        self.steps = []

    #Bisearchs
    def findright(self,target):
        l,r = 0,len(self.intervals)-1
        while l<=r:
            m = (l+r)//2
            if target < self.intervals[m][0]:
                r = m-1  
            else:
                l = m+1
        return r

    def findleft(self,target):
        l,r = 0,len(self.intervals)-1
        while l<=r:
            m = (l+r)//2
            if self.intervals[m][1] < target:
                l = m+1
            else:
                r = m-1  
        return l

    def findLevelright(self,target):
        l,r = 0,len(self.levels)-1
        while l<=r:
            m = (l+r)//2
            if target < self.levels[m][0]:
                r = m-1  
            else:
                l = m+1
        return r

    def findLevelleft(self,target):
        l,r = 0,len(self.levels)-1
        while l<=r:
            m = (l+r)//2
            if self.levels[m][1] < target:
                l = m+1
            else:
                r = m-1  
        return l

    def findStepright(self,target):
        l,r = 0,len(self.steps)-1
        while l<=r:
            m = (l+r)//2
            if target < self.steps[m][0]:
                r = m-1  
            else:
                l = m+1
        return r

    def findStepleft(self,target):
        l,r = 0,len(self.steps)-1
        while l<=r:
            m = (l+r)//2
            if self.steps[m][0] < target:
                l = m+1
            else:
                r = m-1  
        return l

    def add(self,newInterval,height):
        start = newInterval[0]
        end = newInterval[1]
        left = self.findleft(start)
        right = self.findright(end)

        change = self.addStep(newInterval, height)
        if right < left:
            change += 2*(end-start)
            self.intervals.insert(left,[start, end])
        else:
            start = min(self.intervals[left][0],start)
            end = max(self.intervals[right][1],end)

            if newInterval[0] < self.intervals[left][0]:
                change += 2*(self.intervals[left][0] - newInterval[0])
            if self.intervals[right][1] < newInterval[1]:
                change += 2*(newInterval[1] - self.intervals[right][1])
            
            for x in range(left+1,right+1):
                change += 2*(self.intervals[x][0]-self.intervals[x-1][1])

            self.intervals = self.intervals[:left] + [[start, end]] + self.intervals[right+1:]
        return change
    
    def addLevel(self, newLevel, height):
        start = newLevel[0]
        end = newLevel[1]
        left = self.findLevelleft(start)
        right = self.findLevelright(end)
        
        if right < left:
            self.levels.insert(left,[start, end, height])
            return [2*height, 0, 0]
        else:
            med = [newLevel+[height]] 
            past_left_val, past_right_val = 0, 0

            if self.levels[left][0] <= newLevel[0]:
                past_left_val = self.levels[left][2]
                if self.levels[left][0] < newLevel[0]:
                    med = [ [self.levels[left][0], newLevel[0]-1, self.levels[left][2]] ] + med

            if newLevel[1] <= self.levels[right][1]:
                past_right_val = self.levels[right][2]
                if newLevel[1] < self.levels[right][1]:
                    med = med + [ [newLevel[1]+1, self.levels[right][1], self.levels[right][2]] ]

            self.levels = self.levels[:left] + med + self.levels[right+1:]
            return [2*height-past_left_val-past_right_val, past_left_val, past_right_val]

    def addStep(self,newStep, height):
        start = newStep[0]
        end = newStep[1]
        left = self.findStepleft(start)
        right = self.findStepright(end)

        [change, past_left_val, past_right_val] = self.addLevel(newStep, height)
        if right < left:    
            if past_left_val < height:
                self.steps.insert(left, [start, past_left_val, height])
            if past_right_val < height:
                self.steps.insert(left+1, [end, height, past_right_val])
        elif right==left:
            if self.steps[left][0] == newStep[0]:
                past_left_val = self.steps[left][1]
                if self.steps[left][2] < self.steps[left][1]:
                    change -= abs(self.steps[left][1]-self.steps[left][2])
            elif self.steps[right][0] == newStep[1]:
                past_right_val = self.steps[right][2]
                if self.steps[left][1] < self.steps[left][2]:
                    change -= abs(self.steps[left][1]-self.steps[left][2])
            else:  
                change -= abs(self.steps[left][1]-self.steps[left][2])
            
            med = []
            if past_left_val < height:
                med += [ [start, past_left_val, height] ]
            if past_right_val < height:
                med += [ [end, height, past_right_val] ]

            self.steps = self.steps[:left] + med + self.steps[right+1:]

        else:
            if self.steps[left][0] == newStep[0]:
                past_left_val = self.steps[left][1]
                if self.steps[left][2] < self.steps[left][1]:
                    change -= abs(self.steps[left][1]-self.steps[left][2])
            else:  
                change -= abs(self.steps[left][1]-self.steps[left][2])

            if self.steps[right][0] == newStep[1]:
                past_right_val = self.steps[right][2]
                if self.steps[right][1] < self.steps[right][2]:
                    change -= abs(self.steps[left][1]-self.steps[left][2])
            else:
                change -= abs(self.steps[right][1]-self.steps[right][2])

            for x in range(left+1,right):
                change -= abs(self.steps[x][1]-self.steps[x][2])
            
            med = []
            if past_left_val < height:
                med += [ [start, past_left_val, height] ]
            if past_right_val < height:
                med += [ [end, height, past_right_val] ]

            self.steps = self.steps[:left] + med + self.steps[right+1:]
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
    print(t+1,N)

    if K < N:
        for x in range(N-K):
            L.append( ( AL*L[-2] + BL*L[-1] + CL )%DL + 1 )
            W.append( ( AW*W[-2] + BW*W[-1] + CW )%DW + 1 )
            H.append( ( AH*H[-2] + BH*H[-1] + CH )%DH + 1 )

    suma = 0
    total = 1
    sol = Solution()
    P = []
    for i in range(0,N):
        change = sol.add([L[i],L[i]+W[i]],H[i])
        suma += change
        total = (total*suma)%mod
        P.append(suma)

        if i %1000==0:
            print('-',i)
    outtext += 'Case #{}: {}\n'.format(t+1,total)

print(outtext)
archivo = open(mydir+outfile,'w+',encoding='utf-8')
archivo.write(outtext)
archivo.close()