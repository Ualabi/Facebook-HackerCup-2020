# Link: https://www.facebook.com/codingcompetitions/hacker-cup/2020/round-1/problems/A2
# Solution with O(N log N) with a BBST
# But somehow, it gets worse time that my O(N^2 log N) solution with an ordered list and bisearchs

class IntervalNode(): 
    def __init__(self, x1, x2): 
        self.val_from = x1
        self.val_to = x2
        self.left = None
        self.right = None
        self.height = 1
  
class PerimeterTree(): 
    def __init__(self):
        self.head = None

    # It returns the intervals that overlaps with the interval [x1,x2]
    def search(self, root, x1, x2): #It can takes all Nodes O (N)
        if not root:
            return []
        else:
            if root.val_from <= x1 and x2 <= root.val_to:
                None
            elif x1 <= root.val_from and root.val_from <= x2:
                return self.search(root.left, x1, x2) + [[root.val_from, root.val_to]] + self.search(root.right, x1, x2)
            elif x1 <= root.val_to and root.val_to <= x2:
                return self.search(root.left, x1, x2) + [[root.val_from, root.val_to]] + self.search(root.right, x1, x2)
            elif x2 < root.val_from:
                return self.search(root.left, x1, x2)
            elif root.val_to < x1:
                return self.search(root.right, x1, x2)

    def insert(self, x1, x2, rect_height): 
        change = 0
        overlaps = self.search(self.head,x1,x2)
        if type(overlaps) == list:
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
                    change -= 2*rect_height
                    past = overlaps[x][1]
                    self.head = self.delete(self.head, overlaps[x][0], overlaps[x][1])
            else:
                change = 2*(x2-x1) + 2*(rect_height)
                
            self.head = self.insertNode(self.head,x1,x2)

        return change

    # It returns root of the modified subtree.     
    def insertNode(self,root,x1,x2):
        if not root:
            return IntervalNode(x1,x2) 
        elif x2 < root.val_from: 
            root.left = self.insertNode(root.left, x1, x2) 
        elif root.val_to < x1: 
            root.right = self.insertNode(root.right, x1, x2) 

        root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right)) 
        balance = self.getBalance(root) 
  
        # If the node is unbalanced, then try out the 4 cases 
        # Case 1 - Left Left 
        if balance > 1 and x2 < root.left.val_from: 
            return self.rightRotate(root) 
  
        # Case 2 - Right Right 
        if balance < -1 and x1 > root.right.val_to: 
            return self.leftRotate(root) 
  
        # Case 3 - Left Right 
        if balance > 1 and x1 > root.left.val_to: 
            root.left = self.leftRotate(root.left) 
            return self.rightRotate(root) 
  
        # Case 4 - Right Left 
        if balance < -1 and x2 < root.right.val_from: 
            root.right = self.rightRotate(root.right) 
            return self.leftRotate(root) 
        
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
            temp = self.getMinValueNode(root.right) 
            root.val_from = temp.val_from
            root.val_to = temp.val_to
            root.right = self.delete(root.right, temp.val_from, temp.val_to) 
        elif x2 < root.val_from: 
            root.left = self.delete(root.left, x1, x2) 
        elif root.val_to < x1: 
            root.right = self.delete(root.right, x1, x2) 
  
        if root is None: 
            return root 
  
        root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right)) 
        balance = self.getBalance(root) 
  
        # If the node is unbalanced, then try out the 4 cases 
        # Case 1 - Left Left 
        if balance > 1 and self.getBalance(root.left) >= 0: 
            return self.rightRotate(root) 
  
        # Case 2 - Right Right 
        if balance < -1 and self.getBalance(root.right) <= 0: 
            return self.leftRotate(root) 
  
        # Case 3 - Left Right 
        if balance > 1 and self.getBalance(root.left) < 0: 
            root.left = self.leftRotate(root.left) 
            return self.rightRotate(root) 
  
        # Case 4 - Right Left 
        if balance < -1 and self.getBalance(root.right) > 0: 
            root.right = self.rightRotate(root.right) 
            return self.leftRotate(root) 
  
        return root 
  
    def leftRotate(self, z): 
        y = z.right 
        T2 = y.left 
        y.left = z 
        z.right = T2 
        z.height = 1 + max(self.getHeight(z.left), self.getHeight(z.right)) 
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right)) 
        return y 
  
    def rightRotate(self, z): 
        y = z.left 
        T3 = y.right 
        y.right = z 
        z.left = T3 
        z.height = 1 + max(self.getHeight(z.left), self.getHeight(z.right)) 
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right)) 
        return y 
  
    def getHeight(self, root): 
        if not root: 
            return 0
        return root.height 
  
    def getBalance(self, root): 
        if not root: 
            return 0
        return self.getHeight(root.left) - self.getHeight(root.right) 
  
    def getMinValueNode(self, root): 
        if root is None or root.left is None: 
            return root 
        return self.getMinValueNode(root.left) 

    # It returns a string of the values in Pre Order 
    def PreOrder(self, Node = None):
        if Node == None:
            Node = self.head

        if Node == None:
            print(" - ")
        else:
            if Node.left:
                S = self.PreOrder(Node.left) + ', ({}, {})'.format(Node.val_from, Node.val_to)
            else:
                S = "({}, {})".format(Node.val_from, Node.val_to)
            if Node.right:
                S += ', ' + self.PreOrder(Node.right)
            return S

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

infile = finalin
outfile = 'final-out2.txt'

# if finalin:
#     infile = finalin
#     outfile = 'final-out.txt'
# elif validationin:
#     infile = validationin
#     outfile = 'validation-out.txt'
# else:
#     infile = samplein
#     outfile = 'sample-out.txt'

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
    # print(t+1,N)

    if K < N:
        for x in range(N-K):
            L.append( ( AL*L[-2] + BL*L[-1] + CL )%DL + 1 )
            W.append( ( AW*W[-2] + BW*W[-1] + CW )%DW + 1 )
            H.append( ( AH*H[-2] + BH*H[-1] + CH )%DH + 1 )

    suma = 0
    total = 1
    PT = PerimeterTree()
    for i in range(0,N):
        change = PT.insert(L[i],L[i]+W[i],H[i])
        suma += change
        total = (total*suma)%mod
    outtext += 'Case #{}: {}\n'.format(t+1,total)

# print(outtext)
archivo = open(mydir+outfile,'w+',encoding='utf-8')
archivo.write(outtext)
archivo.close()
