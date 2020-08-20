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

if finalin == None:
    if validationin == None:
        infile = samplein
        outfile = 'sample-out.txt'
    else:
        infile = validationin
        outfile = 'validation-out.txt'
else:
    infile = finalin
    outfile = 'final-out.txt'

archivo = open(mydir+infile,'r',encoding='utf-8')
texto = archivo.read()
archivo.close()
text = texto.split('\n')
outtext = ''

mod = 10**9+7
T = int(text[0])
for t in range(T):
    N, K, W = map(int,text[1+t*5].split())
    L = list(map(int,text[2+t*5].split()))
    AL,BL,CL,DL = map(int,text[3+t*5].split())
    H = list(map(int,text[4+t*5].split()))
    AH,BH,CH,DH = map(int,text[5+t*5].split())
    
    if K < N:
        for x in range(N-K):
            L.append( ( AL*L[-2] + BL*L[-1] + CL )%DL + 1 )
            H.append( ( AH*H[-2] + BH*H[-1] + CH )%DH + 1 )

    total = 1
    h = [0] * (L[-1]+W+1)
    suma, curr = 0, 0
    rect = [0,0,0]
    # P = []
    for i in range(N):
        if rect[1] < L[i]:
            suma += curr
            for x in range(L[i],L[i]+W+1):
                h[x] = H[i]
            rect = [L[i],L[i]+W, H[i]]
            curr = 2*W + 2*H[i]
        else:
            I,D,A = rect
            change = (H[i] - h[L[i]]) if H[i] > h[L[i]] else 0
            for x in range(L[i]+1,L[i]+W+1):
                if H[i] > h[x]:
                    h[x] = H[i]

            rect = [I,L[i]+W,A+change]
            curr = 2*(L[i]+W-I) + 2*(A+change)

        # P.append(suma + curr)
        total = (total*(suma + curr))%mod
    
    # print(L)
    # print(H)
    # print(P)
    # print(total,'\n')
    outtext += 'Case #{}: {}\n'.format(t+1,total)
    print(t+1,N)

# print(outtext)
archivo = open(mydir+outfile,'w+',encoding='utf-8')
archivo.write(outtext)
archivo.close()