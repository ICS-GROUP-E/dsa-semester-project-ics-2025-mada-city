#!/usr/bin/env python3
"""
DSA Project - Student Management System
Uses data structures (BST, LinkedList, Stack, Queue) for CRUD operations
"""

import sys
import os

# Add the project root to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dsaproject.src.ui.app import main

if __name__ == "__main__":
    print("Starting DSA Project - Student Management System")
    print("This system uses the following data structures:")
    print("- Binary Search Tree (BST) for efficient student lookup by ID")
    print("- Linked List for maintaining insertion order")
    print("- Stack for undo operations")
    print("- Queue for task processing")
    print("-" * 50)
    main()
