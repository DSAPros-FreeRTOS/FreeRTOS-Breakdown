import tkinter as tk
from tkinter import messagebox


class Node:
    def __init__(self, data, index):
        self.data = data
        self.index = index
        self.left = None
        self.right = None
        self.height = 1
        self.size = 1


class IndexedAVLTree:
    def __init__(self):
        self.root = None

    def insert(self, data, index):
        self.root = self._insertNode(self.root, data, index)

    def _insertNode(self, node, data, index):
        if node is None:
            return Node(data, index)

        if data < node.data:
            node.left = self._insertNode(node.left, data, index)
        else:
            node.right = self._insertNode(node.right, data, index + 1 + self._getSize(node.left))

        node.height = 1 + max(self._getHeight(node.left), self._getHeight(node.right))
        node.size = 1 + self._getSize(node.left) + self._getSize(node.right)

        balance = self._getBalanceFactor(node)

        if balance > 1 and data < node.left.data:
            return self._rotateRight(node)

        if balance < -1 and data > node.right.data:
            return self._rotateLeft(node)

        if balance > 1 and data > node.left.data:
            node.left = self._rotateLeft(node.left)
            return self._rotateRight(node)

        if balance < -1 and data < node.right.data:
            node.right = self._rotateRight(node.right)
            return self._rotateLeft(node)

        return node


    def delete(self, data):
        self.root = self._deleteNode(self.root, data)

    def _deleteNode(self, root, data):
        if root is None:
            return root

        if data < root.data:
            root.left = self._deleteNode(root.left, data)
        elif data > root.data:
            root.right = self._deleteNode(root.right, data)
        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp

            temp = self._findMinValueNode(root.right)
            root.data = temp.data
            root.right = self._deleteNode(root.right, temp.data)

        self._updateHeight(root)
        self._updateSize(root)

        balance = self._getBalanceFactor(root)

        if balance > 1 and self._getBalanceFactor(root.left) >= 0:
            return self._rotateRight(root)

        if balance < -1 and self._getBalanceFactor(root.right) <= 0:
            return self._rotateLeft(root)

        if balance > 1 and self._getBalanceFactor(root.left) < 0:
            root.left = self._rotateLeft(root.left)
            return self._rotateRight(root)

        if balance < -1 and self._getBalanceFactor(root.right) > 0:
            root.right = self._rotateRight(root.right)
            return self._rotateLeft(root)

        return root

    def _findMinValueNode(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current
    
    def getIndexByValue(self, value):
        return self._getIndexByValue(self.root, value)

    def _getIndexByValue(self, node, value):
        if node is None:
            return None

        if node.data == value:
            left_size = self._getSize(node.left)
            return left_size

        if value < node.data:
            return self._getIndexByValue(node.left, value)
        else:
            left_size = self._getSize(node.left)
            right_size = self._getSize(node.right)
            return left_size + 1 + self._getIndexByValue(node.right, value)

    def getValueByIndex(self, index):
        return self._getValueByIndex(self.root, index)

    def _getValueByIndex(self, node, index):
        if node is None:
            return None

        left_size = self._getSize(node.left)

        if index == left_size:
            return node.data
        elif index < left_size:
            return self._getValueByIndex(node.left, index)
        else:
            return self._getValueByIndex(node.right, index - left_size - 1)

    def findIndex(self, index):
        return self._findNodeByIndex(self.root, index)

    def _findNodeByIndex(self, node, index):
        if node is None:
            return None

        leftSize = self._getSize(node.left)

        if index == leftSize:
            return node.data
        elif index < leftSize:
            return self._findNodeByIndex(node.left, index)
        else:
            return self._findNodeByIndex(node.right, index - leftSize - 1)

    def _getHeight(self, node):
        if node is None:
            return 0
        return node.height

    def _getSize(self, node):
        if node is None:
            return 0
        return node.size

    def _updateHeight(self, node):
        node.height = 1 + max(self._getHeight(node.left), self._getHeight(node.right))

    def _updateSize(self, node):
        if node is None:
            return

        node.size = 1 + self._getSize(node.left) + self._getSize(node.right)

        if node.left:
            node.left.index = node.index - self._getSize(node.right) - 1
        if node.right:
            node.right.index = node.index + self._getSize(node.left) + 1

    def _rotateRight(self, y):
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        self._updateHeight(y)
        self._updateHeight(x)

        self._updateSize(y)
        self._updateSize(x)

        return x

    def _rotateLeft(self, x):
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        self._updateHeight(x)
        self._updateHeight(y)

        self._updateSize(x)
        self._updateSize(y)

        return y

    def _getBalanceFactor(self, node):
        if node is None:
            return 0
        return self._getHeight(node.left) - self._getHeight(node.right)


class AVLTreeGUI:
    def __init__(self):
        self.avl_tree = IndexedAVLTree()
        self.window = tk.Tk()
        self.window.title("Indexed AVL Tree GUI")
        self.window.configure(bg="white")

        self.label_number = tk.Label(self.window, text="Node Value:")
        self.label_number.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.entry_number = tk.Entry(self.window)
        self.entry_number.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        self.button_insert = tk.Button(self.window, text="Insert", command=self.insertNode)
        self.button_insert.grid(row=0, column=2, padx=5, pady=5)

        self.label_index = tk.Label(self.window, text="Node Index:")
        self.label_index.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.entry_index = tk.Entry(self.window)
        self.entry_index.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        self.button_delete = tk.Button(self.window, text="Delete", command=self.deleteNode)
        self.button_delete.grid(row=1, column=2, padx=5, pady=5)

        self.button_find = tk.Button(self.window, text="Find", command=self.findNodeByIndex)
        self.button_find.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

        self.canvas = tk.Canvas(self.window, width=800, height=600)
        self.canvas.configure(bg='white')
        self.canvas.configure(border=None)
        self.canvas.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

        self.button_array = tk.Button(self.window, text="Show Array", command=self.displayArray)
        self.button_array.grid(row=2, column=2, padx=5, pady=5)

        self.array_window = None  # Placeholder for the array display window

        self.button_get_index = tk.Button(self.window, text="Get Index", command=self.getIndexByValue)
        self.button_get_index.grid(row=2, column=0, padx=5, pady=5)

        self.button_get_value = tk.Button(self.window, text="Get Value", command=self.getValueByIndex)
        self.button_get_value.grid(row=2, column=1, padx=5, pady=5)

        

        self.window.mainloop()


    def deleteNode(self):
        value = self.entry_number.get()
        if value.isnumeric():
            value = int(value)
            self.avl_tree.delete(value)
            self.visualizeTree()
            self.clearEntry()
        else:
            messagebox.showerror("Error", "Invalid input! Please enter a number.")

    def findNodeByIndex(self):
        index = self.entry_index.get()
        if index.isnumeric():
            index = int(index)
            result = self.avl_tree.findIndex(index)
            if result is not None:
                messagebox.showinfo("Find Result", f"The node value at index {index} is {result}.")
            else:
                messagebox.showinfo("Find Result", f"No node found at index {index}.")
            self.clearEntry()
        else:
            messagebox.showerror("Error", "Invalid input! Please enter a number.")

    def clearEntry(self):
        self.entry_number.delete(0, tk.END)
        self.entry_index.delete(0, tk.END)

    def visualizeTree(self):
        self.canvas.delete("all")
        if self.avl_tree.root is None:
            return
        self._visualizeNode(self.avl_tree.root, 400, 50, 200, 0)
    
    def _visualizeNode(self, node, x, y, gap, index):
        radius = 20
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="white")
        self.canvas.create_text(x, y, text=f"{node.data}", fill="black")

        if node.left is not None:
            left_index = index - self.avl_tree._getSize(node.left) - 1
            self.canvas.create_line(x, y + radius, x - gap, y + 100, width=2)
            self._visualizeNode(node.left, x - gap, y + 100, gap // 2, left_index)

        if node.right is not None:
            right_index = index + self.avl_tree._getSize(node.right)
            self.canvas.create_line(x, y + radius, x + gap, y + 100, width=2)
            self._visualizeNode(node.right, x + gap, y + 100, gap // 2, right_index)


    def insertNode(self):
        value = self.entry_number.get()
        if value.isnumeric():
            value = int(value)
            index = self.avl_tree._getSize(self.avl_tree.root) + 1
            self.avl_tree.insert(value, index)
            self.visualizeTree()
            self.clearEntry()
        else:
            messagebox.showerror("Error", "Invalid input! Please enter a number.")
    

    def getIndexByValue(self):
        value = self.entry_number.get()
        if value.isnumeric():
            value = int(value)
            index = self.avl_tree.getIndexByValue(value)
            if index is not None:
                messagebox.showinfo("Get Index Result", f"The index of node with value {value} is {index}.")
            else:
                messagebox.showinfo("Get Index Result", f"No node found with value {value}.")
            self.clearEntry()
        else:
            messagebox.showerror("Error", "Invalid input! Please enter a number.")
    
    def getValueByIndex(self):
        index = self.entry_index.get()
        if index.isnumeric():
            index = int(index)
            value = self.avl_tree.getValueByIndex(index)
            if value is not None:
                messagebox.showinfo("Get Value Result", f"The value at index {index} is {value}.")
            else:
                messagebox.showinfo("Get Value Result", f"No node found at index {index}.")
            self.clearEntry()
        else:
            messagebox.showerror("Error", "Invalid input! Please enter a number.")
        
    
    def displayArray(self):
        if self.array_window is not None:
            self.array_window.destroy()

        self.array_window = tk.Toplevel(self.window)
        self.array_window.title("AVL Tree Array")
        
        self.array_window.geometry("400x300")
        self.array_window.configure(bg='white')

        array_frame = tk.Frame(self.array_window)
        array_frame.pack(fill=tk.BOTH, expand=True)

        array_frame.configure(bg='white')

        array_label = tk.Label(array_frame, text="AVL Tree Array", font=("Helvetica", 16, "bold"))
        array_label.pack(pady=10)

        array_label.configure(bg='white')

        tree_array = self.getTreeArray(self.avl_tree.root)

        for i, value in enumerate(tree_array):
            array_text = tk.Text(array_frame, height=1, width=50)
            array_text.configure(bg="white")
            array_text.insert(tk.END, f"Index {i}: {value}")
            array_text.pack()
    



    def getTreeArray(self, node):
        if node is None:
            return []

        left_array = self.getTreeArray(node.left)
        right_array = self.getTreeArray(node.right)

        return left_array + [node.data] + right_array


if __name__ == "__main__":
    AVLTreeGUI()`
