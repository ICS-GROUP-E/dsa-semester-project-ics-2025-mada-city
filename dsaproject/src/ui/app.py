import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import List
from ..services.student_service import StudentService
from ..models.student import Student


class StudentManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager - DSA Project")
        self.root.geometry("1000x700")

        # Initialize the student service (uses data structures)
        self.student_service = StudentService()

        # Initialize UI components
        self.setup_ui()
        self.refresh_display()

        # Add some sample data
        self.add_sample_data()

    def setup_ui(self):
        """Setup the user interface."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)

        # Title
        title_label = ttk.Label(main_frame, text="Student Management System",
                                font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))

        # Input frame
        input_frame = ttk.LabelFrame(main_frame, text="Student Information", padding="10")
        input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))

        # Student ID
        ttk.Label(input_frame, text="Student ID:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.id_var = tk.StringVar()
        id_entry = ttk.Entry(input_frame, textvariable=self.id_var, width=10)
        id_entry.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        ttk.Label(input_frame, text="(Leave empty for auto-generate)").grid(row=0, column=2, sticky=tk.W)

        # Name
        ttk.Label(input_frame, text="Name:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5))
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(input_frame, textvariable=self.name_var, width=30)
        name_entry.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))

        # Age
        ttk.Label(input_frame, text="Age:").grid(row=2, column=0, sticky=tk.W, padx=(0, 5))
        self.age_var = tk.StringVar()
        age_entry = ttk.Entry(input_frame, textvariable=self.age_var, width=10)
        age_entry.grid(row=2, column=1, sticky=tk.W, pady=(5, 0))

        # Buttons frame
        buttons_frame = ttk.Frame(input_frame)
        buttons_frame.grid(row=3, column=0, columnspan=3, pady=(10, 0))

        # CRUD buttons
        ttk.Button(buttons_frame, text="Add Student", command=self.add_student).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(buttons_frame, text="Update Student", command=self.update_student).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(buttons_frame, text="Delete Student", command=self.delete_student).grid(row=0, column=2, padx=(0, 5))
        ttk.Button(buttons_frame, text="Clear Form", command=self.clear_form).grid(row=0, column=3, padx=(0, 5))

        # Advanced operations frame
        advanced_frame = ttk.Frame(input_frame)
        advanced_frame.grid(row=4, column=0, columnspan=3, pady=(10, 0))

        ttk.Button(advanced_frame, text="Search by Name", command=self.search_by_name).grid(row=0, column=0,
                                                                                            padx=(0, 5))
        ttk.Button(advanced_frame, text="Undo Last Operation", command=self.undo_operation).grid(row=0, column=1,
                                                                                                 padx=(0, 5))
        ttk.Button(advanced_frame, text="Show Statistics", command=self.show_statistics).grid(row=0, column=2,
                                                                                              padx=(0, 5))
        ttk.Button(advanced_frame, text="Clear All Data", command=self.clear_all_data).grid(row=0, column=3,
                                                                                            padx=(0, 5))

        # Display frame
        display_frame = ttk.LabelFrame(main_frame, text="Students", padding="10")
        display_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        display_frame.columnconfigure(0, weight=1)
        display_frame.rowconfigure(0, weight=1)

        # Treeview for displaying students
        columns = ('ID', 'Name', 'Age')
        self.tree = ttk.Treeview(display_frame, columns=columns, show='headings', height=15)

        # Define column headings and widths
        self.tree.heading('ID', text='Student ID')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Age', text='Age')

        self.tree.column('ID', width=100, anchor=tk.CENTER)
        self.tree.column('Name', width=200, anchor=tk.W)
        self.tree.column('Age', width=100, anchor=tk.CENTER)

        # Scrollbar
        scrollbar = ttk.Scrollbar(display_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Grid the treeview and scrollbar
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Bind treeview selection
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

        # Sort options frame
        sort_frame = ttk.Frame(display_frame)
        sort_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0))

        ttk.Label(sort_frame, text="View:").grid(row=0, column=0, padx=(0, 5))
        ttk.Button(sort_frame, text="Sorted by ID (BST)", command=self.show_sorted_by_id).grid(row=0, column=1,
                                                                                               padx=(0, 5))
        ttk.Button(sort_frame, text="Insertion Order (LinkedList)", command=self.show_insertion_order).grid(row=0,
                                                                                                            column=2,
                                                                                                            padx=(0, 5))

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - Using Data Structures: BST, LinkedList, Stack, Queue")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))

    def add_sample_data(self):
        """Add some sample data to demonstrate the system."""
        sample_students = [
            ("Alice Johnson", 20),
            ("Bob Smith", 22),
            ("Charlie Brown", 19),
            ("Diana Prince", 21),
            ("Eve Adams", 23)
        ]

        for name, age in sample_students:
            self.student_service.add_student(name, age)

        self.refresh_display()
        self.status_var.set("Added sample data - Ready")

    def refresh_display(self, sorted_by_id=True):
        """Refresh the display of students."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Get students
        students = self.student_service.get_all_students(sorted_by_id=sorted_by_id)

        # Add students to treeview
        for student in students:
            self.tree.insert('', tk.END, values=(student.id, student.name, student.age))

        # Update status
        count = self.student_service.get_student_count()
        sort_type = "BST (ID sorted)" if sorted_by_id else "LinkedList (insertion order)"
        self.status_var.set(f"Displaying {count} students - {sort_type}")

    def add_student(self):
        """Add a new student."""
        try:
            name = self.name_var.get().strip()
            age_str = self.age_var.get().strip()
            id_str = self.id_var.get().strip()

            if not name:
                messagebox.showerror("Error", "Name is required!")
                return

            if not age_str:
                messagebox.showerror("Error", "Age is required!")
                return

            try:
                age = int(age_str)
                if age < 0:
                    messagebox.showerror("Error", "Age must be non-negative!")
                    return
            except ValueError:
                messagebox.showerror("Error", "Age must be a valid number!")
                return

            student_id = None
            if id_str:
                try:
                    student_id = int(id_str)
                    if student_id <= 0:
                        messagebox.showerror("Error", "Student ID must be positive!")
                        return
                except ValueError:
                    messagebox.showerror("Error", "Student ID must be a valid number!")
                    return

            # Add student
            success = self.student_service.add_student(name, age, student_id)

            if success:
                messagebox.showinfo("Success", "Student added successfully!")
                self.clear_form()
                self.refresh_display()
            else:
                messagebox.showerror("Error", "Failed to add student!")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def update_student(self):
        """Update an existing student."""
        try:
            id_str = self.id_var.get().strip()
            if not id_str:
                messagebox.showerror("Error", "Student ID is required for update!")
                return

            try:
                student_id = int(id_str)
            except ValueError:
                messagebox.showerror("Error", "Student ID must be a valid number!")
                return

            name = self.name_var.get().strip()
            age_str = self.age_var.get().strip()

            if not name and not age_str:
                messagebox.showerror("Error", "At least one field (name or age) must be provided!")
                return

            age = None
            if age_str:
                try:
                    age = int(age_str)
                    if age < 0:
                        messagebox.showerror("Error", "Age must be non-negative!")
                        return
                except ValueError:
                    messagebox.showerror("Error", "Age must be a valid number!")
                    return

            # Update student
            success = self.student_service.update_student(student_id, name if name else None, age)

            if success:
                messagebox.showinfo("Success", "Student updated successfully!")
                self.clear_form()
                self.refresh_display()
            else:
                messagebox.showerror("Error", "Failed to update student! Student may not exist.")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def delete_student(self):
        """Delete a student."""
        try:
            id_str = self.id_var.get().strip()
            if not id_str:
                messagebox.showerror("Error", "Student ID is required for deletion!")
                return

            try:
                student_id = int(id_str)
            except ValueError:
                messagebox.showerror("Error", "Student ID must be a valid number!")
                return

            # Confirm deletion
            if messagebox.askyesno("Confirm Deletion",
                                   f"Are you sure you want to delete student with ID {student_id}?"):
                success = self.student_service.delete_student(student_id)

                if success:
                    messagebox.showinfo("Success", "Student deleted successfully!")
                    self.clear_form()
                    self.refresh_display()
                else:
                    messagebox.showerror("Error", "Failed to delete student! Student may not exist.")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def search_by_name(self):
        """Search students by name."""
        try:
            name = simpledialog.askstring("Search by Name", "Enter name to search:")
            if name:
                students = self.student_service.search_students_by_name(name)

                if students:
                    # Clear and show search results
                    for item in self.tree.get_children():
                        self.tree.delete(item)

                    for student in students:
                        self.tree.insert('', tk.END, values=(student.id, student.name, student.age))

                    self.status_var.set(f"Found {len(students)} student(s) with name '{name}'")
                    messagebox.showinfo("Search Results", f"Found {len(students)} student(s) with name '{name}'")
                else:
                    messagebox.showinfo("Search Results", f"No students found with name '{name}'")
                    self.refresh_display()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during search: {str(e)}")

    def undo_operation(self):
        """Undo the last operation."""
        try:
            success = self.student_service.undo_last_operation()
            if success:
                messagebox.showinfo("Undo", "Last operation undone successfully!")
                self.refresh_display()
            else:
                messagebox.showinfo("Undo", "No operations to undo!")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during undo: {str(e)}")

    def show_statistics(self):
        """Show statistics about the data structures."""
        try:
            stats = self.student_service.get_statistics()

            stats_text = f"""Data Structure Statistics:

Total Students: {stats['total_students']}
Pending Tasks: {stats['pending_tasks']}
Undo Operations Available: {stats['undo_operations_available']}
Next Available ID: {stats['next_available_id']}

Student with Min ID: {stats['min_student'] if stats['min_student'] else 'None'}
Student with Max ID: {stats['max_student'] if stats['max_student'] else 'None'}

Operation History:
{chr(10).join(self.student_service.get_operation_history()[-10:])}"""  # Last 10 operations

            messagebox.showinfo("Statistics", stats_text)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def clear_all_data(self):
        """Clear all data from the system."""
        if messagebox.askyesno("Confirm Clear", "Are you sure you want to clear all data? This cannot be undone!"):
            self.student_service.clear_all_data()
            self.refresh_display()
            messagebox.showinfo("Clear Data", "All data cleared successfully!")

    def show_sorted_by_id(self):
        """Show students sorted by ID (using BST)."""
        self.refresh_display(sorted_by_id=True)

    def show_insertion_order(self):
        """Show students in insertion order (using LinkedList)."""
        self.refresh_display(sorted_by_id=False)

    def clear_form(self):
        """Clear all form fields."""
        self.id_var.set("")
        self.name_var.set("")
        self.age_var.set("")

    def on_select(self, event):
        """Handle treeview selection."""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            if values:
                self.id_var.set(str(values[0]))
                self.name_var.set(str(values[1]))
                self.age_var.set(str(values[2]))


def main():
    root = tk.Tk()
    app = StudentManagerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()