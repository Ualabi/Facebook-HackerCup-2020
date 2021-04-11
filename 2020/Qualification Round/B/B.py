# Link: https://www.facebook.com/codingcompetitions/hacker-cup/2020/qualification-round/problems/B

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
    N = int(text[1+t*2])
    S = text[2+t*2]
    freq = 0
    for s in S:
        if s == 'A':
            freq += 1
        else:
            freq -= 1

    outtext += 'Case #{}: '.format(t+1)
    if abs(freq) == 1:
        outtext += 'Y\n'
    else:
        outtext += 'N\n'

archivo = open(mydir+outfile,'w+',encoding='utf-8')
archivo.write(outtext)
archivo.close()
