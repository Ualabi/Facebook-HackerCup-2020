# Link: https://www.facebook.com/codingcompetitions/hacker-cup/2020/round-1/problems/A3
# Damn problematic problem, it need 3 BBST and with ranges it got damn tricky

from time import time
import os
start_time = time()

def leftRotate(z): 
    y = z.right 
    T2 = y.left 
    y.left = z 
    z.right = T2 
    z.height = 1 + max(getHeight(z.left), getHeight(z.right)) 
    y.height = 1 + max(getHeight(y.left), getHeight(y.right)) 
    return y 

def rightRotate(z): 
    y = z.left 
    T3 = y.right 
    y.right = z 
    z.left = T3 
    z.height = 1 + max(getHeight(z.left), getHeight(z.right)) 
    y.height = 1 + max(getHeight(y.left), getHeight(y.right)) 
    return y 

def getHeight(root): 
    if not root: 
        return 0
    return root.height 

def getBalance(root): 
    if not root: 
        return 0
    return getHeight(root.left) - getHeight(root.right) 

def getMinValueNode(root): 
    if root is None or root.left is None: 
        return root 
    return getMinValueNode(root.left) 

class IntervalNode(): 
    def __init__(self, x1, x2): 
        self.val_from = x1
        self.val_to = x2
        self.left = None
        self.right = None
        self.height = 1
  
class IntervalTree(): 
    def __init__(self):
        self.head = None
        self.ST = StepTree()

    # It returns the intervals that overlaps with the interval [x1,x2]
    def search(self, root, x1, x2): #It can takes all Nodes O (N)
        if not root:
            return []
        else:
            if root.val_from <= x1 and x2 <= root.val_to:
                return [[root.val_from, root.val_to]]
            elif x1 <= root.val_from and root.val_from <= x2:
                return self.search(root.left, x1, x2) + [[root.val_from, root.val_to]] + self.search(root.right, x1, x2)
            elif x1 <= root.val_to and root.val_to <= x2:
                return self.search(root.left, x1, x2) + [[root.val_from, root.val_to]] + self.search(root.right, x1, x2)
            elif x2 < root.val_from:
                return self.search(root.left, x1, x2)
            elif root.val_to < x1:
                return self.search(root.right, x1, x2)

    # Return the change
    def insert(self, x1, x2, y): 
        change = 0
        changeaux = self.ST.insert(x1, x2, y)
        overlaps = self.search(self.head,x1,x2)
        if 0 < len(overlaps):
            if x1 < overlaps[0][0]:
                change += 2*(overlaps[0][0] - x1)
            else:
                x1 = overlaps[0][0]

            if overlaps[-1][-1] < x2:
                change += 2*(x2 - overlaps[-1][-1])
            else:
                x2 = overlaps[-1][-1]

            past = overlaps[0][1]
            self.head = self.delete(self.head, overlaps[0][0], overlaps[0][1])
            for x in range(1,len(overlaps)):
                change += 2*(overlaps[x][0]-past)
                past = overlaps[x][1]
                self.head = self.delete(self.head, overlaps[x][0], overlaps[x][1])
        else:
            change += 2*(x2-x1)
        self.head = self.insertNode(self.head,x1,x2)
        
        # print('INT:',change)
        # print(self.PreOrder(self.head)[:-2])
        return change+changeaux

    # It returns root of the modified subtree.     
    def insertNode(self,root,x1,x2):
        if not root:
            return IntervalNode(x1,x2) 
        elif x2 < root.val_from: 
            root.left = self.insertNode(root.left, x1, x2) 
        elif root.val_to < x1: 
            root.right = self.insertNode(root.right, x1, x2) 

        root.height = 1 + max(getHeight(root.left), getHeight(root.right)) 
        balance = getBalance(root) 
        if balance > 1 and x2 < root.left.val_from: 
            return rightRotate(root) 
        if balance < -1 and x1 > root.right.val_to: 
            return leftRotate(root) 
        if balance > 1 and x1 > root.left.val_to: 
            root.left = leftRotate(root.left) 
            return rightRotate(root) 
        if balance < -1 and x2 < root.right.val_from: 
            root.right = rightRotate(root.right) 
            return leftRotate(root) 
        return root

    # It returns root of the modified subtree. 
    def delete(self, root, x1, x2): 
        if not root: 
            return root 
        elif root.val_from == x1 and root.val_to == x2:
            if root.left is None: 
                temp = root.right 
                root = None
                return temp 
            elif root.right is None: 
                temp = root.left 
                root = None
                return temp 
            temp = getMinValueNode(root.right) 
            root.val_from = temp.val_from
            root.val_to = temp.val_to
            root.right = self.delete(root.right, temp.val_from, temp.val_to) 
        elif x2 < root.val_from: 
            root.left = self.delete(root.left, x1, x2) 
        elif root.val_to < x1: 
            root.right = self.delete(root.right, x1, x2) 
  
        if root is None: 
            return root 
        root.height = 1 + max(getHeight(root.left), getHeight(root.right)) 
        balance = getBalance(root) 
        if balance > 1 and getBalance(root.left) >= 0: 
            return rightRotate(root) 
        if balance < -1 and getBalance(root.right) <= 0: 
            return leftRotate(root) 
        if balance > 1 and getBalance(root.left) < 0: 
            root.left = leftRotate(root.left) 
            return rightRotate(root) 
        if balance < -1 and getBalance(root.right) > 0: 
            root.right = rightRotate(root.right) 
            return leftRotate(root) 
        return root 

    # It returns the string of the PreOrder
    def PreOrder(self, Node):
        if not Node:
            return ''
        else:
            return self.PreOrder(Node.left) + '({}, {}), '.format(Node.val_from, Node.val_to) + self.PreOrder(Node.right)

