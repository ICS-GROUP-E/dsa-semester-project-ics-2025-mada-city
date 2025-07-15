from dataclasses import dataclass
from typing import Optional


@dataclass
class Student:
    id: int
    name: str
    age: int

    def __post_init__(self):
        if self.id is None:
            raise ValueError("Student ID cannot be None")
        if not self.name:
            raise ValueError("Student name cannot be empty")
        if self.age < 0:
            raise ValueError("Student age cannot be negative")

    def __lt__(self, other):
        """For BST comparison based on student ID"""
        if isinstance(other, Student):
            return self.id < other.id
        return self.id < other

    def __gt__(self, other):
        """For BST comparison based on student ID"""
        if isinstance(other, Student):
            return self.id > other.id
        return self.id > other

    def __eq__(self, other):
        """For equality comparison"""
        if isinstance(other, Student):
            return self.id == other.id
        return self.id == other

    def __str__(self):
        return f"Student(ID: {self.id}, Name: {self.name}, Age: {self.age})"

    def __repr__(self):
        return self.__str__()