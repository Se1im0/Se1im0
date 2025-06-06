from Node import Node

class TreeNode(Node):
    """A class representing a node in a binary tree.

    This tree supports removing the leaf node of a given node.

    Attributes:
        key (any): The value of the node.
        left (TreeNode): The left child of the node.
        right (TreeNode): The right child of the node.
        parent (TreeNode): The parent of the node.
        value (any): The value associated with the key.
    """
    def __init__(self,key=None,value=None,left=None,right=None,parent=None):
        """Initialize a tree node instance.

        Args:
            key(any): The value of the node. Defaults to None.
            value (any): The value associated with the key. Defaults to None.
            left(TreeNode, optional): The left child of the node. Defaults to None.
            right(TreeNode, optional): The right child of the node. Defaults to None.
            parent(TreeNode, optional): The parent of the node. Defaults to None.
        """
        super().__init__(key)
        self._key = key
        self._left = None
        self._right = None
        self._parent = parent 
        self._value = value

       
    
    @property
    def key(self):
        """Get the key value of the node.

        Returns:
            any: The key value stored in the node.
        """
        return self._key
    
    @key.setter
    def key(self, key):
        """Set the key value of the node.

        Args:
            key (any): The new key value of the node.
        
        """
        self._key = key
    
    @property
    def left(self) -> 'TreeNode':
        """Get the left child of the node.

        Retruns:
            TreeNode: The left child of the node
        """
        return self._left
    
    @left.setter
    def left(self, node: 'TreeNode'):
        """Set the left child of the node and update parent references.

        Args:
            node (TreeNode or None): The node to set as left child.
        
        Raises:
            TypeError: If node is not a Node instance or is None.
        """
        if not isinstance(node,(Node,type(None))):
            raise TypeError
        if self._left is not None:
            self._left._parent = None
        self._left = node
        if node is not None:
            node._parent = self

        
    
    @property
    def right(self) -> 'TreeNode':
        """Get the right child of a node.

        Returns:
            TreeNode: The right child of the node.
        """
        return self._right

    @right.setter
    def right(self, node: 'TreeNode'):
        """Set the right child of the node and update parent references.

        Args:
            node (TreeNode or None): The node to set as the right child.
        
        Raises:
            TyperError: If the node is not a Node instance or is none.
        """
        if not isinstance(node,(Node,type(None))):
            raise TypeError
        if self._right is not None:
            self._right._parent = None
        self._right = node
        if node is not None:
            node._parent = self
        
    
    @property
    def parent(self) -> 'TreeNode':
        """Get the parent of the node.

        Returns:
            TreeNode: The parent of the node.
        """
        return self._parent
    
    @property
    def depth(self) -> int:
        """Get the depth of the node in the tree.
        
        The depth of a node is defined to be the number of nodes on the
        path from the node to the root. The root has a depth of 1.
        
        Returns:
            int: The depth of the node.
        """
        if self._parent is None:
            return 1
        return 1 + self._parent.depth
    
    @property
    def value(self) -> any:
        """Get the value associated with the node's key.

        Returns:
            any: The value stored in the node.
        """
        return self._value
    
    @value.setter
    def value(self, value):
        """Set the value of the node associated with the node's key.

        Args:
            value (any): The new value to be stored in the node.
        """
        self._value = value



    def remove_leaf(self, node: 'TreeNode') -> 'TreeNode':
        """Remove a leaf node that is a child of this node.

        Args:
            node (TreeNode): The leaf node to remove.
        
        Returns:
            TreeNode: The removed leaf node.
        
        Raises:
            TypeError: If node is not a TreeNode instance.
            ValueError: If node is not a leaf or is not a direct child of this node.
        """
        if not isinstance(node,TreeNode):
            raise TypeError

        is_left_child = self._left is node
        is_right_child = self._right is node

        if not(is_left_child or is_right_child):
            raise ValueError
        if node._left is not None or node._right is not None:
            raise ValueError
        if is_left_child: 
            self._left = None
        else:
            self._right = None
        
        node._parent = None
        
        return node

    

    def __repr__(self) -> str:
        """Get a string representation of this node.

        Returns:
            str: A string represenation of this node including the key,left, right and parent.
        
        """
        parent_str = self._parent._key if self._parent else 'None'

        return f"TreeNode (key={self._key}, left={self._left}, right={self._right}, parent={parent_str}"    
    