from src.datastructures.linkedlist import LinkedList

def test_linkedlist_operations():
    ll = LinkedList()
    ll.insert(10)
    ll.insert(20)
    assert ll.search(10) is not None
    assert ll.delete(20)
    assert not ll.delete(30)