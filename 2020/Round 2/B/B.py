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
    aux = text[1+t].split()
    N, P = int(aux[0]), float(aux[1])
    print('Case #{}: {}, {}'.format(t+1,N,P))

    total, past = 1, 0
    for x in range(1,N):
        past += x
        total *= past
    
    


    # outtext += 'Case #{}: {}\n'.format(t+1,max(maxim,minim))
    # print('---------------------')
    # print(P,'\n\n')

# print(outtext)
# archivo = open(mydir+outfile,'w+',encoding='utf-8')
# archivo.write(outtext)
# archivo.close()
