from typing import Optional, Any
from ..models.student import Student


class Operation:
    """Represents an operation that can be undone"""

    def __init__(self, operation_type: str, student: Student, old_data: Any = None):
        self.operation_type = operation_type  # 'add', 'update', 'delete'
        self.student = student
        self.old_data = old_data  # For update operations, stores the old student data


class Stack:
    def __init__(self):
        self._container = []

    def push(self, item: Any) -> bool:
        """Push an item onto the stack."""
        try:
            self._container.append(item)
            if isinstance(item, Operation):
                print(f"Pushed operation: {item.operation_type} for student ID {item.student.id}")
            else:
                print(f"Pushed {item}")
            return True
        except Exception as e:
            print(f"Error pushing item: {e}")
            return False

    def pop(self) -> Optional[Any]:
        """Pop an item from the stack."""
        if not self._container:
            print("Cannot pop from empty stack")
            return None

        item = self._container.pop()
        if isinstance(item, Operation):
            print(f"Popped operation: {item.operation_type} for student ID {item.student.id}")
        else:
            print(f"Popped {item}")
        return item

    def peek(self) -> Optional[Any]:
        """Peek at the top item without removing it."""
        if not self._container:
            return None
        return self._container[-1]

    def is_empty(self) -> bool:
        """Check if the stack is empty."""
        return len(self._container) == 0

    def size(self) -> int:
        """Get the number of items in the stack."""
        return len(self._container)

    def clear(self):
        """Clear all items from the stack."""
        self._container.clear()
        print("Cleared all items from stack")


class UndoStack(Stack):
    """Specialized stack for managing undo operations"""

    def __init__(self, max_size: int = 50):
        super().__init__()
        self.max_size = max_size

    def push_operation(self, operation_type: str, student: Student, old_data: Any = None) -> bool:
        """Push an operation that can be undone."""
        operation = Operation(operation_type, student, old_data)

        # Remove oldest operation if we exceed max size
        if len(self._container) >= self.max_size:
            self._container.pop(0)
            print(f"Removed oldest operation to maintain max size of {self.max_size}")

        return self.push(operation)

    def get_last_operation(self) -> Optional[Operation]:
        """Get the last operation without removing it."""
        if self.is_empty():
            return None
        return self.peek()

    def undo_last_operation(self) -> Optional[Operation]:
        """Remove and return the last operation for undo."""
        if self.is_empty():
            print("No operations to undo")
            return None
        return self.pop()

    def get_operation_history(self) -> list:
        """Get a copy of all operations in the stack."""
        return self._container.copy()