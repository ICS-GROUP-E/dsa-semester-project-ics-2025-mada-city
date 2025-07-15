class BSTNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        self.root = self._insert(self.root, key)
        print(f"Inserted {key} into BST")

    def _insert(self, node, key):
        if node is None:
            return BSTNode(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)
        return node

    def search(self, key):
        found = self._search(self.root, key)
        if found:
            print(f"Found {key} in BST")
        else:
            print(f"{key} not found in BST")
        return found

    def _search(self, node, key):
        if node is None or node.key == key:
            return node
        if key < node.key:
            return self._search(node.left, key)
        return self._search(node.right, key)

    def delete(self, key):
        self.root, deleted = self._delete(self.root, key)
        print(f"{'Deleted' if deleted else 'Did not find'} {key} in BST")
        return deleted

    def _delete(self, node, key):
        if node is None:
            return node, False
        if key < node.key:
            node.left, deleted = self._delete(node.left, key)
            return node, deleted
        if key > node.key:
            node.right, deleted = self._delete(node.right, key)
            return node, deleted
        # node.key == key
        if node.left is None:
            return node.right, True
        if node.right is None:
            return node.left, True
        # two children: get inorder successor
        succ = node.right
        while succ.left:
            succ = succ.left
        node.key = succ.key
        node.right, _ = self._delete(node.right, succ.key)
        return node, True