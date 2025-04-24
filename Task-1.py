import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import os

# ----- Main Application Class -----
class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📝 To-Do List")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        self.tasks = []

        self.create_widgets()

    def create_widgets(self):
        # --------- Title ----------
        tk.Label(self.root, text="✨ My Stylish To-Do List", font=("Helvetica", 20, "bold"), fg="#333").pack(pady=10)

        # --------- Entry + Priority ----------
        entry_frame = tk.Frame(self.root)
        entry_frame.pack(pady=10)

        self.task_entry = tk.Entry(entry_frame, font=("Helvetica", 14), width=25)
        self.task_entry.pack(side=tk.LEFT, padx=5)
        self.task_entry.focus()

        self.priority_var = tk.StringVar()
        self.priority_var.set("Medium")
        priority_menu = ttk.Combobox(entry_frame, textvariable=self.priority_var, state="readonly",
                                     values=["High", "Medium", "Low"], width=10)
        priority_menu.pack(side=tk.LEFT)

        # --------- Buttons ----------
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Add Task", command=self.add_task, width=12, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Delete Task", command=self.delete_task, width=12, bg="#f44336", fg="white").grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Mark Done", command=self.mark_done, width=12, bg="#2196F3", fg="white").grid(row=0, column=2, padx=5)

        # --------- Listbox ----------
        self.task_listbox = tk.Listbox(self.root, font=("Helvetica", 12), selectbackground="#ddd", height=20)
        self.task_listbox.pack(pady=10, padx=20, fill='both')

        # --------- Bottom Buttons ----------
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(pady=5)

        tk.Button(bottom_frame, text="Save List", command=self.save_tasks, bg="#607D8B", fg="white", width=12).grid(row=0, column=0, padx=10)
        tk.Button(bottom_frame, text="Load List", command=self.load_tasks, bg="#607D8B", fg="white", width=12).grid(row=0, column=1, padx=10)
        tk.Button(bottom_frame, text="Clear All", command=self.clear_all, bg="#9C27B0", fg="white", width=12).grid(row=0, column=2, padx=10)

    def get_task_display(self, task_text, priority):
        symbol = {"High": "🔥", "Medium": "⚡", "Low": "🌱"}
        return f"[{priority}] {task_text} {symbol.get(priority, '')}"

    def add_task(self):
        task = self.task_entry.get().strip()
        priority = self.priority_var.get()
        if task:
            task_display = self.get_task_display(task, priority)
            self.tasks.append((task_display, priority, False))  # (task_text, priority, is_done)
            self.sort_tasks()
            self.refresh_tasks()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Enter a task!")

    def delete_task(self):
        try:
            index = self.task_listbox.curselection()[0]
            del self.tasks[index]
            self.refresh_tasks()
        except IndexError:
            messagebox.showwarning("Warning", "Select a task to delete!")

    def mark_done(self):
        try:
            index = self.task_listbox.curselection()[0]
            task, priority, _ = self.tasks[index]
            if not task.endswith("✔"):
                self.tasks[index] = (task + " ✔", priority, True)
                self.sort_tasks()
                self.refresh_tasks()
        except IndexError:
            messagebox.showwarning("Warning", "Select a task to mark as done!")

    def clear_all(self):
        confirm = messagebox.askyesno("Clear All", "Are you sure you want to clear all tasks?")
        if confirm:
            self.tasks.clear()
            self.task_listbox.delete(0, tk.END)

    def save_tasks(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                for task, priority, is_done in self.tasks:
                    f.write(f"{task}||{priority}||{is_done}\n")
            messagebox.showinfo("Saved", "Tasks saved successfully!")

    def load_tasks(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path and os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                self.tasks = []
                for line in f:
                    parts = line.strip().split("||")
                    if len(parts) == 3:
                        self.tasks.append((parts[0], parts[1], parts[2] == "True"))
            self.sort_tasks()
            self.refresh_tasks()
            messagebox.showinfo("Loaded", "Tasks loaded successfully!")

    def refresh_tasks(self):
        self.task_listbox.delete(0, tk.END)
        for task, _, _ in self.tasks:
            self.task_listbox.insert(tk.END, task)

    def sort_tasks(self):
        priority_order = {"High": 1, "Medium": 2, "Low": 3}
        self.tasks.sort(key=lambda x: (x[2], priority_order.get(x[1], 4)))

# ----- Run App -----
if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
