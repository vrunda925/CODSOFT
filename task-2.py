from tkinter import *
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk

def start_spinner():
    loading_label.pack(pady=5)
    progress_bar.pack(pady=5)
    progress_bar.start(10)
    root.update_idletasks()

def stop_spinner():
    progress_bar.stop()
    loading_label.pack_forget()
    progress_bar.pack_forget()
    root.update_idletasks()

# Submit button logic
def client_user():
    number1 = number1_entry.get()
    number2 = number2_entry.get()
    operation = selected_option.get()

    if not number1 or not number2:
        messagebox.showerror("Error", "Both values are required to proceed!")
        return

    try:
        global num1, num2, selected_operation
        num1 = int(number1)
        num2 = int(number2)
        selected_operation = operation
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers!")
        return

    if selected_operation == "Select-item":
        messagebox.showwarning("Warning", "Please select an operation!")
        return

    start_spinner()
    root.after(1500, process_login)

# Actual calculation after loading
def process_login():
    stop_spinner()

    result = None
    if selected_operation == "Addition +":
        result = num1 + num2
    elif selected_operation == "Subtraction -":
        result = num1 - num2
    elif selected_operation == "Multiplication *":
        result = num1 * num2
    elif selected_operation == "Division /":
        if num2 != 0:
            result = num1 / num2
        else:
            messagebox.showerror("Error", "Division by zero is not allowed!")
            return
    elif selected_operation == "Modulas %":
        if num2 != 0:
            result = num1 % num2
        else:
            messagebox.showerror("Error", "Modulas by zero is not allowed!")
            return
    elif selected_operation == "Exponentiation ^":
        result = num1 ** num2
    else:
        messagebox.showerror("Error", "Invalid operation selected!")
        return

    messagebox.showinfo("Result", f"The result of {selected_operation} is: {result}")
    messagebox.showinfo("Done", "Your operation has been successfully processed!")

# Clear inputs
def clear_fields():
    number1_entry.delete(0, tk.END)
    number2_entry.delete(0, tk.END)
    selected_option.set(options[0])

# GUI setup
root = Tk()
root.title("CALCULATOR")
root.geometry("500x500")

# Background image
bg_image = Image.open("images/login.png")
bg_image = bg_image.resize((1700, 1300), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

frame = Frame(root, bg="white", padx=30, pady=30)
frame.place(relx=0.5, rely=0.5, anchor="center")

heading_label = Label(frame, text="CALCULATOR", font=("Arial", 24, "bold"), bg="white")
heading_label.pack(pady=10)

number1_label = Label(frame, text="Enter a first no:", font=("Arial", 12), bg="white")
number1_label.pack(fill="x")

number1_entry = Entry(frame, width=30)
number1_entry.pack(pady=5)
number1_entry.focus()

number2_label = Label(frame, text="Enter a Second no:", font=("Arial", 12), bg="white")
number2_label.pack(fill="x")

number2_entry = Entry(frame, width=30)
number2_entry.pack(pady=5)

options = ["Select-item", "Addition +", "Subtraction -", "Multiplication *", "Division /", "Modulas %", "Exponentiation ^"]
selected_option = tk.StringVar()
selected_option.set(options[0])

drop_down = tk.OptionMenu(frame, selected_option, *options)
drop_down.pack()

button_frame = Frame(frame, bg="white")
button_frame.pack(pady=10)

submit_button = Button(button_frame, bg="blue", fg="white", text="Submit", command=client_user)
submit_button.pack(side="left", padx=5)

clear_button = Button(button_frame, bg="green", fg="white", text="Clear", command=clear_fields)
clear_button.pack(side="left", padx=5)

loading_label = Label(frame, text="⏳ Processing...", font=("Arial", 10), bg="white", fg="gray")
progress_bar = ttk.Progressbar(frame, mode="indeterminate", length=200)

root.mainloop()
