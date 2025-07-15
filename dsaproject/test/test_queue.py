import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.datastructures.queue import Queue, PriorityQueue, ProcessingTask
from src.models.student import Student


def test_queue_enqueue_dequeue():
    """Test basic queue operations."""
    q = Queue()

    # Test enqueue and dequeue
    assert q.enqueue('a') == True
    assert not q.is_empty()
    assert q.size() == 1
    assert q.front() == 'a'
    assert q.dequeue() == 'a'
    assert q.is_empty()

    # Test dequeue from empty queue
    assert q.dequeue() is None

    # Test FIFO behavior
    q.enqueue('first')
    q.enqueue('second')
    q.enqueue('third')
    assert q.dequeue() == 'first'
    assert q.dequeue() == 'second'
    assert q.dequeue() == 'third'

    print("Basic queue test passed!")


def test_priority_queue():
    """Test PriorityQueue operations with Student objects."""
    pq = PriorityQueue()

    # Create test students
    student1 = Student(id=1, name="Alice", age=20)
    student2 = Student(id=2, name="Bob", age=22)
    student3 = Student(id=3, name="Charlie", age=19)

    # Test enqueue tasks with different priorities
    assert pq.enqueue_task('add', student1, priority=1) == True
    assert pq.enqueue_task('update', student2, priority=3) == True
    assert pq.enqueue_task('delete', student3, priority=2) == True

    assert pq.size() == 3

    # Test get next task (should be highest priority)
    next_task = pq.get_next_task()
    assert next_task is not None
    assert next_task.priority == 3
    assert next_task.student.id == 2

    # Test process tasks in priority order
    task1 = pq.process_next_task()
    assert task1.priority == 3
    assert task1.task_type == 'update'

    task2 = pq.process_next_task()
    assert task2.priority == 2
    assert task2.task_type == 'delete'

    task3 = pq.process_next_task()
    assert task3.priority == 1
    assert task3.task_type == 'add'

    assert pq.is_empty()

    print("PriorityQueue test passed!")


def test_processing_task():
    """Test ProcessingTask creation and properties."""
    student = Student(id=1, name="Alice", age=20)
    task = ProcessingTask('add', student, priority=2)

    assert task.task_type == 'add'
    assert task.student.id == 1
    assert task.priority == 2

    print("ProcessingTask test passed!")


def test_queue_with_students():
    """Test queue operations with Student objects."""
    q = Queue()

    # Create test students
    student1 = Student(id=1, name="Alice", age=20)
    student2 = Student(id=2, name="Bob", age=22)

    # Test enqueue and dequeue with students
    assert q.enqueue(student1) == True
    assert q.enqueue(student2) == True

    dequeued1 = q.dequeue()
    assert dequeued1.id == 1
    assert dequeued1.name == "Alice"

    dequeued2 = q.dequeue()
    assert dequeued2.id == 2
    assert dequeued2.name == "Bob"

    print("Queue with students test passed!")


if __name__ == "__main__":
    test_queue_enqueue_dequeue()
    test_priority_queue()
    test_processing_task()
    test_queue_with_students()