#include <iostream>
using namespace std;

typedef struct Node {
    int data;         // element to be stored
    Node* left;       // pointer to the left child
    Node* right;      // pointer to the right child
    int height;       // height of the element in the tree
    int size;         // number of nodes in the subtree rooted at this node

    Node(int data) {
        this->data = data;
        left = nullptr;
        right = nullptr;
        height = 1;
        size = 1;
    }
} Node;

class IndexedAVLTree {
private:
    int size;

    // Function which returns the height of a particular Node
    int getHeight(Node* node) {
        if (node == nullptr)
            return 0;
        return node->height;
    }

    // Returns the number of subtrees rooted at this Node
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

        // This condition checks if the left subtree of the current node is taller (balance factor > 1) and the new data to be
        // inserted is smaller than the data in the left child.
        if (balance > 1 && data < node->left->data)
            return rotateRight(node);

        // This condition checks if the right subtree of the current node is taller (balance factor < -1) and the new data to be
        // inserted is greater than the data in the right child.
        if (balance < -1 && data > node->right->data)
            return rotateLeft(node);

        // This condition checks if the left subtree of the current node is taller (balance factor > 1) and the new data to be
        // inserted is greater than the data in the left child.
        if (balance > 1 && data > node->left->data) {
            node->left = rotateLeft(node->left);
            return rotateRight(node);
        }

        // This condition checks if the right subtree of the current node is taller (balance factor < -1) and the new data to be
        // inserted is smaller than the data in the right child.
        if (balance < -1 && data < node->right->data) {
            node->right = rotateRight(node->right);
            return rotateLeft(node);
        }
        return node;
    }

    Node* deleteNode(Node* node, int data) {
        if (node == nullptr)
            return nullptr;

        if (data < node->data)
            node->left = deleteNode(node->left, data);
        else if (data > node->data)
            node->right = deleteNode(node->right, data);
        else {
            // Node to be deleted is found

            // Case 1: Node has no children or only one child
            if (node->left == nullptr || node->right == nullptr) {
                Node* temp = node->left ? node->left : node->right;

                if (temp == nullptr) {
                    // Node has no children
                    temp = node;
                    node = nullptr;
                } else {
                    // Node has one child
                    *node = *temp;
                }

                delete temp;
            } else {
                // Case 2: Node has two children
                Node* temp = findMinValueNode(node->right);
                node->data = temp->data;
                node->right = deleteNode(node->right, temp->data);
            }
        }

        // If the tree had only one node
        if (node == nullptr)
            return nullptr;

        updateHeight(node);
        updateSize(node);

        int balance = getBalanceFactor(node);

        // Rebalance the tree

        // Left Left Case
        if (balance > 1 && getBalanceFactor(node->left) >= 0)
            return rotateRight(node);

        // Left Right Case
        if (balance > 1 && getBalanceFactor(node->left) < 0) {
            node->left = rotateLeft(node->left);
            return rotateRight(node);
        }

        // Right Right Case
        if (balance < -1 && getBalanceFactor(node->right) <= 0)
            return rotateLeft(node);

        // Right Left Case
        if (balance < -1 && getBalanceFactor(node->right) > 0) {
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

    Node* findMinValueNode(Node* node) {
        Node* current = node;
        while (current->left != nullptr)
            current = current->left;
        return current;
    }

public:
    Node* root;
    IndexedAVLTree() {
        root = nullptr;
        size = 0;
    }

    void insert(int data) {
        root = insertNode(root, data);
        size++;
    }

    void deleteValue(int data) {
        root = deleteNode(root, data);
        size--;
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

    int getSize() {
        return size;
    }

    int getBalanceFactor(Node* node) {
        if (node == nullptr)
            return 0;
        return getHeight(node->left) - getHeight(node->right);
    }
};

int main() {
    IndexedAVLTree tree;
    tree.insert(4);
    tree.insert(2);
    tree.insert(1);
    tree.insert(3);
    tree.insert(6);
    tree.insert(5);
    tree.insert(7);

    cout << "Values in the Indexed AVL Tree: ";
    for (int i = 1; i <= tree.getSize(); i++)
        cout << tree.getValueByIndex(i) << " ";
    cout << endl;

    tree.deleteValue(3);

    cout << "Values in the Indexed AVL Tree after deleting 3: ";
    for (int i = 1; i <= tree.getSize(); i++)
        cout << tree.getValueByIndex(i) << " ";
    cout << endl;
    
    int bf=tree.getBalanceFactor(tree.root);
    cout<<"Balance factor is :"<<bf<<endl;
    return 0;
}
