#!/usr/bin/env python3
"""
Demo script to showcase the DSA Student Management System
"""
import sys
import os

# Add the project root to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dsaproject.src.services.student_service import StudentService


def demo_data_structures():
    """Demonstrate the data structures in action."""
    print("🎓 DSA Student Management System Demo")
    print("=" * 50)

    # Create service instance
    service = StudentService()

    # Add students
    print("\n📝 Adding Students:")
    service.add_student("Alice Johnson", 20)
    service.add_student("Bob Smith", 22)
    service.add_student("Charlie Brown", 19)
    service.add_student("Diana Prince", 21)

    # Display statistics
    print("\n📊 Current Statistics:")
    stats = service.get_statistics()
    print(f"   Total Students: {stats['total_students']}")
    print(f"   Pending Tasks: {stats['pending_tasks']}")
    print(f"   Undo Operations Available: {stats['undo_operations_available']}")
    print(f"   Min Student: {stats['min_student']}")
    print(f"   Max Student: {stats['max_student']}")

    # Show students in different orders
    print("\n🌳 Students (BST - Sorted by ID):")
    bst_students = service.get_all_students(sorted_by_id=True)
    for student in bst_students:
        print(f"   {student}")

    print("\n🔗 Students (LinkedList - Insertion Order):")
    linked_students = service.get_all_students(sorted_by_id=False)
    for student in linked_students:
        print(f"   {student}")

    # Search functionality
    print("\n🔍 Search by Name:")
    alice_students = service.search_students_by_name("Alice Johnson")
    for student in alice_students:
        print(f"   Found: {student}")

    # Update operation
    print("\n✏️ Updating Student:")
    service.update_student(1, "Alice Smith", 21)
    updated = service.get_student(1)
    print(f"   Updated: {updated}")

    # Delete operation
    print("\n🗑️ Deleting Student:")
    service.delete_student(2)
    print(f"   Remaining students: {service.get_student_count()}")

    # Undo operation
    print("\n↩️ Undo Last Operation:")
    service.undo_last_operation()
    print(f"   Students after undo: {service.get_student_count()}")
    restored = service.get_student(2)
    print(f"   Restored: {restored}")

    # Show operation history
    print("\n📋 Operation History:")
    history = service.get_operation_history()
    for i, op in enumerate(history[-5:], 1):  # Show last 5 operations
        print(f"   {i}. {op}")

    # Show pending tasks
    print("\n📋 Pending Tasks:")
    tasks = service.get_pending_tasks()
    for task in tasks[-3:]:  # Show last 3 tasks
        print(f"   {task['task_type'].capitalize()} - {task['student'].name} (Priority: {task['priority']})")

    # Process a task
    print("\n⚙️ Processing Next Task:")
    next_task = service.process_next_task()
    if next_task:
        print(f"   Processed: {next_task['task_type']} for {next_task['student'].name}")

    print("\n" + "=" * 50)
    print("✅ Demo completed successfully!")
    print("🚀 Run 'python main.py' to start the GUI application!")


if __name__ == "__main__":
    demo_data_structures()
