from typing import Optional, List
from ..models.student import Student

class Node:
    def __init__(self, student: Student):
        self.student = student
        self.next: Optional['Node'] = None

class LinkedList:
    def __init__(self):
        self.head: Optional[Node] = None
        self.size_count = 0

    def insert_at_head(self, student: Student) -> bool:
        """Insert a student at the head of the linked list."""
        try:
            new_node = Node(student)
            new_node.next = self.head
            self.head = new_node
            self.size_count += 1
            print(f"Inserted {student} at head")
            return True
        except Exception as e:
            print(f"Error inserting student: {e}")
            return False

    def insert_at_tail(self, student: Student) -> bool:
        """Insert a student at the tail of the linked list."""
        try:
            new_node = Node(student)
            if not self.head:
                self.head = new_node
            else:
                current = self.head
                while current.next:
                    current = current.next
                current.next = new_node
            self.size_count += 1
            print(f"Inserted {student} at tail")
            return True
        except Exception as e:
            print(f"Error inserting student: {e}")
            return False

    def search_by_id(self, student_id: int) -> Optional[Student]:
        """Search for a student by ID."""
        current = self.head
        while current:
            if current.student.id == student_id:
                print(f"Found student with ID {student_id}")
                return current.student
            current = current.next
        print(f"Student with ID {student_id} not found")
        return None

    def search_by_name(self, name: str) -> List[Student]:
        """Search for students by name (returns all matches)."""
        matches = []
        current = self.head
        while current:
            if current.student.name.lower() == name.lower():
                matches.append(current.student)
            current = current.next
        if matches:
            print(f"Found {len(matches)} student(s) with name '{name}'")
        else:
            print(f"No students found with name '{name}'")
        return matches

    def delete_by_id(self, student_id: int) -> bool:
        """Delete a student by ID."""
        if not self.head:
            print(f"List is empty, cannot delete student with ID {student_id}")
            return False

        # If head node contains the student to delete
        if self.head.student.id == student_id:
            self.head = self.head.next
            self.size_count -= 1
            print(f"Deleted student with ID {student_id}")
            return True

        # Search for the student to delete
        current = self.head
        while current.next:
            if current.next.student.id == student_id:
                current.next = current.next.next
                self.size_count -= 1
                print(f"Deleted student with ID {student_id}")
                return True
            current = current.next

        print(f"Student with ID {student_id} not found for deletion")
        return False

    def get_all_students(self) -> List[Student]:
        """Get all students in insertion order."""
        students = []
        current = self.head
        while current:
            students.append(current.student)
            current = current.next
        return students

    def size(self) -> int:
        """Get the number of students in the linked list."""
        return self.size_count

    def is_empty(self) -> bool:
        """Check if the linked list is empty."""
        return self.head is None

    def clear(self):
        """Clear all students from the linked list."""
        self.head = None
        self.size_count = 0
        print("Cleared all students from linked list")

    def update_student(self, student_id: int, new_name: str = None, new_age: int = None) -> bool:
        """Update student information."""
        current = self.head
        while current:
            if current.student.id == student_id:
                if new_name is not None:
                    current.student.name = new_name
                if new_age is not None:
                    current.student.age = new_age
                print(f"Updated student with ID {student_id}")
                return True
            current = current.next
        print(f"Student with ID {student_id} not found for update")
        return False