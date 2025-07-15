import pytest
from src.datastructures.stack import Stack

def test_stack_push_pop():
    s = Stack()
    s.push(1)
    assert not s.is_empty()
    assert s.pop() == 1
    with pytest.raises(IndexError):
        s.pop()