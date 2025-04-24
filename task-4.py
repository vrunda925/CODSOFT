import tkinter as tk
from tkinter import ttk
import random

# Logic
choices = ["rock", "paper", "scissors"]
result = ""
user_score = 0
computer_score = 0

root = tk.Tk()
root.title("Rock, Paper, Scissors")
root.geometry("500x500")
root.config(bg="pink")

def exit_application():
    root.destroy()

def play(user_choice):
    global result, user_score, computer_score
    computer_choice = random.choice(choices)
    
    if user_choice == computer_choice:
        result = f"It's a tie! Both chose {computer_choice}."
    elif user_choice == "rock":
        if computer_choice == "scissors":
            result = f"You win! Rock crushes scissors. Computer chose {computer_choice}."
            user_score += 1
        else:
            result = f"You lose! Paper covers rock. Computer chose {computer_choice}."
            computer_score += 1
    elif user_choice == "paper":
        if computer_choice == "rock":
            result = f"You win! Paper covers rock. Computer chose {computer_choice}."
            user_score += 1
        else:
            result = f"You lose! Scissors cut paper. Computer chose {computer_choice}."
            computer_score += 1
    elif user_choice == "scissors":
        if computer_choice == "paper":
            result = f"You win! Scissors cut paper. Computer chose {computer_choice}."
            user_score += 1
        else:
            result = f"You lose! Rock crushes scissors. Computer chose {computer_choice}."
            computer_score += 1

    result_label.config(text=result)
    score_label.config(text=f"Your Score: {user_score} | Computer Score: {computer_score}")

def restart_game():
    global user_score, computer_score, result
    user_score = 0
    computer_score = 0
    result = ""
    result_label.config(text="Make your choice!")
    score_label.config(text="Your Score: 0 | Computer Score: 0")

# Title Label
title_label = tk.Label(
    root,
    text="Rock Paper Scissors",
    font=("Helvetica", 20, "bold"),
    bg="#f0f0f0",
    fg="#333"
)
title_label.pack(pady=20)

# Buttons Frame
button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.pack(pady=10)

rock_btn = ttk.Button(button_frame, text="🪨 Rock", command=lambda: play("rock"))
rock_btn.grid(row=0, column=0, padx=10, ipadx=10, ipady=5)

paper_btn = ttk.Button(button_frame, text="📄 Paper", command=lambda: play("paper"))
paper_btn.grid(row=0, column=1, padx=10, ipadx=10, ipady=5)

scissors_btn = ttk.Button(button_frame, text="✂ Scissors", command=lambda: play("scissors"))
scissors_btn.grid(row=0, column=2, padx=10, ipadx=10, ipady=5)

# Result Label
result_label = tk.Label(
    root,
    text="Make your choice!",
    font=("Helvetica", 14),
    bg="#f0f0f0",
    fg="#555"
)
result_label.pack(pady=20)

# Score Label
score_label = tk.Label(
    root,
    text="Your Score: 0 | Computer Score: 0",
    font=("Helvetica", 14, "bold"),
    bg="#f0f0f0",
    fg="#333"
)
score_label.pack(pady=10)

# Restart Button
restart_btn = ttk.Button(root, text="🔁 Restart", command=restart_game)
restart_btn.pack(pady=10)

# Exit Button
exit_btn = ttk.Button(root, text="Exit", command=exit_application)
exit_btn.pack(pady=10)

# Mainloop
root.mainloop()
