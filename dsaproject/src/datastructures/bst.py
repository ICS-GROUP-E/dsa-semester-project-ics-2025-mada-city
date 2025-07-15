from typing import Optional, List
from ..models.student import Student


class BSTNode:
    def __init__(self, student: Student):
        self.student = student
        self.left: Optional['BSTNode'] = None
        self.right: Optional['BSTNode'] = None


class BinarySearchTree:
    def __init__(self):
        self.root: Optional[BSTNode] = None

    def insert(self, student: Student) -> bool:
        """Insert a student into the BST. Returns True if successful."""
        try:
            self.root = self._insert(self.root, student)
            print(f"Inserted {student}")
            return True
        except Exception as e:
            print(f"Error inserting student: {e}")
            return False

    def _insert(self, node: Optional[BSTNode], student: Student) -> BSTNode:
        if node is None:
            return BSTNode(student)

        if student.id == node.student.id:
            # Update existing student
            node.student = student
            return node

        if student.id < node.student.id:
            node.left = self._insert(node.left, student)
        else:
            node.right = self._insert(node.right, student)
        return node

    def search(self, student_id: int) -> Optional[Student]:
        """Search for a student by ID."""
        result = self._search(self.root, student_id)
        if result:
            print(f"Found student with ID {student_id}")
            return result.student
        else:
            print(f"Student with ID {student_id} not found")
            return None

    def _search(self, node: Optional[BSTNode], student_id: int) -> Optional[BSTNode]:
        if node is None or node.student.id == student_id:
            return node
        if student_id < node.student.id:
            return self._search(node.left, student_id)
        return self._search(node.right, student_id)

    def delete(self, student_id: int) -> bool:
        """Delete a student by ID. Returns True if successful."""
        old_size = self.size()
        self.root, deleted = self._delete(self.root, student_id)
        if deleted:
            print(f"Deleted student with ID {student_id}")
        else:
            print(f"Student with ID {student_id} not found for deletion")
        return deleted

    def _delete(self, node: Optional[BSTNode], student_id: int) -> tuple[Optional[BSTNode], bool]:
        if node is None:
            return node, False

        if student_id < node.student.id:
            node.left, deleted = self._delete(node.left, student_id)
            return node, deleted
        elif student_id > node.student.id:
            node.right, deleted = self._delete(node.right, student_id)
            return node, deleted
        else:
            # Found the node to delete
            if node.left is None:
                return node.right, True
            elif node.right is None:
                return node.left, True
            else:
                # Node has two children: get inorder successor
                succ = node.right
                while succ.left:
                    succ = succ.left
                node.student = succ.student
                node.right, _ = self._delete(node.right, succ.student.id)
                return node, True

    def get_all_students(self) -> List[Student]:
        """Get all students in sorted order (by ID)."""
        students = []
        self._inorder_traversal(self.root, students)
        return students

    def _inorder_traversal(self, node: Optional[BSTNode], students: List[Student]) -> None:
        if node is not None:
            self._inorder_traversal(node.left, students)
            students.append(node.student)
            self._inorder_traversal(node.right, students)

    def size(self) -> int:
        """Get the number of students in the BST."""
        return self._size(self.root)

    def _size(self, node: Optional[BSTNode]) -> int:
        if node is None:
            return 0
        return 1 + self._size(node.left) + self._size(node.right)

    def get_min_student(self) -> Optional[Student]:
        """Get student with minimum ID."""
        if self.root is None:
            return None
        node = self.root
        while node.left:
            node = node.left
        return node.student

    def get_max_student(self) -> Optional[Student]:
        """Get student with maximum ID."""
        if self.root is None:
            return None
        node = self.root
        while node.right:
            node = node.right
        return node.student