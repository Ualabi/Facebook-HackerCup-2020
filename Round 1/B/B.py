# Link: https://www.facebook.com/codingcompetitions/hacker-cup/2020/round-1/problems/B

from time import time
import os
start_time = time()

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
# soutfile = 'sample-out.txt'

archivo = open(mydir+infile,'r',encoding='utf-8')
texto = archivo.read()
archivo.close()
text = texto.split('\n')
outtext = ''

mod = 10**9+7
T = int(text[0])
for t in range(T):
    N,M,K,S = map(int,text[1+t*5].split())
    P = list(map(int,text[2+t*5].split()))
    AP,BP,CP,DP = map(int,text[3+t*5].split())
    Q = list(map(int,text[4+t*5].split()))
    AQ,BQ,CQ,DQ = map(int,text[5+t*5].split())
    print('Case #{}: {} {}'.format(t+1,N,M))

    for x in range(N-K):
        P.append((AP*P[-2]+BP*P[-1]+CP)%DP+1)
        Q.append((AQ*Q[-2]+BQ*Q[-1]+CQ)%DQ+1)

    print(P)
    print(Q)

    ans = 0
    outtext += 'Case #{}: {}\n'.format(t+1,ans)

# print(outtext)
archivo = open(mydir+outfile,'w+',encoding='utf-8')
archivo.write(outtext)
archivo.close()

print("Elapsed time: {} seconds.".format(time() - start_time))
