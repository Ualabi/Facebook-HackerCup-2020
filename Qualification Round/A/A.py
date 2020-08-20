# Link: https://www.facebook.com/codingcompetitions/hacker-cup/2020/qualification-round/problems/A

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

T = int(text[0])
for t in range(T):
    N = int(text[1+t*3])
    I = text[2+t*3]
    O = text[3+t*3]
    M = [['N' for _ in range(N)] for __ in range(N)]
    
    for x in range(N):
        M[x][x] = 'Y'
        y = 0
        while x+y < N-1 and O[x+y] == 'Y':
            if I[x+y+1] == 'Y':
                M[x][x+y+1] = 'Y'
            else:
                break
            y += 1
        
        y = 0
        while 0 < x-y and O[x-y] == 'Y':
            if I[x-y-1] == 'Y':
                M[x][x-y-1] = 'Y'
            else:
                break
            y += 1

    outtext += 'Case #{}:\n'.format(t+1)
    for r in range(N):
        for c in range(N):
            outtext += M[r][c]
        outtext += '\n'

archivo = open(mydir+outfile,'w+',encoding='utf-8')
archivo.write(outtext)
archivo.close()
