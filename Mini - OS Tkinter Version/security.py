import customtkinter as ctk
from tkinter import simpledialog, messagebox
import os
import json
import stat

class Security(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Security")
        self.geometry("600x450")
        self.configure(fg_color="#2e2f4f")

        # Password Manager data file
        self.pwd_file = os.path.join(os.path.expanduser("~"), "miniOS_passwords.json")
        self.passwords = self.load_passwords()

        # UI layout
        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.pack(expand=True, fill="both", padx=15, pady=15)

        # Tabs
        self.pwd_tab = self.tab_view.add("Password Manager")
        self.folder_tab = self.tab_view.add("Folder Locker")

        self.setup_password_manager()
        self.setup_folder_locker()

    def load_passwords(self):
        if os.path.exists(self.pwd_file):
            try:
                with open(self.pwd_file, "r") as f:
                    return json.load(f)
            except:
                return {}
        else:
            return {}

    def save_passwords(self):
        with open(self.pwd_file, "w") as f:
            json.dump(self.passwords, f)

    # --- Password Manager Tab ---
    def setup_password_manager(self):
        ctk.CTkLabel(self.pwd_tab, text="Website/Service:", font=("Consolas", 14)).pack(pady=(10, 5))
        self.website_entry = ctk.CTkEntry(self.pwd_tab, font=("Consolas", 14))
        self.website_entry.pack(fill="x", padx=20)

        ctk.CTkLabel(self.pwd_tab, text="Username/Email:", font=("Consolas", 14)).pack(pady=(10, 5))
        self.username_entry = ctk.CTkEntry(self.pwd_tab, font=("Consolas", 14))
        self.username_entry.pack(fill="x", padx=20)

        ctk.CTkLabel(self.pwd_tab, text="Password:", font=("Consolas", 14)).pack(pady=(10, 5))
        self.password_entry = ctk.CTkEntry(self.pwd_tab, font=("Consolas", 14), show="*")
        self.password_entry.pack(fill="x", padx=20)

        save_btn = ctk.CTkButton(self.pwd_tab, text="Save Password", command=self.save_password)
        save_btn.pack(pady=15)

        view_btn = ctk.CTkButton(self.pwd_tab, text="View Saved Passwords", command=self.view_passwords)
        view_btn.pack()

    def save_password(self):
        website = self.website_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not website or not username or not password:
            messagebox.showwarning("Warning", "Please fill all fields!")
            return

        self.passwords[website] = {"username": username, "password": password}
        self.save_passwords()
        messagebox.showinfo("Success", f"Password saved for {website}.")

        self.website_entry.delete(0, "end")
        self.username_entry.delete(0, "end")
        self.password_entry.delete(0, "end")

    def view_passwords(self):
        if not self.passwords:
            messagebox.showinfo("Info", "No passwords saved yet.")
            return

        all_pwds = ""
        for site, creds in self.passwords.items():
            all_pwds += f"Site: {site}\nUsername: {creds['username']}\nPassword: {creds['password']}\n\n"

        messagebox.showinfo("Saved Passwords", all_pwds)

    # --- Folder Locker Tab ---
    def setup_folder_locker(self):
        ctk.CTkLabel(self.folder_tab, text="Folder Path to Lock/Unlock:", font=("Consolas", 14)).pack(pady=(10,5))
        self.folder_entry = ctk.CTkEntry(self.folder_tab, font=("Consolas", 14))
        self.folder_entry.pack(fill="x", padx=20)

        lock_btn = ctk.CTkButton(self.folder_tab, text="Lock Folder", command=self.lock_folder)
        lock_btn.pack(pady=(15,5))

        unlock_btn = ctk.CTkButton(self.folder_tab, text="Unlock Folder", command=self.unlock_folder)
        unlock_btn.pack()

    def lock_folder(self):
        path = self.folder_entry.get().strip()
        if not path or not os.path.isdir(path):
            messagebox.showerror("Error", "Invalid folder path!")
            return

        try:
            # On Windows, make folder hidden + read-only
            if os.name == 'nt':
                os.system(f'attrib +h +s "{path}"')
            else:
                # On Linux/Mac, rename folder with dot prefix to hide
                folder_name = os.path.basename(path)
                parent_dir = os.path.dirname(path)
                hidden_path = os.path.join(parent_dir, f".{folder_name}")
                os.rename(path, hidden_path)
            messagebox.showinfo("Success", "Folder locked successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def unlock_folder(self):
        path = self.folder_entry.get().strip()
        if not path:
            messagebox.showerror("Error", "Enter folder path!")
            return

        try:
            if os.name == 'nt':
                os.system(f'attrib -h -s "{path}"')
            else:
                folder_name = os.path.basename(path)
                parent_dir = os.path.dirname(path)
                if folder_name.startswith('.'):
                    new_name = folder_name[1:]
                    new_path = os.path.join(parent_dir, new_name)
                    os.rename(path, new_path)
            messagebox.showinfo("Success", "Folder unlocked successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    app = Security()
    app.mainloop()