from TreePrinter import print_tree
from TreeNode import TreeNode
from BST import BST

class BinarySearchTree(BST):
    def __init__(self,root=None):
        super().__init__()
        self._root = root
    
    @property
    def root(self):
        """Get the root of the tree."""
        return self._root
        
    @root.setter
    def root(self, node):
        """Set the root of the tree."""
        self._root = node


    def insert(self, key, value=None):
        """Insert a key-value pair into the binary search tree recursively."""
        def _insert_recursive(node, key, value):
            if node is None:
                return TreeNode(key=key, value=value)
        
            if key < node.key:
                node.left = _insert_recursive(node.left, key, value)
            elif key > node.key:
                node.right = _insert_recursive(node.right, key, value)
            else: 
                node.value = value
        
            return node
    
        self._root = _insert_recursive(self._root, key, value)
        
    
    def search(self,key):
        current = self._root
        while current is not None:
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                return current
        raise KeyError


    def get_value(self,key):
        current = self._root
        while current is not None:
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                return current.value
        raise KeyError

    
    def minimum_node(self,node):
        while node.left:
            node = node.left
        return node

    def delete(self,key):
        if self._root is None:
            raise KeyError
        
        self._root = self._delete_node(self._root, key)


    def _delete_node(self,node,key):
        if node is None:
            raise KeyError
        
        if key < node.key:
            node.left = self._delete_node(node.left,key)
        elif key > node.key:
            node.right = self._delete_node(node.right,key)
        else:
            if node.left is None and node.right is None:
                return None
            
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            
            min_node = self.minimum_node(node.right)
            node.key = min_node.key
            node.value = min_node.value

            node.right = self._delete_node(node.right, min_node.key)

        return node



