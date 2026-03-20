import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.title("Bhavyansh IDE")
root.geometry("800x600")

# Text Editor
editor = tk.Text(root, font=("Consolas", 12))
editor.pack(fill="both", expand=True)

# Open file
def open_file():
    file = filedialog.askopenfilename(filetypes=[("Python Files","*.py"),("All Files","*.*")])
    if file:
        with open(file, "r") as f:
            editor.delete(1.0, tk.END)
            editor.insert(tk.END, f.read())

# Save file
def save_file():
    file = filedialog.asksaveasfilename(defaultextension=".py")
    if file:
        with open(file, "w") as f:
            f.write(editor.get(1.0, tk.END))

# Menu bar
menu = tk.Menu(root)

file_menu = tk.Menu(menu, tearoff=0)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)

menu.add_cascade(label="File", menu=file_menu)

root.config(menu=menu)

root.mainloop()