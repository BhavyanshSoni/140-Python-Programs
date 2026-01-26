import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import time
import json
import os

# ----------- Core Functions ----------- #
def generate_charset(password_type):
    if password_type == "PIN":
        return string.digits
    elif password_type == "Pattern":
        return "123456789"
    elif password_type == "Typed":
        return string.ascii_letters + string.digits + string.punctuation
    return ""

def simulate_crack(password, charset):
    guessed = ""
    attempts = 0
    start_time = time.time()

    while guessed != password:
        guessed = ''.join(random.choices(charset, k=len(password)))
        attempts += 1
        if attempts > 100000000000000000000:
            break

    end_time = time.time()
    return attempts, round(end_time - start_time, 2)

def save_log(data):
    log_file = "crack_logs.json"
    logs = []

    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            try:
                logs = json.load(f)
            except:
                logs = []

    logs.append(data)
    with open(log_file, "w") as f:
        json.dump(logs, f, indent=4)

# ----------- GUI Setup ----------- #
root = tk.Tk()
root.title("Password Cracker Simulator")
root.geometry("500x450")
root.configure(bg="#1e1e1e")

pattern_input = []

# Title
tk.Label(root, text="Password Cracker Simulator", font=("Arial", 18), bg="#1e1e1e", fg="#39FF14").pack(pady=10)

# Frame
frame = tk.Frame(root, bg="#1e1e1e")
frame.pack(pady=10)

# Dropdown
tk.Label(frame, text="Password Type:", fg="white", bg="#1e1e1e").grid(row=0, column=0, padx=5, pady=5, sticky='e')
type_var = tk.StringVar()
type_dropdown = ttk.Combobox(frame, textvariable=type_var, values=["PIN", "Pattern", "Typed"], state="readonly", width=20)
type_dropdown.grid(row=0, column=1, padx=5)
type_dropdown.current(0)

# Input Entry
entry_label = tk.Label(frame, text="Password:", fg="white", bg="#1e1e1e")
entry_label.grid(row=1, column=0, padx=5, pady=5, sticky='e')
entry_password = tk.Entry(frame, font=("Arial", 14))
entry_password.grid(row=1, column=1, padx=5)

# Pattern Grid
grid_frame = tk.Frame(root, bg="#1e1e1e")
pattern = []
buttons = []

def select_pattern(num, btn):
    if num not in pattern:
        pattern.append(num)
        btn.config(bg="#39FF14")
    else:
        pattern.remove(num)
        btn.config(bg="#303030")

def toggle_input_field():
    p_type = type_var.get()
    if p_type == "Pattern":
        entry_password.grid_remove()
        entry_label.config(text="Pattern Grid:")
        grid_frame.pack(pady=5)
    else:
        entry_label.config(text="Password:")
        entry_password.grid()
        grid_frame.pack_forget()
        pattern.clear()
        for b in buttons:
            b.config(bg="#303030")

type_dropdown.bind("<<ComboboxSelected>>", lambda e: toggle_input_field())

for i in range(3):
    for j in range(3):
        num = str(3 * i + j + 1)
        btn = tk.Button(grid_frame, text=num, width=4, height=2, bg="#303030", fg="white",
                        command=lambda n=num, b=None: select_pattern(n, b))
        btn.grid(row=i, column=j, padx=3, pady=3)
        buttons.append(btn)

# Progress Bar
progress = ttk.Progressbar(root, length=300, mode='determinate')
progress.pack(pady=10)

# Result
result_label = tk.Label(root, text="", font=("Arial", 12), bg="#1e1e1e", fg="white", wraplength=450, justify="center")
result_label.pack(pady=10)

# Simulate Button
def start_crack():
    password_type = type_var.get()
    if password_type == "Pattern":
        if not pattern:
            messagebox.showerror("Input Error", "Please select pattern.")
            return
        password = ''.join(pattern)
    else:
        password = entry_password.get()

    if not password:
        messagebox.showerror("Input Error", "Please enter a password.")
        return

    charset = generate_charset(password_type)
    if not charset:
        messagebox.showerror("Input Error", "Invalid character set.")
        return

    result_label.config(text="Cracking...")
    root.update()

    progress.start()
    attempts, duration = simulate_crack(password, charset)
    progress.stop()

    result_label.config(text=f"Cracked in {attempts:,} attempts\nTime Taken: {duration} seconds")

    save_log({
        "password": password,
        "type": password_type,
        "attempts": attempts,
        "time": duration
    })

btn = tk.Button(root, text="Simulate Crack", command=start_crack, bg="#39FF14", fg="black", font=("Arial", 12))
btn.pack(pady=10)

# Start GUI
toggle_input_field()
root.mainloop()