class StepNode():
    def __init__(self, x, y1, y2): 
        self.val_x = x
        self.val_yp = y1
        self.val_yn = y2
        self.left = None
        self.right = None
        self.height = 1

class StepTree():
    def __init__(self):
        self.head = None
        self.LT = LevelTree()

    # It returns the intervals that overlaps with the interval [x1,x2]
    def search(self, root, x1, x2): #It can takes all Nodes O (N)
        if not root:
            return []
        else:
            if x1 <= root.val_x and root.val_x <= x2:
                return self.search(root.left, x1, x2) + [ [root.val_x, root.val_yp, root.val_yn] ] + self.search(root.right, x1, x2)
            elif x2 < root.val_x:
                return self.search(root.left, x1, x2)
            elif root.val_x < x1:
                return self.search(root.right, x1, x2)

    # It returns change
    def insert(self, x1, x2, y):
        change = 0
        [changeaux, past_left_val, past_right_val] = self.LT.insert(x1, x2, y)
        overlaps = self.search(self.head,x1,x2)
        if 1 < len(overlaps):
            if x1 == overlaps[0][0]:
                if overlaps[0][2] < overlaps[0][1]:
                    change -= abs(overlaps[0][1]-overlaps[0][2])
                else:
                    past_left_val = overlaps[0][1]
            elif x1 < overlaps[0][0]:
                change -= abs(overlaps[0][1]-overlaps[0][2])
            self.head = self.delete(self.head, overlaps[0][0])

            if overlaps[-1][0] == x2:
                if overlaps[-1][1] < overlaps[-1][2]:
                    change -= abs(overlaps[-1][1]-overlaps[-1][2])
                else:
                    past_right_val = overlaps[-1][2]
            elif overlaps[-1][0] < x2:
                change -= abs(overlaps[-1][1]-overlaps[-1][2])
            self.head = self.delete(self.head, overlaps[-1][0])

            for x in range(1,len(overlaps)-1):
                change -= abs(overlaps[x][1]-overlaps[x][2])
                self.head = self.delete(self.head, overlaps[x][0])
            
        elif 1 == len(overlaps):
            if x1 == overlaps[0][0]:
                if overlaps[0][2] < overlaps[0][1]:
                    change -= abs(overlaps[0][1]-overlaps[0][2])
                else:
                    past_left_val = overlaps[0][1]
            elif x2 == overlaps[0][0]:
                if overlaps[0][1] < overlaps[0][2]:
                    change -= abs(overlaps[0][1]-overlaps[0][2])
                else:
                    past_right_val = overlaps[0][2]
            else:
                change -= abs(overlaps[0][1]-overlaps[0][2])
            self.head = self.delete(self.head, overlaps[0][0])
        
        if past_left_val < y:
            self.head = self.insertNode(self.head, x1, past_left_val, y)
        if past_right_val < y:
            self.head = self.insertNode(self.head, x2, y, past_right_val)

        # print('STP:', change)
        # print(self.PreOrder(self.head)[:-2])
        return change+changeaux

    # It returns root of the modified subtree.     
    def insertNode(self, root, x, y1, y2):
        if not root:
            return StepNode(x,y1,y2) 
        elif x < root.val_x: 
            root.left = self.insertNode(root.left, x, y1, y2) 
        elif root.val_x < x: 
            root.right = self.insertNode(root.right, x, y1, y2) 

        root.height = 1 + max(getHeight(root.left), getHeight(root.right)) 
        balance = getBalance(root) 
        if balance > 1 and x < root.left.val_x: 
            return rightRotate(root) 
        if balance < -1 and x > root.right.val_x: 
            return leftRotate(root) 
        if balance > 1 and x > root.left.val_x: 
            root.left = leftRotate(root.left) 
            return rightRotate(root) 
        if balance < -1 and x < root.right.val_x: 
            root.right = rightRotate(root.right) 
            return leftRotate(root) 
        return root

    # It returns root of the modified subtree. 
    def delete(self, root, x): 
        if not root: 
            return root 
        elif root.val_x == x:
            if root.left is None: 
                temp = root.right 
                root = None
                return temp 
            elif root.right is None: 
                temp = root.left 
                root = None
                return temp 
            temp = getMinValueNode(root.right) 
            root.val_x = temp.val_x
            root.val_yp = temp.val_yp
            root.val_yn = temp.val_yn
            root.right = self.delete(root.right, temp.val_x) 
        elif x < root.val_x: 
            root.left = self.delete(root.left, x) 
        elif root.val_x < x: 
            root.right = self.delete(root.right, x) 
  
        if root is None: 
            return root 
        root.height = 1 + max(getHeight(root.left), getHeight(root.right)) 
        balance = getBalance(root) 
        if balance > 1 and getBalance(root.left) >= 0: 
            return rightRotate(root) 
        if balance < -1 and getBalance(root.right) <= 0: 
            return leftRotate(root) 
        if balance > 1 and getBalance(root.left) < 0: 
            root.left = leftRotate(root.left) 
            return rightRotate(root) 
        if balance < -1 and getBalance(root.right) > 0: 
            root.right = rightRotate(root.right) 
            return leftRotate(root) 
        return root 

    # Return String of PreOrder
    def PreOrder(self, Node):
        if not Node:
            return ''
        else:
            return self.PreOrder(Node.left) + '{}:({},{}), '.format(Node.val_x,Node.val_yp,Node.val_yn) + self.PreOrder(Node.right)

