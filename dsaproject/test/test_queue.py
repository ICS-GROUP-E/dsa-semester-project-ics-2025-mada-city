import pytest
from src.datastructures.queue import Queue

def test_queue_enqueue_dequeue():
    q = Queue()
    q.enqueue('a')
    assert not q.is_empty()
    assert q.dequeue() == 'a'
    with pytest.raises(IndexError):
        q.dequeue()