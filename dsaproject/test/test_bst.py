import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.datastructures.bst import BinarySearchTree
from src.models.student import Student


def test_bst_operations():
    """Test BST operations with Student objects."""
    bst = BinarySearchTree()

    # Create test students
    student1 = Student(id=5, name="Alice", age=20)
    student2 = Student(id=3, name="Bob", age=22)
    student3 = Student(id=7, name="Charlie", age=19)

    # Test insertion
    assert bst.insert(student1) == True
    assert bst.insert(student2) == True
    assert bst.insert(student3) == True

    # Test search
    found_student = bst.search(3)
    assert found_student is not None
    assert found_student.name == "Bob"
    assert found_student.age == 22

    # Test search for non-existent student
    assert bst.search(10) is None

    # Test deletion
    assert bst.delete(3) == True
    assert bst.search(3) is None
    assert bst.delete(10) == False

    # Test get all students
    all_students = bst.get_all_students()
    assert len(all_students) == 2
    assert all_students[0].id == 5  # Should be sorted by ID
    assert all_students[1].id == 7

    # Test size
    assert bst.size() == 2

    # Test min and max
    min_student = bst.get_min_student()
    max_student = bst.get_max_student()
    assert min_student.id == 5
    assert max_student.id == 7

    print("All BST tests passed!")


def test_bst_update():
    """Test BST update functionality."""
    bst = BinarySearchTree()

    # Insert a student
    student = Student(id=1, name="Alice", age=20)
    bst.insert(student)

    # Update the student
    updated_student = Student(id=1, name="Alice Smith", age=21)
    bst.insert(updated_student)  # Insert with same ID updates

    # Verify update
    found = bst.search(1)
    assert found.name == "Alice Smith"
    assert found.age == 21

    print("BST update test passed!")


if __name__ == "__main__":
    test_bst_operations()
    test_bst_update()