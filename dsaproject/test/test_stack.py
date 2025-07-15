import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.datastructures.stack import Stack, UndoStack, Operation
from src.models.student import Student


def test_stack_push_pop():
    """Test basic stack operations."""
    s = Stack()

    # Test push and pop
    assert s.push(1) == True
    assert not s.is_empty()
    assert s.size() == 1
    assert s.peek() == 1
    assert s.pop() == 1
    assert s.is_empty()

    # Test pop from empty stack
    assert s.pop() is None

    print("Basic stack test passed!")


def test_undo_stack():
    """Test UndoStack operations with Student objects."""
    undo_stack = UndoStack(max_size=3)

    # Create test students
    student1 = Student(id=1, name="Alice", age=20)
    student2 = Student(id=2, name="Bob", age=22)
    student3 = Student(id=3, name="Charlie", age=19)
    student4 = Student(id=4, name="Diana", age=21)

    # Test push operations
    assert undo_stack.push_operation('add', student1) == True
    assert undo_stack.push_operation('add', student2) == True
    assert undo_stack.push_operation('add', student3) == True
    assert undo_stack.size() == 3

    # Test max size enforcement
    assert undo_stack.push_operation('add', student4) == True
    assert undo_stack.size() == 3  # Should still be 3 due to max_size

    # Test get last operation
    last_op = undo_stack.get_last_operation()
    assert last_op is not None
    assert last_op.student.id == 4

    # Test undo operations
    op1 = undo_stack.undo_last_operation()
    assert op1.student.id == 4
    assert undo_stack.size() == 2

    op2 = undo_stack.undo_last_operation()
    assert op2.student.id == 3

    # Test operation history
    history = undo_stack.get_operation_history()
    assert len(history) == 1
    assert history[0].student.id == 2

    print("UndoStack test passed!")


def test_operation_types():
    """Test different operation types."""
    undo_stack = UndoStack()

    student = Student(id=1, name="Alice", age=20)
    old_student = Student(id=1, name="Alice", age=19)

    # Test different operation types
    undo_stack.push_operation('add', student)
    undo_stack.push_operation('update', student, old_student)
    undo_stack.push_operation('delete', student)

    # Check operations
    delete_op = undo_stack.undo_last_operation()
    assert delete_op.operation_type == 'delete'

    update_op = undo_stack.undo_last_operation()
    assert update_op.operation_type == 'update'
    assert update_op.old_data.age == 19

    add_op = undo_stack.undo_last_operation()
    assert add_op.operation_type == 'add'

    print("Operation types test passed!")


if __name__ == "__main__":
    test_stack_push_pop()
    test_undo_stack()
    test_operation_types()