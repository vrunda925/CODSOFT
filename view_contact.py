import tkinter as tk
from tkinter import ttk, messagebox
from db_connect import get_connection
from update_contact import open_update_contact_window
import subprocess  # For running external files, if required


def delete_contact(tree):
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a contact to delete.")
        return

    values = tree.item(selected_item, "values")
    contact_id = values[0]

    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this contact?")
    if confirm:
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM contacts WHERE id = %s", (contact_id,))
            conn.commit()
            cursor.close()
            conn.close()

            tree.delete(selected_item)
            messagebox.showinfo("Deleted", "Contact deleted successfully.")
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to delete contact:\n{e}")


def go_back():
    try:
        # Use pythonw.exe to avoid opening a command prompt
        subprocess.run(['pythonw', 'task-5.py'])  # 'pythonw' does not open a cmd window
    except Exception as e:
        messagebox.showerror("Error", f"Failed to go back:\n{e}")


def open_view_contact_window(parent_window):
    parent_window.destroy()  # Close the contact.py file (if running as part of a flow)
    
    view_window = tk.Tk()
    view_window.title("View Contacts")
    view_window.geometry("750x400")
    view_window.configure(bg="#f0f8ff")

    title_label = tk.Label(view_window, text="Contact List", font=("Helvetica", 16, "bold"), bg="#f0f8ff", fg="#4b0082")
    title_label.pack(pady=10)

    tree_frame = tk.Frame(view_window)
    tree_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    tree_scroll_y = tk.Scrollbar(tree_frame, orient=tk.VERTICAL)
    tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

    tree_scroll_x = tk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
    tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

    tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set,
                        columns=("ID", "Name", "Phone", "Email", "Address"), show="headings")

    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Phone", text="Phone")
    tree.heading("Email", text="Email")
    tree.heading("Address", text="Address")

    tree.column("ID", width=40, anchor=tk.CENTER)
    tree.column("Name", width=150)
    tree.column("Phone", width=100)
    tree.column("Email", width=200)
    tree.column("Address", width=250)

    tree.pack(fill=tk.BOTH, expand=True)

    tree_scroll_y.config(command=tree.yview)
    tree_scroll_x.config(command=tree.xview)

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contacts")
        records = cursor.fetchall()

        for row in records:
            tree.insert("", tk.END, values=row)

        cursor.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to load contacts:\n{e}")

    button_frame = tk.Frame(view_window, bg="#f0f8ff")
    button_frame.pack(pady=10)

    # Pass 'tree' as an argument using lambda
    delete_button = tk.Button(button_frame, text="Delete Contact", command=lambda: delete_contact(tree), bg="red", fg="white")
    delete_button.pack(side=tk.LEFT, padx=10)

    update_button = tk.Button(button_frame, text="Update Contact", command=lambda: open_update_contact_window(tree), bg="green", fg="white")
    update_button.pack(side=tk.LEFT, padx=10)

    # Add Back button
    back_button = tk.Button(button_frame, text="Back", command=go_back, bg="blue", fg="white")
    back_button.pack(side=tk.LEFT, padx=10)

    view_window.mainloop()
