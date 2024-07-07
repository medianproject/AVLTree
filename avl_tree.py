import random
import streamlit as st

#start_time = time.time()

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1
        self.size = 1

class AVLTree:
    def __init__(self):
        self.root = None
        self.median_value = None

    def height(self, node):
        if not node:
            return 0
        return node.height

    def size(self, node):
        if not node:
            return 0
        return node.size

    def balance(self, node):
        if not node:
            return 0
        return self.height(node.left) - self.height(node.right)

    def update_height_and_size(self, node):
        if node:
            node.height = 1 + max(self.height(node.left), self.height(node.right))
            node.size = 1 + self.size(node.left) + self.size(node.right)

    def left_rotate(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        self.update_height_and_size(z)
        self.update_height_and_size(y)

        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        self.update_height_and_size(z)
        self.update_height_and_size(y)

        return y

    def insert(self, root, value):
        if not root:
            return Node(value)
        elif value < root.value:
            root.left = self.insert(root.left, value)
        else:
            root.right = self.insert(root.right, value)

        self.update_height_and_size(root)
        balance = self.balance(root)

        # Left rotation
        if balance > 1 and value < root.left.value:
            return self.right_rotate(root)

        # Right rotation
        if balance < -1 and value > root.right.value:
            return self.left_rotate(root)

        # Left-Right rotation
        if balance > 1 and value > root.left.value:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right-Left rotation
        if balance < -1 and value < root.right.value:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def appendNum(self, value):
        self.root = self.insert(self.root, value)
        self.median_value = self.find_median()

    def find_rank(self, node, R):
        if not node:
            return None

        left_size = self.size(node.left)

        if left_size + 1 == R:
            return node.value
        elif left_size >= R:
            return self.find_rank(node.left, R)
        else:
            return self.find_rank(node.right, R - left_size - 1)

    def find_median(self):
        if not self.root:
            return None

        n = self.size(self.root)
        if n % 2 == 1:
            # n is odd, return the middle element
            return self.find_rank(self.root, n // 2 + 1)
        else:
            # n is even, return the average of the two middle elements
            left_middle = self.find_rank(self.root, n // 2)
            right_middle = self.find_rank(self.root, n // 2 + 1)
            return (left_middle + right_middle) / 2

    def getMedian(self): # das ist O(1), da bei insert gleichzeitig auch findrank o(log(n)) angewandt wird
        return self.median_value

    # Helper function for in-order traversal
    def inorder_traversal(self, root):
        if root:
            return self.inorder_traversal(root.left) + [root.value] + self.inorder_traversal(root.right)
        else:
            return []

# Initialize session state for list_unsorted and tree
if 'list_unsorted' not in st.session_state:
    st.session_state.list_unsorted = []

if 'tree' not in st.session_state:
    st.session_state.tree = AVLTree()

if 'median_list' not in st.session_state:
    st.session_state.median_list = []

st.title("Median Calculator", anchor=False)
new_number=st.sidebar.button("New number")

if new_number:
    value = random.randint(1, 10)
    st.session_state.list_unsorted.append(value)
    st.session_state.tree.appendNum(value)
    list_sorted = st.session_state.tree.inorder_traversal(st.session_state.tree.root)
    current_median = st.session_state.tree.getMedian()# neu
    st.session_state.median_list.append(current_median)# neu

    st.write(f"Random integers: {st.session_state.list_unsorted}")
    st.write(f"Sorted random integers: {list_sorted}") 
    st.write(f"Current Median: {current_median}") # neu
    st.write(f"All Medians: {st.session_state.median_list}")
    st.line_chart(st.session_state.median_list, x_label="Iterations", y_label="Median values")
