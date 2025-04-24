from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import random

# Character sets
lowercase = "abcdefghijklmnopqrstuvwxyz"
uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
numbers = "0123456789"
symbols = "~`@#$%^&*()_-"

# Create window
root = Tk()
root.title("Password Generator")
root.geometry("600x600")
root.configure(bg="#f8f9fa")

# Background setup
frame = Frame(root, bg="#f8f9fa")
frame.pack(fill=BOTH, expand=True)

bg_image = Image.open("images/register.jpg")
bg_image = bg_image.resize((600, 600), Image.Resampling.LANCZOS)
bg_image = ImageTk.PhotoImage(bg_image)

bg_label = Label(frame, image=bg_image)
bg_label.place(relwidth=1, relheight=1)
bg_label.image = bg_image

form_frame = Frame(frame, bg="#f8f9fa", bd=2, width=500, height=500)
form_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
form_frame.pack_propagate(False)

heading_label = Label(frame, text="Password Generator", font=("Arial", 14, "bold"), bg="#f8f9fa")
heading_label.place(relx=0.5, rely=0.05, anchor=CENTER)

# User input fields
Label(form_frame, text="Enter Your Name:", bg="#f8f9fa", font=("Arial", 10)).pack(pady=5)
username_entry = Entry(form_frame, width=30)
username_entry.pack(pady=5)

Label(form_frame, text="Enter Desired Password Length:", bg="#f8f9fa", font=("Arial", 10)).pack(pady=5)
password_entry = Entry(form_frame, width=30)
password_entry.pack(pady=5)

# Strength selection
Label(form_frame, text="Select Password Strength:", bg="#f8f9fa", font=("Arial", 10)).pack(pady=5)
strength_var = StringVar(value="strong")
Radiobutton(form_frame, text="Weak", variable=strength_var, value="weak", bg="#f8f9fa").pack()
Radiobutton(form_frame, text="Medium", variable=strength_var, value="medium", bg="#f8f9fa").pack()
Radiobutton(form_frame, text="Strong", variable=strength_var, value="strong", bg="#f8f9fa").pack()

# Display label
generated_password_label = Label(form_frame, text="", bg="#f8f9fa", font=("Arial", 10, "bold"))
generated_password_label.pack(pady=10)

# Password generation logic
def generate_password():
    user_name = username_entry.get().strip()
    try:
        password_length = int(password_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Password length must be a number.")
        return

    if not user_name:
        messagebox.showerror("Missing Name", "Please enter your name.")
        return

    if password_length <= len(user_name):
        messagebox.showerror("Invalid Length", "Password length must be greater than the length of your name.")
        return

    # Get selected strength
    strength = strength_var.get()
    if strength == "weak":
        char_set = lowercase + uppercase
    elif strength == "medium":
        char_set = lowercase + uppercase + numbers
    else:  # strong
        char_set = lowercase + uppercase + numbers + symbols

    random_length = password_length - len(user_name)
    random_part = ''.join(random.choices(char_set, k=random_length))
    combined = user_name + random_part
    password = ''.join(random.sample(combined, len(combined)))

    # Show password
    generated_password_label.config(text=f"Generated Password:\n{password}")

# Button
generate_button = Button(form_frame, text="Generate Password", command=generate_password, bg="#007bff", fg="white", font=("Arial", 10, "bold"))
generate_button.pack(pady=10)

root.mainloop()
