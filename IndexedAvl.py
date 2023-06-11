import pandas as pd
import timeit
class node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


class BST:
    def __init__(self, val):
        self.root = node(val)

    def insert(self, start, val):
        if start is None:
            start = node(val)
        elif val < start.data:
            if start.left is None:
                start.left = node(val)
            else:
                self.insert(start.left, val)
        else:
            if start.right is None:
                start.right = node(val)
            else:
                self.insert(start.right, val)
        self.change_to_self_balanced(start)

    def printio(self, start, trav):
        if start is not None:
            trav = self.printio(start.left, trav)
            trav += (str(start.data) + " ")
            trav = self.printio(start.right, trav)
        return trav

    def printpst(self, start, trav):
        if start is not None:
            trav = self.printio(start.left, trav)
            trav = self.printio(start.right, trav)
            trav += (str(start.data) + " ")
        return trav

    def printpro(self, start, trav):
        if start is not None:
            trav += (str(start.data) + " ")
            trav = self.printio(start.left, trav)
            trav = self.printio(start.right, trav)
        return trav

    def printCurrentlevel(self, root, level):
        if root is None:
            return
        if level == 1:
            print(root.data, end=" ")
        elif level > 1:
            self.printCurrentlevel(root.left, level - 1)
            self.printCurrentlevel(root.right, level - 1)

    def levelOrder(self, root):
        height = self.height(root)
        for i in range(1, height + 1):
            self.printCurrentlevel(root, i)

    def search(self, start, val):
        f = "Not Found"
        if start is None:
            f="Not Found"
        else:
            if start.data == val:
                f="Found"
            elif val < start.data:
                self.search(start.left, val)
            else:
                self.search(start.right, val)
        return f

    def height(self, start):
        if start is None:
            return 0
        else:
            return max(self.height(start.left), self.height(start.right)) + 1

    def check_if_self_balanced(self, start):#this function calcualtes balance factor and checks if the tree is self balanced or not
        if start is not None:
            lh = self.height(start.left)
            rh = self.height(start.right)
            if abs(lh - rh) <= 1:
                print("Yes, it is self-balanced")
            else:
                print("No, it is not self-balanced")

    def insert_balanced(self, start, L):
        if not L:
            return None
        mid = len(L) // 2
        start.data = L[mid]
        start.left = self.insert_balanced(node(None), L[:mid])
        start.right = self.insert_balanced(node(None), L[mid + 1:])
        return start

    def change_to_self_balanced(self, start):
        a = self.printio(start, "")
        L = a.split(" ")
        L.pop(-1)
        for i in range(len(L)):
            L[i] = int(L[i])
        self.insert_balanced(start, L)

    def inorderinsertion(self,start,L):
        if not L:
            return
        med=len(L)//2

    def getvaluebyindex(self,start,index):
        a = self.printio(start, "")
        L = a.split(" ")
        L.pop(-1)
        return L[index]

    def find_indices(self,A, item_to_find):
        indices = []
        for idx, value in enumerate(A):
            if int(value)==item_to_find:
                indices.append(idx)
        return indices



    def getindexbyvalue(self,start,value):
        a = self.printio(start, "")
        L = a.split(" ")
        L.pop(-1)
        A=self.find_indices(L, value)
        for i in A:
            print(i,end=" ")
        print()


    def delete(self,start,val):
        a = self.printio(start, "")
        L = a.split(" ")
        L.pop(-1)
        for i in range(len(L)):
            L[i] = int(L[i])
        L.remove(val)
        self.insert_balanced(start, L)





tree = BST(50)

df = pd.read_excel('C:/Users/viswa/AppData/Local/Programs/Python/Python310/Tools/DATA.xlsx', sheet_name=0)
mylist = df['A'].tolist()

# tree.check_if_self_balanced(tree.root)
# print(tree.printpro(tree.root, ''))
# tree.check_if_self_balanced(tree.root)
# print(tree.printio(tree.root, ''))
# print(tree.search(tree.root,10))
#
# print(tree.getvaluebyindex(tree.root, 2))
# tree.getindexbyvalue(tree.root, 4)
x=0
while(x==0):
    print("-------------------------------------")
    print("----------------MENU-----------------")
    print("--- 1: Insert data from excel     ---")
    print("--- 2: Delete data from memory    ---")
    print("--- 3: Search data from memory    ---")
    print("--- 4: Get value from indices     ---")
    print("--- 5: Get Indices from values    ---")
    print("--- 6: Print Inorder Traversal    ---")
    print("--- 7: Print Preorder Traversal   ---")
    print("--- 8: Print Postorder Traversal  ---")
    print("--- 9: Print levelorder Traversal ---")
    print("--- 10: Print Time for opertion   ---")
    print("-------------------------------------")
    print("-------------------------------------")
    option = int(input("Enter your option "))
    if option==1:
        for i in mylist:
            tree.insert(tree.root, i)
    elif option==2:
        val=int(input("Enter your value to be removed "))
        tree.delete(tree.root,val)
    elif option==3:
        val = int(input("Enter your value to be searched "))
        print(tree.search(tree.root,val))
    elif option==4:
        val=int(input("Enter index"))
        print(tree.getvaluebyindex(tree.root,val))
    elif option==5:
        val=int(input("Enter value"))
        tree.getindexbyvalue(tree.root,val)
    elif option==6:
        print(tree.printio(tree.root,''))
    elif option==7:
        print(tree.printpro(tree.root,''))
    elif option==8:
        print(tree.printpst(tree.root,''))
    elif option==9:
        tree.levelOrder(tree.root)
        print()
    elif option==10:
        # Measure the execution time of specific operations
        insert_time = timeit.timeit(lambda: tree.insert(tree.root, 100), number=1000)
        search_time = timeit.timeit(lambda: tree.search(tree.root, 10), number=1000)
        height_time = timeit.timeit(lambda: tree.height(tree.root), number=1000)
        print("Average Insertion Time:", insert_time)
        print("Average Search Time:", search_time)
        print("Average Height Time:", height_time)
    x=1
    x=int(input("Press 0 to go back to menu or any integer to exit "))


