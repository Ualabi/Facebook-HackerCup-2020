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
# soutfile = 'sample-out.txt'

archivo = open(mydir+infile,'r',encoding='utf-8')
texto = archivo.read()
archivo.close()
text = texto.split('\n')
outtext = ''

mod = 10**9+7
T = int(text[0])
for t in range(T):
    N, K = map(int,text[1+t*7].split())
    S = list(map(int,text[2+t*7].split()))
    AS,BS,CS,DS = map(int,text[3+t*7].split())
    X = list(map(int,text[4+t*7].split()))
    AX,BX,CX,DX = map(int,text[5+t*7].split())
    Y = list(map(int,text[6+t*7].split()))
    AY,BY,CY,DY = map(int,text[7+t*7].split())
    print('Case #{}: {}'.format(t+1,N))

    for x in range(N-K):
        S.append( ( AS*S[-2] + BS*S[-1] + CS )%DS )
        X.append( ( AX*X[-2] + BX*X[-1] + CX )%DX )
        Y.append( ( AY*Y[-2] + BY*Y[-1] + CY )%DY )

    ss, sx, sy = sum(S), sum(X), sum(Y)
    if ss < sx or sx+sy < ss:
        outtext += 'Case #{}: -1\n'.format(t+1)
    else:
        maxim, minim = 0, 0
        for i in range(N):
            # print(S[i],' : (',X[i],',',X[i]+Y[i],')')
            if S[i] < X[i]:
                minim += X[i] - S[i]
            elif X[i] + Y[i] < S[i]:
                maxim += S[i] - X[i] - Y[i]
        outtext += 'Case #{}: {}\n'.format(t+1,max(maxim,minim))

    # print('---------------------')
    # print(P,'\n\n')

# print(outtext)
archivo = open(mydir+outfile,'w+',encoding='utf-8')
archivo.write(outtext)
archivo.close()
