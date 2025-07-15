import tkinter as tk
from src.db.database import init_db, get_connection

init_db()

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager")
        self.setup_ui()
        self.load_students()

    def setup_ui(self):
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10)
        tk.Label(frame, text="Name").grid(row=0, column=0)
        tk.Label(frame, text="Age").grid(row=1, column=0)
        self.name_var = tk.StringVar()
        self.age_var = tk.IntVar()
        tk.Entry(frame, textvariable=self.name_var).grid(row=0, column=1)
        tk.Entry(frame, textvariable=self.age_var).grid(row=1, column=1)
        tk.Button(frame, text="Add", command=self.add_student).grid(row=2, column=0)
        tk.Button(frame, text="Update", command=self.update_student).grid(row=2, column=1)
        tk.Button(frame, text="Delete", command=self.delete_student).grid(row=2, column=2)
        self.listbox = tk.Listbox(self.root, width=50)
        self.listbox.pack(padx=10, pady=10)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

    def load_students(self):
        self.listbox.delete(0, tk.END)
        conn = get_connection()
        for row in conn.execute("SELECT * FROM students"):
            self.listbox.insert(tk.END, f"{row[0]}: {row[1]}, {row[2]}")
        conn.close()

    def add_student(self):
        name = self.name_var.get()
        age = self.age_var.get()
        if name:
            conn = get_connection()
            conn.execute("INSERT INTO students(name, age) VALUES(?, ?)", (name, age))
            conn.commit()
            conn.close()
            self.load_students()

    def update_student(self):
        sel = self.listbox.curselection()
        if sel:
            selection = self.listbox.get(sel)
            student_id = int(selection.split(":")[0])
            name = self.name_var.get()
            age = self.age_var.get()
            conn = get_connection()
            conn.execute("UPDATE students SET name=?, age=? WHERE id=?", (name, age, student_id))
            conn.commit()
            conn.close()
            self.load_students()

    def delete_student(self):
        sel = self.listbox.curselection()
        if sel:
            selection = self.listbox.get(sel)
            student_id = int(selection.split(":")[0])
            conn = get_connection()
            conn.execute("DELETE FROM students WHERE id=?", (student_id,))
            conn.commit()
            conn.close()
            self.load_students()

    def on_select(self, event):
        sel = self.listbox.curselection()
        if sel:
            selection = self.listbox.get(sel)
            _, rest = selection.split(":", 1)
            name, age = rest.split(",")
            self.name_var.set(name.strip())
            self.age_var.set(int(age.strip()))

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()