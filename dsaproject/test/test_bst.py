from src.datastructures.bst import BinarySearchTree

def test_bst_operations():
    bst = BinarySearchTree()
    bst.insert(5)
    bst.insert(3)
    bst.insert(7)
    assert bst.search(3) is not None
    assert bst.delete(3)
    assert not bst.delete(10)