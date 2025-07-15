from typing import Optional, Any
from ..models.student import Student


class ProcessingTask:
    """Represents a task to be processed"""

    def __init__(self, task_type: str, student: Student, priority: int = 0):
        self.task_type = task_type  # 'add', 'update', 'delete', 'search'
        self.student = student
        self.priority = priority


class Queue:
    def __init__(self):
        self._container = []

    def enqueue(self, item: Any) -> bool:
        """Add an item to the rear of the queue."""
        try:
            self._container.insert(0, item)
            if isinstance(item, ProcessingTask):
                print(f"Enqueued task: {item.task_type} for student ID {item.student.id}")
            else:
                print(f"Enqueued {item}")
            return True
        except Exception as e:
            print(f"Error enqueuing item: {e}")
            return False

    def dequeue(self) -> Optional[Any]:
        """Remove and return an item from the front of the queue."""
        if not self._container:
            print("Cannot dequeue from empty queue")
            return None

        item = self._container.pop()  # Regular queue uses FIFO
        if isinstance(item, ProcessingTask):
            print(f"Dequeued task: {item.task_type} for student ID {item.student.id}")
        else:
            print(f"Dequeued {item}")
        return item

    def front(self) -> Optional[Any]:
        """Peek at the front item without removing it."""
        if not self._container:
            return None
        return self._container[-1]  # Regular queue: front is at the end

    def is_empty(self) -> bool:
        """Check if the queue is empty."""
        return len(self._container) == 0

    def size(self) -> int:
        """Get the number of items in the queue."""
        return len(self._container)

    def clear(self):
        """Clear all items from the queue."""
        self._container.clear()
        print("Cleared all items from queue")


class PriorityQueue(Queue):
    """A priority queue implementation for processing tasks"""

    def dequeue(self) -> Optional[Any]:
        """Remove and return the highest priority item."""
        if not self._container:
            print("Cannot dequeue from empty queue")
            return None

        # For priority queue, highest priority is at index 0
        item = self._container.pop(0)
        if isinstance(item, ProcessingTask):
            print(f"Dequeued task: {item.task_type} for student ID {item.student.id}")
        else:
            print(f"Dequeued {item}")
        return item

    def front(self) -> Optional[Any]:
        """Peek at the highest priority item without removing it."""
        if not self._container:
            return None
        return self._container[0]

    def enqueue_task(self, task_type: str, student: Student, priority: int = 0) -> bool:
        """Add a processing task with priority."""
        task = ProcessingTask(task_type, student, priority)
        return self.enqueue(task)

    def enqueue(self, item: Any) -> bool:
        """Add an item maintaining priority order (higher priority first)."""
        try:
            if isinstance(item, ProcessingTask):
                # Find the correct position based on priority (higher priority comes first)
                inserted = False
                for i, existing_item in enumerate(self._container):
                    if (isinstance(existing_item, ProcessingTask) and
                            item.priority > existing_item.priority):
                        self._container.insert(i, item)
                        inserted = True
                        break

                if not inserted:
                    self._container.append(item)

                print(
                    f"Enqueued priority task: {item.task_type} for student ID {item.student.id} (priority: {item.priority})")
            else:
                self._container.insert(0, item)
                print(f"Enqueued {item}")
            return True
        except Exception as e:
            print(f"Error enqueuing item: {e}")
            return False

    def get_next_task(self) -> Optional[ProcessingTask]:
        """Get the next task to process without removing it."""
        if self.is_empty():
            return None

        front_item = self.front()
        if isinstance(front_item, ProcessingTask):
            return front_item
        return None

    def process_next_task(self) -> Optional[ProcessingTask]:
        """Remove and return the next task to process."""
        if self.is_empty():
            return None

        task = self.dequeue()
        if isinstance(task, ProcessingTask):
            return task
        return None

    def get_all_tasks(self) -> list:
        """Get all tasks in the queue."""
        return [item for item in self._container if isinstance(item, ProcessingTask)]