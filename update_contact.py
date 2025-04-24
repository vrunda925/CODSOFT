import tkinter as tk
from tkinter import messagebox
from db_connect import get_connection

def open_update_contact_window(tree):
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a contact to update.")
        return

    values = tree.item(selected_item, "values")
    contact_id, name, phone, email, address = values

    update_window = tk.Toplevel()
    update_window.title("Update Contact")
    update_window.geometry("400x400")
    update_window.configure(bg="#fdf6ec")

    tk.Label(update_window, text="Update Contact", font=("Arial", 16, "bold"), bg="#fdf6ec", fg="#6b4226").pack(pady=10)

    # Name
    tk.Label(update_window, text="Name:", bg="#fdf6ec").pack(anchor='w', padx=30)
    name_entry = tk.Entry(update_window)
    name_entry.pack(padx=30, fill='x')
    name_entry.insert(0, name)

    # Phone
    tk.Label(update_window, text="Phone:", bg="#fdf6ec").pack(anchor='w', padx=30, pady=(10,0))
    phone_entry = tk.Entry(update_window)
    phone_entry.pack(padx=30, fill='x')
    phone_entry.insert(0, phone)

    # Email
    tk.Label(update_window, text="Email:", bg="#fdf6ec").pack(anchor='w', padx=30, pady=(10,0))
    email_entry = tk.Entry(update_window)
    email_entry.pack(padx=30, fill='x')
    email_entry.insert(0, email)

    # Address
    tk.Label(update_window, text="Address:", bg="#fdf6ec").pack(anchor='w', padx=30, pady=(10,0))
    address_entry = tk.Entry(update_window)
    address_entry.pack(padx=30, fill='x')
    address_entry.insert(0, address)

    def update_contact():
        new_name = name_entry.get()
        new_phone = phone_entry.get()
        new_email = email_entry.get()
        new_address = address_entry.get()

        if not new_name or not new_phone:
            messagebox.showerror("Input Error", "Name and phone are required.")
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE contacts 
                SET name = %s, phone = %s, email = %s, address = %s 
                WHERE id = %s
            """, (new_name, new_phone, new_email, new_address, contact_id))
            conn.commit()
            cursor.close()
            conn.close()

            tree.item(selected_item, values=(contact_id, new_name, new_phone, new_email, new_address))
            messagebox.showinfo("Success", "Contact updated successfully.")
            update_window.destroy()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to update contact:\n{e}")

    # Update Button
    tk.Button(update_window, text="Update", command=update_contact, bg="#4CAF50", fg="white").pack(pady=20)
