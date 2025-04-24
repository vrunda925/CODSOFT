from tkinter import *
import tkinter as tk
from tkinter import messagebox
import re
from view_contact import open_view_contact_window
from db_connect import get_connection  # import connection function

# Main window setup
root = tk.Tk()
root.title("Contact Book")
root.geometry("700x700")
root.configure(bg="#E6E6FA")  # lavender background

frame = tk.Frame(root, bg="#E6E6FA")
frame.pack(fill=BOTH, expand=True)

form_frame = Frame(frame, bg="#301934", bd=2, width=600, height=600)
form_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
form_frame.pack_propagate(False)

heading_label = Label(frame, text="Contact Book 📖", font=("Arial", 14, "bold"), bg="#f8f9fa")
heading_label.place(relx=0.5, rely=0.05, anchor=CENTER)

# Navbar
navbar_frame = Frame(form_frame, bg="#301934")
navbar_frame.grid(row=0, column=0, columnspan=2, pady=20)

viewcontact_button = Button(navbar_frame, text="View contact List", command=lambda: open_view_contact_window(root), bg="#8A2BE2", fg="white")
viewcontact_button.grid(row=0, column=1, padx=10)

search_entry = Entry(navbar_frame, width=20, bg="#E6E6FA")
search_entry.grid(row=0, column=3, padx=10)

search_button = Button(navbar_frame, text="Search", bg="#8A2BE2", fg="white")
search_button.grid(row=0, column=4, padx=10)

# Form fields
Label(form_frame, text="Name 🙋🏻:", bg="#f8f9fa", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
name_entry = Entry(form_frame, width=30)
name_entry.grid(row=1, column=1, padx=10, pady=10)

Label(form_frame, text="Phone Number 📞:", bg="#f8f9fa", font=("Arial", 10)).grid(row=2, column=0, padx=10, pady=10, sticky="e")
phone_entry = Entry(form_frame, width=30)
phone_entry.grid(row=2, column=1, padx=10, pady=10)

Label(form_frame, text="Email ✉️:", bg="#f8f9fa", font=("Arial", 10)).grid(row=3, column=0, padx=10, pady=10, sticky="e")
email_entry = Entry(form_frame, width=30)
email_entry.grid(row=3, column=1, padx=10, pady=10)

Label(form_frame, text="Address 📍:", bg="#f8f9fa", font=("Arial", 10)).grid(row=4, column=0, padx=10, pady=10, sticky="e")
address_entry = Text(form_frame, width=30, height=3)
address_entry.grid(row=4, column=1, padx=10, pady=10)

# Validation function
def validate_form():
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    address = address_entry.get("1.0", "end-1c")

    if not name:
        messagebox.showerror("Input Error", "Please enter your name.")
        return False

    if not phone.isdigit() or len(phone) != 10:
        messagebox.showerror("Input Error", "Please enter a valid 10-digit phone number.")
        return False

    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        messagebox.showerror("Input Error", "Please enter a valid email address.")
        return False

    if not address.strip():
        messagebox.showerror("Input Error", "Please enter your address.")
        return False

    return True

# Submit function
def submit_form():
    if validate_form():
        name = name_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        address = address_entry.get("1.0", "end-1c")

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO contacts (name, phone, email, address) VALUES (%s, %s, %s, %s)", 
                           (name, phone, email, address))
            conn.commit()

            messagebox.showinfo("Success", "Contact added successfully!")

            # Clear inputs
            name_entry.delete(0, END)
            phone_entry.delete(0, END)
            email_entry.delete(0, END)
            address_entry.delete("1.0", "end")

            cursor.close()
            conn.close()

        except Exception as e:
            messagebox.showerror("Database Error", f"Something went wrong!\n{e}")

# Search functionality
def search_contact():
    search_term = search_entry.get()
    
    if not search_term:
        messagebox.showwarning("Input Error", "Please enter a search term.")
        return

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Search query - searching by name, phone, or email
        cursor.execute("""
            SELECT * FROM contacts 
            WHERE name LIKE %s OR phone LIKE %s OR email LIKE %s
        """, ('%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%'))
        
        results = cursor.fetchall()

        if results:
            # Creating a new window to display the search results
            result_window = Toplevel(root)
            result_window.title("Search Results")
            result_window.geometry("600x400")
            result_window.configure(bg="#f8f9fa")  # Set background color

            # Add heading
            result_heading = Label(result_window, text="Search Results", font=("Arial", 14, "bold"), bg="#8A2BE2", fg="white")
            result_heading.pack(fill=X)

            # Create a canvas and a scrollbar
            canvas = Canvas(result_window, bg="#f8f9fa")
            scrollbar = Scrollbar(result_window, orient="vertical", command=canvas.yview)
            scrollable_frame = Frame(canvas)

            scrollable_frame.bind(
                "<Configure>", 
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side=LEFT, fill=BOTH, expand=True)
            scrollbar.pack(side=RIGHT, fill=Y)

            # Display results in the scrollable frame
            for row in results:
                contact_info = f"Name: {row[0]}\nPhone: {row[1]}\nEmail: {row[2]}\nAddress: {row[3]}\n\n"
                result_label = Label(scrollable_frame, text=contact_info, anchor="w", bg="#f8f9fa", font=("Arial", 10))
                result_label.pack(padx=10, pady=5, anchor="w")

            result_window.mainloop()
        else:
            messagebox.showinfo("No Results", "No matching contacts found.")
        
        cursor.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Database Error", f"Something went wrong!\n{e}")

# Update search_button to use the search_contact function
search_button.config(command=search_contact)

# Submit button
submit_button = Button(form_frame, text="Add contact", bg="#8A2BE2", fg="white", command=submit_form)
submit_button.grid(row=5, column=0, columnspan=2, pady=20)

root.mainloop()
