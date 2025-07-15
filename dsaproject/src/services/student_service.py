from typing import List, Optional, Dict, Any
from ..models.student import Student
from ..datastructures.bst import BinarySearchTree
from ..datastructures.linkedlist import LinkedList
from ..datastructures.stack import UndoStack, Operation
from ..datastructures.queue import PriorityQueue, ProcessingTask


class StudentService:
    """Service class that manages student data using various data structures"""

    def __init__(self):
        # Primary storage using BST for efficient search by ID
        self.bst = BinarySearchTree()

        # LinkedList for maintaining insertion order and alternative searching
        self.linked_list = LinkedList()

        # Stack for undo operations
        self.undo_stack = UndoStack(max_size=100)

        # Queue for processing tasks
        self.processing_queue = PriorityQueue()

        # ID counter for auto-generating student IDs
        self.next_id = 1

    def add_student(self, name: str, age: int, student_id: int = None) -> bool:
        """Add a new student to the system."""
        try:
            # Generate ID if not provided
            if student_id is None:
                student_id = self.next_id
                self.next_id += 1
            else:
                # Check if ID already exists
                existing = self.bst.search(student_id)
                if existing:
                    print(f"Student with ID {student_id} already exists")
                    return False

                # Update next_id if provided ID is higher
                if student_id >= self.next_id:
                    self.next_id = student_id + 1

            # Create student object
            student = Student(id=student_id, name=name, age=age)

            # Add to BST (primary storage)
            if not self.bst.insert(student):
                return False

            # Add to LinkedList (for insertion order)
            if not self.linked_list.insert_at_tail(student):
                # Rollback BST insertion if LinkedList fails
                self.bst.delete(student_id)
                return False

            # Record operation for undo
            self.undo_stack.push_operation('add', student)

            # Add to processing queue (low priority for new additions)
            self.processing_queue.enqueue_task('add', student, priority=1)

            print(f"Successfully added student: {student}")
            return True

        except Exception as e:
            print(f"Error adding student: {e}")
            return False

    def get_student(self, student_id: int) -> Optional[Student]:
        """Get a student by ID."""
        try:
            # Use BST for efficient search
            return self.bst.search(student_id)
        except Exception as e:
            print(f"Error getting student: {e}")
            return None

    def update_student(self, student_id: int, name: str = None, age: int = None) -> bool:
        """Update an existing student."""
        try:
            # Find existing student
            existing_student = self.bst.search(student_id)
            if not existing_student:
                print(f"Student with ID {student_id} not found")
                return False

            # Store old data for undo
            old_student = Student(
                id=existing_student.id,
                name=existing_student.name,
                age=existing_student.age
            )

            # Update student data
            updated_student = Student(
                id=student_id,
                name=name if name is not None else existing_student.name,
                age=age if age is not None else existing_student.age
            )

            # Update in BST
            if not self.bst.insert(updated_student):  # BST insert updates if ID exists
                return False

            # Update in LinkedList
            if not self.linked_list.update_student(student_id, updated_student.name, updated_student.age):
                # Rollback BST update
                self.bst.insert(old_student)
                return False

            # Record operation for undo
            self.undo_stack.push_operation('update', updated_student, old_student)

            # Add to processing queue (medium priority for updates)
            self.processing_queue.enqueue_task('update', updated_student, priority=2)

            print(f"Successfully updated student: {updated_student}")
            return True

        except Exception as e:
            print(f"Error updating student: {e}")
            return False

    def delete_student(self, student_id: int) -> bool:
        """Delete a student by ID."""
        try:
            # Find existing student
            existing_student = self.bst.search(student_id)
            if not existing_student:
                print(f"Student with ID {student_id} not found")
                return False

            # Delete from BST
            if not self.bst.delete(student_id):
                return False

            # Delete from LinkedList
            if not self.linked_list.delete_by_id(student_id):
                # Rollback BST deletion
                self.bst.insert(existing_student)
                return False

            # Record operation for undo
            self.undo_stack.push_operation('delete', existing_student)

            # Add to processing queue (high priority for deletions)
            self.processing_queue.enqueue_task('delete', existing_student, priority=3)

            print(f"Successfully deleted student: {existing_student}")
            return True

        except Exception as e:
            print(f"Error deleting student: {e}")
            return False

    def get_all_students(self, sorted_by_id: bool = True) -> List[Student]:
        """Get all students. If sorted_by_id is True, returns sorted by ID, otherwise by insertion order."""
        if sorted_by_id:
            return self.bst.get_all_students()
        else:
            return self.linked_list.get_all_students()

    def search_students_by_name(self, name: str) -> List[Student]:
        """Search students by name using LinkedList."""
        return self.linked_list.search_by_name(name)

    def get_student_count(self) -> int:
        """Get total number of students."""
        return self.bst.size()

    def get_min_max_students(self) -> tuple[Optional[Student], Optional[Student]]:
        """Get students with minimum and maximum IDs."""
        return self.bst.get_min_student(), self.bst.get_max_student()

    def undo_last_operation(self) -> bool:
        """Undo the last operation."""
        try:
            operation = self.undo_stack.undo_last_operation()
            if not operation:
                return False

            if operation.operation_type == 'add':
                # Undo add by deleting
                self.bst.delete(operation.student.id)
                self.linked_list.delete_by_id(operation.student.id)
                print(f"Undid add operation for student ID {operation.student.id}")

            elif operation.operation_type == 'delete':
                # Undo delete by adding back
                self.bst.insert(operation.student)
                self.linked_list.insert_at_tail(operation.student)
                print(f"Undid delete operation for student ID {operation.student.id}")

            elif operation.operation_type == 'update':
                # Undo update by restoring old data
                if operation.old_data:
                    self.bst.insert(operation.old_data)
                    self.linked_list.update_student(
                        operation.old_data.id,
                        operation.old_data.name,
                        operation.old_data.age
                    )
                    print(f"Undid update operation for student ID {operation.student.id}")

            return True

        except Exception as e:
            print(f"Error undoing operation: {e}")
            return False

    def get_operation_history(self) -> List[str]:
        """Get a history of operations."""
        operations = self.undo_stack.get_operation_history()
        return [f"{op.operation_type.capitalize()} student ID {op.student.id} ({op.student.name})"
                for op in operations]

    def process_next_task(self) -> Optional[Dict[str, Any]]:
        """Process the next task in the queue."""
        task = self.processing_queue.process_next_task()
        if task:
            return {
                'task_type': task.task_type,
                'student': task.student,
                'priority': task.priority
            }
        return None

    def get_pending_tasks(self) -> List[Dict[str, Any]]:
        """Get all pending tasks."""
        tasks = self.processing_queue.get_all_tasks()
        return [{'task_type': task.task_type, 'student': task.student, 'priority': task.priority}
                for task in tasks]

    def clear_all_data(self):
        """Clear all data from all data structures."""
        self.bst = BinarySearchTree()
        self.linked_list = LinkedList()
        self.undo_stack.clear()
        self.processing_queue.clear()
        self.next_id = 1
        print("Cleared all student data")

    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the data structures."""
        return {
            'total_students': self.bst.size(),
            'pending_tasks': self.processing_queue.size(),
            'undo_operations_available': self.undo_stack.size(),
            'min_student': self.bst.get_min_student(),
            'max_student': self.bst.get_max_student(),
            'next_available_id': self.next_id
        }
