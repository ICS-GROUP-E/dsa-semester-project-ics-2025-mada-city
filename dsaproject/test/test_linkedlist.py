import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.datastructures.linkedlist import LinkedList
from src.models.student import Student


def test_linkedlist_operations():
    """Test LinkedList operations with Student objects."""
    ll = LinkedList()

    # Create test students
    student1 = Student(id=10, name="Alice", age=20)
    student2 = Student(id=20, name="Bob", age=22)
    student3 = Student(id=30, name="Charlie", age=19)

    # Test insertion at head
    assert ll.insert_at_head(student1) == True
    assert ll.insert_at_head(student2) == True
    assert ll.size() == 2

    # Test insertion at tail
    assert ll.insert_at_tail(student3) == True
    assert ll.size() == 3

    # Test search by ID
    found_student = ll.search_by_id(10)
    assert found_student is not None
    assert found_student.name == "Alice"

    # Test search by name
    found_students = ll.search_by_name("Bob")
    assert len(found_students) == 1
    assert found_students[0].id == 20

    # Test deletion
    assert ll.delete_by_id(20) == True
    assert ll.size() == 2
    assert ll.search_by_id(20) is None
    assert ll.delete_by_id(40) == False

    # Test get all students
    all_students = ll.get_all_students()
    assert len(all_students) == 2

    # Test update
    assert ll.update_student(10, "Alice Smith", 21) == True
    updated = ll.search_by_id(10)
    assert updated.name == "Alice Smith"
    assert updated.age == 21

    # Test clear
    ll.clear()
    assert ll.is_empty() == True
    assert ll.size() == 0

    print("All LinkedList tests passed!")


def test_linkedlist_order():
    """Test LinkedList maintains insertion order."""
    ll = LinkedList()

    students = [
        Student(id=3, name="Charlie", age=19),
        Student(id=1, name="Alice", age=20),
        Student(id=2, name="Bob", age=22)
    ]

    # Insert in order
    for student in students:
        ll.insert_at_tail(student)

    # Check order is preserved
    all_students = ll.get_all_students()
    assert len(all_students) == 3
    assert all_students[0].id == 3
    assert all_students[1].id == 1
    assert all_students[2].id == 2

    print("LinkedList order test passed!")


if __name__ == "__main__":
    test_linkedlist_operations()
    test_linkedlist_order()