class LevelNode():
    def __init__(self, x1, x2, y): 
        self.val_from = x1
        self.val_to = x2
        self.val_height = y
        self.left = None
        self.right = None
        self.height = 1

class LevelTree():
    def __init__(self):
        self.head = None

    # It returns the intervals that overlaps with the interval [x1,x2]
    def search(self, root, x1, x2): #It can takes all Nodes O (N)
        if not root:
            return []
        else:
            if root.val_from <= x1 and x2 <= root.val_to:
                return [[root.val_from, root.val_to, root.val_height]]
            elif x1 <= root.val_from and root.val_from <= x2:
                return self.search(root.left, x1, x2) + [[root.val_from, root.val_to, root.val_height]] + self.search(root.right, x1, x2)
            elif x1 <= root.val_to and root.val_to <= x2:
                return self.search(root.left, x1, x2) + [[root.val_from, root.val_to, root.val_height]] + self.search(root.right, x1, x2)
            elif x2 < root.val_from:
                return self.search(root.left, x1, x2)
            elif root.val_to < x1:
                return self.search(root.right, x1, x2)
            return []

    # It returns change and past values left and right
    def insert(self, x1, x2, y):
        change = 0
        overlaps = self.search(self.head,x1,x2)
        if 0 < len(overlaps):
            for [a,b,c] in overlaps:
                self.head = self.delete(self.head,a,b)
            
            past_left_val, past_right_val = 0, 0

            if overlaps[0][0] <= x1:
                past_left_val = overlaps[0][2]
                if overlaps[0][0] < x1:
                    if overlaps[0][2] == y:
                        x1 = overlaps[0][0]
                    else:
                        self.head = self.insertNode(self.head, overlaps[0][0], x1-1, overlaps[0][2])

            if x2 <= overlaps[-1][1]:
                past_right_val = overlaps[-1][2] 
                if x2 < overlaps[-1][1]:
                    if overlaps[-1][2] == y:
                        x2 = overlaps[-1][1]
                    else:
                        self.head = self.insertNode(self.head, x2+1, overlaps[-1][1], overlaps[-1][2])

            self.head = self.insertNode(self.head,x1,x2,y)
            # print('LVL:',2*y-past_left_val-past_right_val)
            # print(self.PreOrder(self.head)[:-2])
            return [2*y-past_left_val-past_right_val, past_left_val, past_right_val]
        else:
            self.head = self.insertNode(self.head,x1,x2,y)
            # print('LVL:',2*y)
            # print(self.PreOrder(self.head)[:-2])
            return [2*y, 0, 0]

    # It returns root of the modified subtree.     
    def insertNode(self, root, x1, x2, y):
        if not root:
            return LevelNode(x1,x2, y) 
        elif x2 < root.val_from: 
            root.left = self.insertNode(root.left, x1, x2, y) 
        elif root.val_to < x1: 
            root.right = self.insertNode(root.right, x1, x2, y) 

        root.height = 1 + max(getHeight(root.left), getHeight(root.right)) 
        balance = getBalance(root) 
        if balance > 1 and x2 < root.left.val_from: 
            return rightRotate(root) 
        if balance < -1 and x1 > root.right.val_to: 
            return leftRotate(root) 
        if balance > 1 and x1 > root.left.val_to: 
            root.left = leftRotate(root.left) 
            return rightRotate(root) 
        if balance < -1 and x2 < root.right.val_from: 
            root.right = rightRotate(root.right) 
            return leftRotate(root) 
        return root

    # It returns root of the modified subtree. 
    def delete(self, root, x1, x2): 
        if not root: 
            return root 
        elif root.val_from == x1 and root.val_to == x2:
            if root.left is None: 
                temp = root.right 
                root = None
                return temp 
            elif root.right is None: 
                temp = root.left 
                root = None
                return temp 
            temp = getMinValueNode(root.right) 
            root.val_from = temp.val_from
            root.val_to = temp.val_to
            root.val_height = temp.val_height
            root.right = self.delete(root.right, temp.val_from, temp.val_to) 
        elif x2 < root.val_from: 
            root.left = self.delete(root.left, x1, x2) 
        elif root.val_to < x1: 
            root.right = self.delete(root.right, x1, x2) 
  
        if root is None: 
            return root 
        root.height = 1 + max(getHeight(root.left), getHeight(root.right)) 
        balance = getBalance(root) 
        if balance > 1 and getBalance(root.left) >= 0: 
            return rightRotate(root) 
        if balance < -1 and getBalance(root.right) <= 0: 
            return leftRotate(root) 
        if balance > 1 and getBalance(root.left) < 0: 
            root.left = leftRotate(root.left) 
            return rightRotate(root) 
        if balance < -1 and getBalance(root.right) > 0: 
            root.right = rightRotate(root.right) 
            return leftRotate(root) 
        return root 

    # Return a String of PreOrder
    def PreOrder(self, Node):
        if not Node:
            return ''
        else:
            return self.PreOrder(Node.left) + '({}, {}):{}, '.format(Node.val_from, Node.val_to, Node.val_height) + self.PreOrder(Node.right)

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
    L = list(map(int,text[2+t*7].split()))
    AL,BL,CL,DL = map(int,text[3+t*7].split())
    W = list(map(int,text[4+t*7].split()))
    AW,BW,CW,DW = map(int,text[5+t*7].split())
    H = list(map(int,text[6+t*7].split()))
    AH,BH,CH,DH = map(int,text[7+t*7].split())
    print('Case #{}: {} rectangles'.format(t+1,N))

    for x in range(N-K):
        L.append( ( AL*L[-2] + BL*L[-1] + CL )%DL + 1 )
        W.append( ( AW*W[-2] + BW*W[-1] + CW )%DW + 1 )
        H.append( ( AH*H[-2] + BH*H[-1] + CH )%DH + 1 )

    P = []
    suma, total = 0, 1
    IT = IntervalTree()
    for i in range(0,N):
        change = IT.insert(L[i],L[i]+W[i],H[i])
        suma += change
        # print('Rango ({}, {}), Altura {} : {}\n'.format(L[i],L[i]+W[i],H[i],suma))
        P.append(suma)
        total = (total*suma)%mod
    outtext += 'Case #{}: {}\n'.format(t+1,total)
    print('Case #{}: {}'.format(t+1,total))
    # print('---------------------')
    # print(P,'\n\n')

# print(outtext)
archivo = open(mydir+outfile,'w+',encoding='utf-8')
archivo.write(outtext)
archivo.close()

print("Elapsed time: {} seconds.".format(time() - start_time))
