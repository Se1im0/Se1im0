from TreeNode import TreeNode
from TreePrinter import print_tree

class MinHeap:
    """This class implements a linked binary min-heap.

    The heap will support insertion, extraction of the minimum element,
    and dynamic deletion of nodes by reference. The heap is a binary tree
    with nodes of type TreeNode.

    Attributes:
        root: Optional[TreeNode] the root node of the heap. If the heap
            is empty, this is None.
    """
    def __init__(self):
        """Creates a new, empty heap"""
        self.root: TreeNode = None

        # We use a protected attribute to store the current size
        # of the heap. This keeps us from needing to recompute the size.
        # Any delete or insert operations must update this protected
        # attribute to ensure the size remains correct!
        self._size = 0

    def __len__(self):
        """Return the number of nodes stored in the heap.

        Returns:
            int: the number of nodes in the heap.
        """
        
        return self._size

    def _swap_node_with_parent(self, x: TreeNode):
        """Swaps the given node with its parent in the heap.
       
        This method will actually swap the TreeNodes for a node
        and its parent, rather than simply swapping the values. As part
        of the swap, all links to parents and children will be altered
        so that afterwards the given node assumes the role of its parent
        and vice-versa in the linked tree structure. This means that
        all references to the node x should still refer to x after the swap.

        Args:
             x: a TreeNode object that should be swapped with its parent.
        
        Raises:
             ValueError: if x does not have a parent.
        """
        p = x.parent
        if p is None:
            raise ValueError("Node {x} has no parent")

        # Save the left and right children of p and x then break these
        # links from p to its children (including x)
        pr, pl = p.right, p.left
        p.right, p.left = None, None

        # Now we put x into the correct position with respect to p's
        # parent p2:
        p2 = p.parent
        # If p was the root, make x the root instead
        if p2 is None:
            self.root = x
        # If p was a left child of its parent, make x the left child
        # of this parent instead
        elif p2.left is p:
            p2.left = x
        # If p was a right child of its parent, make x a right child
        # instead
        else:
            p2.right = x

        # Next we need to exchange x and p's children One of these
        # will be x so we need to put that in the position that p was
        # in:

        # First, save x's old left and right children, then break
        # these links
        xl, xr = x.left, x.right
        x.left, x.right = None, None
        # Next, set x's new children to be p's old children, except...
        # ...if x was a left child of p, then p should be a left 
        # child of x
        if x is pl:
            x.left = p
            x.right = pr
        # ...if x was a right child of p, then p should be a right
        # child of x
        else:
            x.left = pl
            x.right = p
        # Finally, make p's new children x's old children
        p.left = xl
        p.right = xr


    def _replace_node_with_leaf(self, node: TreeNode, leaf: TreeNode):
        """Replaces the given node with the given leaf node.
       
        This method will first remove the leaf node from the linked
        structure. It will then rearrange the linked structure so that 
        the given leaf node takes the role of node: all of node's children
        will be made children of the leaf node, and node's parent will
        become the parent of the leaf node. After the operation, node will
        have no parent or children.

        Args:
             node: a TreeNode object that is the node we wish to replace.
             leaf: a TreeNode object that is a leaf node that we will
                 replace node with. This node should not have any children
                 and should have a parent. That is, it should be a leaf 
                 and also not the root of the heap.

        Returns:
             TreeNode: the node that was replaced. This node will have
                 no children and no parent after the replacement operation.

        Raises:
             ValueError: if leaf has any children or has no parent.
        """
        # Make sure leaf is a leaf and has a parent:
        if (leaf.left is not None) or (leaf.right is not None):
            raise ValueError("The specified node is not a leaf")
        if leaf.parent is None:
            raise ValueError("The specified node has no parent")
        # Remove the leaf node from its parent
        leaf.parent.remove_leaf(leaf)
        # Remove the children from the replaced node, and then assign them
        # as children to the leaf that is replacing node.
        nl, nr = node.left, node.right
        node.left, node.right = None, None
        leaf.left, leaf.right = nl, nr

        # Insert the leaf node into the same position as the removed
        # node:

        # Check if the removed node is the root. If so, we make
        # replacement leaf the root:
        if node.parent is None:
            self.root = leaf
        # Otherwise, make the leaf the left or right child of the replaced
        # node's parent, as appropriate:
        elif node is node.parent.left:
            node.parent.left = leaf
        else:
            node.parent.right = leaf
        return node


    def _get_node_at(self,ix) -> TreeNode:
        """Returns the node at position ix in the heap.

        Args:
            ix (int): The index of the node to retrieve.
        
        Returns:
            TreeNode: Node at given index.
        
        Raises:
            KeyError: If index is out of bounds or invalid.
        
        """
        
        if ix > self._size or ix <= 0:
            raise KeyError("Invalid index, Out of bounds!")
        
        path = [int(bit) for bit in bin(ix)[2:]] #Skip '0b' part
        

        current = self.root
        for direct in path[1:]: #Skip leading 1 (which just indicates the root)
            if direct == 0:
                current = current.left
            else:
                current = current.right
        return current

    def _add_leaf(self,leaf: TreeNode) -> TreeNode:
        """Adds a new leaf to the tree at the next available position.

        This method places the new leaf in the position that maintains the complete binary
        tree property - filling the tree level by level, left to right.

        Args:
            leaf (TreeNode): The node to be added as a leaf.
        
        Returns:
            TreeNode: The newly added leaf.
        
        Raises:
             TypeError: If the provided leaf is not a TreeNode instance.
             ValueError: If the leaf already has a parent, left, or right child.
        """
        if not isinstance(leaf,TreeNode):
            raise TypeError("Leaf is not a TreeNode!")
        
        if leaf.parent is not None or leaf.left is not None or leaf.right is not None:
            raise ValueError("Leaf cannot already have a parent, left, or right child.")

        # Special case: If the tree is empty, set the leaf as the root

        if self.root is None:
            self.root = leaf
            self._size = 1
            return leaf
        
        # Compute parent and assign the new leaf in the correct position

        index = self._size + 1
        parent_index = index // 2

        parent_node = self._get_node_at(parent_index)        

        if index % 2 == 0:
            parent_node.left = leaf
        else:
            parent_node.right = leaf

        self._size += 1
        
        return leaf


    def _sift_up(self,node: TreeNode):
        """Moves a node up the tree to maintain the min-heap property.

        Args:
            node (TreeNode): The node to sift up.
        """
        while node.parent is not None and node.key < node.parent.key:
            self._swap_node_with_parent(node)
        
       
            
    def _sift_down(self, node: TreeNode):
        """Moves a node down the tree to maintain the heap property.

        Args:
            node (TreeNode): The node to sift down.
        """

        while node is not None:
            smallest = node

            #Check if left child is smaller

            if node.left is not None and node.left.key < smallest.key:
                smallest = node.left

            #Check if right child is smaller

            if node.right is not None and node.right.key < smallest.key:
                smallest = node.right
            
            #If the node is already the smallest stop

            if smallest == node:
                break
                
            #Swap the node with smallest child

            self._swap_node_with_parent(smallest)

    
    def insert_node(self,node: TreeNode):
        """Inserts a node into the tree.

        This method places the node in the next available position to maintain complete
        binary tree property, then sifts the node up as needed in order to restore
        the min heap property.

        Args:
            node (TreeNode): The node to insert into the heap.

        Returns:
            TreeNode: The inserted node.

        Raises:
            ValueError: If the node is None.
        """

        if node is None:
            raise ValueError("Cannot insert a None node.")

        # Special case: If the tree is empty, set the node as the root

        if self.root is None:
            self.root = node
            self._size = 1
            return node
        
        # Compute parent and assign the node in the correct position

        index = self._size + 1
        parent_index = index // 2

        parent_node = self._get_node_at(parent_index)

        if index % 2 == 0:
            parent_node.left = node
        else:
            parent_node.right = node

        self._size += 1

        # Maintain the heap property

        if node is not None:
            self._sift_up(node)

        return node
    
    def insert(self,key,value=None) -> TreeNode:
        """Creates a new TreeNode with given key and value and inserts it into the heap.

        Args:
            key (any): The key of the new node.
            value (any, optional): The value associated with the key. Defaults to None.

        Returns:
            TreeNode: The newly created and inserted node.
        """

        new_node = TreeNode(key=key, value=value)
        
        return self.insert_node(new_node)
    

    def extract(self):
        """Removes and returns the minimum element (root) from the heap.

        Returns:
            TreeNode: The removed root node.

        Raises:
             KeyError: If the heap is empty.
        """

        if self.root is None:
            raise KeyError("Cannot extract from an empty heap!")
        
        original_node = self.root

        #Special case where heap has one node

        if self._size == 1:
            self.root = None
            self._size = 0
            return original_node
    
        # Replace the root with the last node and restore the heap property

        last_node = self._get_node_at(self._size)

        self._replace_node_with_leaf(self.root, last_node)

        self._sift_down(self.root)

        self._size += -1 

        return original_node
        
    
    def delete_node(self,node: TreeNode) -> TreeNode:
        """Deletes a specific node from the heap.

        Args:
            node (TreeNode): The node to be deleted from the heap.

        Returns:
            TreeNode: The removed node.

        Raises:
            KeyError: If the heap is empty or the node is not in the heap.
        """

        if self.root is None:
            raise KeyError("Cannot delete from an empty heap!")

        removed_node = node

        # Special case: If there's only one node in the heap

        if self._size == 1:
            if node is not self.root:
                raise KeyError("Node is not in the heap")
            self.root = None
            self._size = 0
            return removed_node


        # Get the last node in the heap

        last_node = self._get_node_at(self._size)

        if node is last_node:
            # If the node to delete is the last node, simply remove it

            if last_node.parent.left is last_node:
                last_node.parent.left = None
            else:
                last_node.parent.right = None
            
            self._size += -1 

            return removed_node
        
        # Replace the node to delete with the last node

        self._replace_node_with_leaf(node,last_node)
        new_node = last_node

        # Restore the heap property

        if new_node is not None and new_node.parent is not None and new_node.key < new_node.parent.key:
            self._sift_up(new_node)
        else:
            if new_node is not None:
                self._sift_down(new_node)
        
        self._size += -1 
        return removed_node