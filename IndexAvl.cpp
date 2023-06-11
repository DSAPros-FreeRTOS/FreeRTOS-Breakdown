#include <iostream>
using namespace std;

typedef struct Node{
    int data; //element to be stored
    Node* left; //pointer to left child
    Node* right; //pointer to right child
    int height; //height of the element in the tree
    int size; // Number of nodes in the subtree rooted at this node

    Node(int data) {
        this->data = data;
        left = nullptr;
        right = nullptr;
        height = 1;
        size = 1;
    }
}Node;

class IndexedAVLTree {
private:
    
    int size;
    

    //function which returns the height of a particular Node
    int getHeight(Node* node) {
        if (node == nullptr)
            return 0;
        return node->height;
    }

    // returns the no of subtrees which are rooted at this Node
    int getSize(Node* node) {
        if (node == nullptr)
            return 0;
        return node->size;
    }
    
    

    void updateHeight(Node* node) {
        int leftHeight = getHeight(node->left);
        int rightHeight = getHeight(node->right);
        node->height = 1 + max(leftHeight, rightHeight);
    }

    void updateSize(Node* node) {
        int leftSize = getSize(node->left);
        int rightSize = getSize(node->right);
        node->size = 1 + leftSize + rightSize;
    }

    Node* rotateRight(Node* y) {
        Node* x = y->left;
        Node* T2 = x->right;

        // Perform rotation
        x->right = y;
        y->left = T2;

        // Update heights
        updateHeight(y);
        updateHeight(x);

        // Update sizes
        updateSize(y);
        updateSize(x);

        return x;
    }

    Node* rotateLeft(Node* x) {
        Node* y = x->right;
        Node* T2 = y->left;

        // Perform rotation
        y->left = x;
        x->right = T2;

        // Update heights
        updateHeight(x);
        updateHeight(y);

        // Update sizes
        updateSize(x);
        updateSize(y);

        return y;
    }

    Node* insertNode(Node* node, int data) {
        if (node == nullptr)
            return new Node(data);

        if (data < node->data)
            node->left = insertNode(node->left, data);
        else
            node->right = insertNode(node->right, data);

        updateHeight(node);
        updateSize(node);

        int balance = getBalanceFactor(node);

        //This condition checks if the left subtree of the current node is taller (balance factor > 1) and the new data to be
        //inserted is smaller than the data in the left child.
        if (balance > 1 && data < node->left->data)
            return rotateRight(node);

        //This condition checks if the right subtree of the current node is taller (balance factor < -1) and the new data to be 
        // inserted is greater than the data in the right child.
        if (balance < -1 && data > node->right->data)
            return rotateLeft(node);
            
        //This condition checks if the left subtree of the current node is taller (balance factor > 1) and the new data to be 
        // inserted is greater than the data in the left child.
        if (balance > 1 && data > node->left->data) {
            node->left = rotateLeft(node->left);
            return rotateRight(node);
        }
        
        //This condition checks if the right subtree of the current node is taller (balance factor < -1) and the new data to be 
        // inserted is smaller than the data in the right child.
        if (balance < -1 && data < node->right->data) {
            node->right = rotateRight(node->right);
            return rotateLeft(node);
        }
        return node;
    }

    int getIndexByValue(Node* node, int data, int& index) {
        if (node == nullptr)
            return -1;

        int leftIndex = getIndexByValue(node->left, data, index);
        if (leftIndex != -1)
            return leftIndex;

        if (node->data == data) {
            index = getSize(node->left) + 1;
            return index;
        }

        int rightIndex = getIndexByValue(node->right, data, index);
        if (rightIndex != -1)
            return rightIndex;

        return -1;
    }

    Node* getNodeByIndex(Node* node, int index) {
        if (node == nullptr)
            return nullptr;

        int leftSize = getSize(node->left);

        if (index <= leftSize)
            return getNodeByIndex(node->left, index);

        if (index == leftSize + 1)
            return node;

        return getNodeByIndex(node->right, index - leftSize - 1);
    }

public:
    Node* root;
    IndexedAVLTree() {
        root = nullptr;
        size=0;
    }

    void insert(int data) {
        root = insertNode(root, data);
        size++;
    }

    int getIndexByValue(int data) {
        int index = -1;
        getIndexByValue(root, data, index);
        return index;
    }

    int getValueByIndex(int index) {
        Node* node = getNodeByIndex(root, index);
        if (node != nullptr)
            return node->data;
        return -1;
    }
    int  getsize(){
        return size;
    }
    // for a balanced binary tree balanced factor must be either 0 or 1 , -1
    int getBalanceFactor(Node* node) {
        if (node == nullptr)
            return 0;
        return getHeight(node->left) - getHeight(node->right);
    }
};

int main() {
    IndexedAVLTree tree;

    // Inserting nodes into the indexed AVL tree
    tree.insert(4);
    tree.insert(5);
    tree.insert(8);
    tree.insert(11);
    tree.insert(12);
    tree.insert(17);
    tree.insert(18);
    tree.insert(1);
    tree.insert(2);
    tree.insert(10);

    // In-order traversal of the indexed AVL tree
    for (int i = 1; i <= tree.getsize(); i++) {
        int value = tree.getValueByIndex(i);
        cout << value << " ";
    }
    cout << endl;

    // Searching for a node by value
    int targetValue = 5;
    int targetIndex = tree.getIndexByValue(targetValue);
    cout << "Index of element " << targetValue << ": " << targetIndex << endl;
    
    int bal = tree.getBalanceFactor(tree.root);
    cout<<bal<<endl;

    return 0;
}
