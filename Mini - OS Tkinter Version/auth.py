import customtkinter as ctk
from tkinter import messagebox
import os

class AuthWindow(ctk.CTkToplevel):
    def __init__(self, parent, login_success_callback):
        super().__init__(parent)
        self.parent = parent
        self.login_success_callback = login_success_callback
        self.mode = "login"

        self.title("Login / Sign Up")
        self.geometry("360x330")
        self.configure(fg_color="#2e2a57")
        self.resizable(False, False)

        ctk.CTkLabel(self, text="Mini OS", font=("Helvetica", 22, "bold"), text_color="#e0e0ff").pack(pady=20)

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username", width=250, height=35,
                                           fg_color="#423e70", text_color="white", corner_radius=15)
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", width=250, height=35,
                                           fg_color="#423e70", text_color="white", corner_radius=15, show="*")
        self.password_entry.pack(pady=10)

        self.action_btn = ctk.CTkButton(self, text="Login", width=250, height=40,
                                        fg_color="#665dff", hover_color="#7a70ff", corner_radius=20,
                                        font=("Helvetica", 14, "bold"), command=self.perform_action)
        self.action_btn.pack(pady=(20, 5))

        self.toggle_btn = ctk.CTkButton(self, text="Create Account", width=250, height=30,
                                        fg_color="transparent", hover_color="#3e3e5e", text_color="#bbbbff",
                                        font=("Helvetica", 12), command=self.toggle_mode)
        self.toggle_btn.pack()

    def toggle_mode(self):
        if self.mode == "login":
            self.mode = "signup"
            self.action_btn.configure(text="Sign Up")
            self.toggle_btn.configure(text="Already have an account?")
        else:
            self.mode = "login"
            self.action_btn.configure(text="Login")
            self.toggle_btn.configure(text="Create Account")

    def perform_action(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Please fill in both fields.")
            return

        if self.mode == "signup":
            if self.user_exists(username):
                messagebox.showerror("Error", "User already exists!")
            else:
                self.save_user(username, password)
                messagebox.showinfo("Success", "Account created! You can now login.")
                self.toggle_mode()
        else:
            if self.validate_login(username, password):
                self.after(200, lambda: [self.login_success_callback(), self.destroy()])
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")

    def user_exists(self, username):
        if not os.path.exists("users.txt"):
            return False
        with open("users.txt", "r") as f:
            for line in f:
                stored_user, _ = line.strip().split(":")
                if stored_user == username:
                    return True
        return False

    def save_user(self, username, password):
        with open("users.txt", "a") as f:
            f.write(f"{username}:{password}\n")

    def validate_login(self, username, password):
        if not os.path.exists("users.txt"):
            return False
        with open("users.txt", "r") as f:
            for line in f:
                stored_user, stored_pass = line.strip().split(":")
                if stored_user == username and stored_pass == password:
                    return True
        return False
