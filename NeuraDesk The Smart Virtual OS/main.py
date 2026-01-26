"""
NeuraDesk - Advanced AI-powered Virtual Operating System
A feature-rich desktop application built with Python Tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import os
import json
import hashlib
import base64
import datetime
import math
import shutil
import subprocess
import sys
from pathlib import Path
import sqlite3
from cryptography.fernet import Fernet
import secrets
import string

class NeuraDesk:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("NeuraDesk - AI Virtual OS")
        self.root.geometry("1100x650")
        self.root.resizable(False, False)
        self.root.configure(bg='#2b2b40')
        
        # Color scheme
        self.colors = {
            'bg_primary': '#2b2b40',
            'bg_secondary': '#3e3e55', 
            'bg_tertiary': '#505070',
            'text_primary': '#ffffff',
            'text_secondary': '#cccccc',
            'accent': '#8a7aff',
            'hover': '#6b5fcc'
        }
        
        # Initialize data directory
        self.data_dir = Path.home() / ".neuradesk"
        self.data_dir.mkdir(exist_ok=True)
        
        # Current active app
        self.current_app = None
        
        # Initialize UI
        self.setup_ui()
        self.setup_apps()
        
    def setup_ui(self):
        """Setup the main UI structure"""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Sidebar
        self.sidebar = tk.Frame(main_frame, bg=self.colors['bg_secondary'], width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)
        
        # Title
        title_label = tk.Label(
            self.sidebar,
            text="NeuraDesk",
            font=("Segoe UI", 16, "bold"),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary']
        )
        title_label.pack(pady=20)
        
        # Main content area
        self.main_content = tk.Frame(main_frame, bg=self.colors['bg_primary'])
        self.main_content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Welcome screen
        self.show_welcome()
        
    def create_sidebar_button(self, text, command, icon="📱"):
        """Create a styled sidebar button"""
        btn_frame = tk.Frame(self.sidebar, bg=self.colors['bg_secondary'])
        btn_frame.pack(fill=tk.X, padx=10, pady=2)
        
        btn = tk.Button(
            btn_frame,
            text=f"{icon} {text}",
            command=command,
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_primary'],
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            anchor=tk.W,
            padx=15,
            pady=8,
            cursor="hand2"
        )
        btn.pack(fill=tk.X)
        
        # Hover effects
        def on_enter(e):
            btn.configure(bg=self.colors['hover'])
            
        def on_leave(e):
            btn.configure(bg=self.colors['bg_tertiary'])
            
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
        
    def setup_apps(self):
        """Setup all integrated applications"""
        self.apps = {
            'notes': NotesApp(self),
            'calculator': CalculatorApp(self),
            'file_explorer': FileExplorerApp(self),
            'secure_vault': SecureVaultApp(self),
            'expense_tracker': ExpenseTrackerApp(self),
            'reminder': ReminderApp(self),
            'chatbot': ChatbotApp(self),
            'ai_assistant': AIAssistantApp(self),
            'password_manager': PasswordManagerApp(self),
            'folder_locker': FolderLockerApp(self),
            'task_manager': TaskManagerApp(self),
            'weather': WeatherApp(self)
        }
        
        # Create sidebar buttons
        self.create_sidebar_button("Notes", lambda: self.show_app('notes'), "📝")
        self.create_sidebar_button("Calculator", lambda: self.show_app('calculator'), "🧮")
        self.create_sidebar_button("File Explorer", lambda: self.show_app('file_explorer'), "📁")
        self.create_sidebar_button("Secure Vault", lambda: self.show_app('secure_vault'), "🔒")
        self.create_sidebar_button("Expense Tracker", lambda: self.show_app('expense_tracker'), "💰")
        self.create_sidebar_button("Reminders", lambda: self.show_app('reminder'), "⏰")
        self.create_sidebar_button("Chatbot", lambda: self.show_app('chatbot'), "🤖")
        self.create_sidebar_button("AI Assistant", lambda: self.show_app('ai_assistant'), "🧠")
        self.create_sidebar_button("Password Manager", lambda: self.show_app('password_manager'), "🔑")
        self.create_sidebar_button("Folder Locker", lambda: self.show_app('folder_locker'), "🗂️")
        self.create_sidebar_button("Task Manager", lambda: self.show_app('task_manager'), "📋")
        self.create_sidebar_button("Weather", lambda: self.show_app('weather'), "🌤️")
        
    def show_welcome(self):
        """Show welcome screen"""
        self.clear_main_content()
        
        welcome_frame = tk.Frame(self.main_content, bg=self.colors['bg_primary'])
        welcome_frame.pack(expand=True, fill=tk.BOTH)
        
        # Center content
        center_frame = tk.Frame(welcome_frame, bg=self.colors['bg_primary'])
        center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        tk.Label(
            center_frame,
            text="Welcome to NeuraDesk",
            font=("Segoe UI", 24, "bold"),
            bg=self.colors['bg_primary'],
            fg=self.colors['text_primary']
        ).pack(pady=20)
        
        tk.Label(
            center_frame,
            text="Your AI-Powered Virtual Operating System",
            font=("Segoe UI", 14),
            bg=self.colors['bg_primary'],
            fg=self.colors['text_secondary']
        ).pack(pady=10)
        
        tk.Label(
            center_frame,
            text="Select an app from the sidebar to get started",
            font=("Segoe UI", 12),
            bg=self.colors['bg_primary'],
            fg=self.colors['text_secondary']
        ).pack(pady=10)
        
    def show_app(self, app_name):
        """Show the specified app"""
        if app_name in self.apps:
            self.current_app = app_name
            self.clear_main_content()
            self.apps[app_name].show()
            
    def clear_main_content(self):
        """Clear the main content area"""
        for widget in self.main_content.winfo_children():
            widget.destroy()
            
    def run(self):
        """Start the application"""
        self.root.mainloop()

class BaseApp:
    """Base class for all integrated apps"""
    def __init__(self, parent):
        self.parent = parent
        self.frame = None
        
    def show(self):
        """Show the app interface"""
        self.frame = tk.Frame(self.parent.main_content, bg=self.parent.colors['bg_primary'])
        self.frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        self.create_interface()
        
    def create_interface(self):
        """Override this method to create app interface"""
        pass
        
    def create_title(self, text):
        """Create a title label"""
        return tk.Label(
            self.frame,
            text=text,
            font=("Segoe UI", 18, "bold"),
            bg=self.parent.colors['bg_primary'],
            fg=self.parent.colors['text_primary']
        )
        
    def create_button(self, text, command, **kwargs):
        """Create a styled button"""
        return tk.Button(
            self.frame,
            text=text,
            command=command,
            bg=self.parent.colors['bg_tertiary'],
            fg=self.parent.colors['text_primary'],
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor="hand2",
            **kwargs
        )

class NotesApp(BaseApp):
    def __init__(self, parent):
        super().__init__(parent)
        self.notes_file = parent.data_dir / "notes.json"
        self.notes = self.load_notes()
        
    def create_interface(self):
        title = self.create_title("📝 Notes")
        title.pack(pady=(0, 20))
        
        # Toolbar
        toolbar = tk.Frame(self.frame, bg=self.parent.colors['bg_primary'])
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        self.create_button("New Note", self.new_note).pack(side=tk.LEFT, padx=(0, 10))
        self.create_button("Save", self.save_note).pack(side=tk.LEFT, padx=(0, 10))
        self.create_button("Delete", self.delete_note).pack(side=tk.LEFT, padx=(0, 10))
        
        # Notes list and editor
        content_frame = tk.Frame(self.frame, bg=self.parent.colors['bg_primary'])
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Notes list
        list_frame = tk.Frame(content_frame, bg=self.parent.colors['bg_secondary'], width=200)
        list_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        list_frame.pack_propagate(False)
        
        tk.Label(list_frame, text="Notes", font=("Segoe UI", 12, "bold"),
                bg=self.parent.colors['bg_secondary'], fg=self.parent.colors['text_primary']).pack(pady=10)
        
        self.notes_listbox = tk.Listbox(
            list_frame,
            bg=self.parent.colors['bg_tertiary'],
            fg=self.parent.colors['text_primary'],
            selectbackground=self.parent.colors['accent'],
            font=("Segoe UI", 10),
            relief=tk.FLAT
        )
        self.notes_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        self.notes_listbox.bind('<<ListboxSelect>>', self.on_note_select)
        
        # Editor
        editor_frame = tk.Frame(content_frame, bg=self.parent.colors['bg_primary'])
        editor_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Note title
        self.title_var = tk.StringVar()
        title_entry = tk.Entry(
            editor_frame,
            textvariable=self.title_var,
            bg=self.parent.colors['bg_secondary'],
            fg=self.parent.colors['text_primary'],
            font=("Segoe UI", 12, "bold"),
            relief=tk.FLAT
        )
        title_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Note content
        self.text_editor = tk.Text(
            editor_frame,
            bg=self.parent.colors['bg_secondary'],
            fg=self.parent.colors['text_primary'],
            font=("Consolas", 11),
            relief=tk.FLAT,
            wrap=tk.WORD
        )
        self.text_editor.pack(fill=tk.BOTH, expand=True)
        
        self.refresh_notes_list()
        
    def load_notes(self):
        try:
            if self.notes_file.exists():
                with open(self.notes_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return {}
        
    def save_notes(self):
        with open(self.notes_file, 'w') as f:
            json.dump(self.notes, f, indent=2)
            
    def refresh_notes_list(self):
        self.notes_listbox.delete(0, tk.END)
        for note_id, note in self.notes.items():
            self.notes_listbox.insert(tk.END, note['title'])
            
    def new_note(self):
        title = simpledialog.askstring("New Note", "Enter note title:")
        if title:
            note_id = str(len(self.notes) + 1)
            self.notes[note_id] = {
                'title': title,
                'content': '',
                'created': datetime.datetime.now().isoformat()
            }
            self.save_notes()
            self.refresh_notes_list()
            
    def save_note(self):
        selection = self.notes_listbox.curselection()
        if selection:
            note_id = str(selection[0] + 1)
            if note_id in self.notes:
                self.notes[note_id]['title'] = self.title_var.get()
                self.notes[note_id]['content'] = self.text_editor.get(1.0, tk.END)
                self.save_notes()
                self.refresh_notes_list()
                messagebox.showinfo("Success", "Note saved!")
                
    def delete_note(self):
        selection = self.notes_listbox.curselection()
        if selection:
            if messagebox.askyesno("Confirm", "Delete this note?"):
                note_id = str(selection[0] + 1)
                if note_id in self.notes:
                    del self.notes[note_id]
                    self.save_notes()
                    self.refresh_notes_list()
                    self.title_var.set("")
                    self.text_editor.delete(1.0, tk.END)
                    
    def on_note_select(self, event):
        selection = self.notes_listbox.curselection()
        if selection:
            note_id = str(selection[0] + 1)
            if note_id in self.notes:
                note = self.notes[note_id]
                self.title_var.set(note['title'])
                self.text_editor.delete(1.0, tk.END)
                self.text_editor.insert(1.0, note['content'])

class CalculatorApp(BaseApp):
    def __init__(self, parent):
        super().__init__(parent)
        self.display_var = tk.StringVar(value="0")
        self.expression = ""
        
    def create_interface(self):
        title = self.create_title("🧮 Calculator")
        title.pack(pady=(0, 20))
        
        # Calculator frame
        calc_frame = tk.Frame(self.frame, bg=self.parent.colors['bg_primary'])
        calc_frame.pack(expand=True)
        
        # Display
        display = tk.Entry(
            calc_frame,
            textvariable=self.display_var,
            font=("Consolas", 20),
            bg=self.parent.colors['bg_secondary'],
            fg=self.parent.colors['text_primary'],
            relief=tk.FLAT,
            justify=tk.RIGHT,
            state='readonly'
        )
        display.pack(fill=tk.X, pady=(0, 10))
        
        # Buttons
        buttons = [
            ['C', '±', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]
        
        for row in buttons:
            button_row = tk.Frame(calc_frame, bg=self.parent.colors['bg_primary'])
            button_row.pack(fill=tk.X, pady=2)
            
            for button_text in row:
                if button_text == '0':
                    btn = tk.Button(
                        button_row,
                        text=button_text,
                        command=lambda t=button_text: self.button_click(t),
                        bg=self.parent.colors['bg_tertiary'],
                        fg=self.parent.colors['text_primary'],
                        font=("Segoe UI", 14),
                        relief=tk.FLAT,
                        width=10 if button_text == '0' else 5,
                        height=2
                    )
                    btn.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
                else:
                    btn = tk.Button(
                        button_row,
                        text=button_text,
                        command=lambda t=button_text: self.button_click(t),
                        bg=self.parent.colors['accent'] if button_text in ['=', '+', '-', '×', '÷'] else self.parent.colors['bg_tertiary'],
                        fg=self.parent.colors['text_primary'],
                        font=("Segoe UI", 14),
                        relief=tk.FLAT,
                        width=5,
                        height=2
                    )
                    btn.pack(side=tk.LEFT, padx=2)
                    
    def button_click(self, value):
        if value == 'C':
            self.expression = ""
            self.display_var.set("0")
        elif value == '=':
            try:
                # Replace symbols for evaluation
                expr = self.expression.replace('×', '*').replace('÷', '/')
                result = eval(expr)
                self.display_var.set(str(result))
                self.expression = str(result)
            except:
                self.display_var.set("Error")
                self.expression = ""
        elif value == '±':
            if self.expression and self.expression != "0":
                if self.expression[0] == '-':
                    self.expression = self.expression[1:]
                else:
                    self.expression = '-' + self.expression
                self.display_var.set(self.expression)
        elif value == '%':
            try:
                result = float(self.expression) / 100
                self.expression = str(result)
                self.display_var.set(self.expression)
            except:
                pass
        else:
            if self.expression == "0" and value.isdigit():
                self.expression = value
            else:
                self.expression += value
            self.display_var.set(self.expression)

class FileExplorerApp(BaseApp):
    def __init__(self, parent):
        super().__init__(parent)
        self.current_path = Path.home()
        
    def create_interface(self):
        title = self.create_title("📁 File Explorer")
        title.pack(pady=(0, 20))
        
        # Toolbar
        toolbar = tk.Frame(self.frame, bg=self.parent.colors['bg_primary'])
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        self.path_var = tk.StringVar(value=str(self.current_path))
        path_entry = tk.Entry(
            toolbar,
            textvariable=self.path_var,
            bg=self.parent.colors['bg_secondary'],
            fg=self.parent.colors['text_primary'],
            font=("Consolas", 10),
            relief=tk.FLAT
        )
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        self.create_button("Go", self.navigate_to_path).pack(side=tk.LEFT, padx=(0, 10))
        self.create_button("Up", self.go_up).pack(side=tk.LEFT, padx=(0, 10))
        self.create_button("New Folder", self.create_folder).pack(side=tk.LEFT, padx=(0, 10))
        
        # File list
        list_frame = tk.Frame(self.frame, bg=self.parent.colors['bg_primary'])
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.file_listbox = tk.Listbox(
            list_frame,
            bg=self.parent.colors['bg_secondary'],
            fg=self.parent.colors['text_primary'],
            selectbackground=self.parent.colors['accent'],
            font=("Consolas", 10),
            relief=tk.FLAT,
            yscrollcommand=scrollbar.set
        )
        self.file_listbox.pack(fill=tk.BOTH, expand=True)
        self.file_listbox.bind('<Double-1>', self.on_double_click)
        
        scrollbar.config(command=self.file_listbox.yview)
        
        # Context menu
        self.context_menu = tk.Menu(self.frame, tearoff=0)
        self.context_menu.add_command(label="Delete", command=self.delete_item)
        self.context_menu.add_command(label="Rename", command=self.rename_item)
        
        self.file_listbox.bind('<Button-3>', self.show_context_menu)
        
        self.refresh_file_list()
        
    def refresh_file_list(self):
        self.file_listbox.delete(0, tk.END)
        self.path_var.set(str(self.current_path))
        
        try:
            # Add parent directory
            if self.current_path != self.current_path.parent:
                self.file_listbox.insert(tk.END, "📁 ..")
                
            # List directories first
            for item in sorted(self.current_path.iterdir()):
                if item.is_dir():
                    self.file_listbox.insert(tk.END, f"📁 {item.name}")
                    
            # Then files
            for item in sorted(self.current_path.iterdir()):
                if item.is_file():
                    self.file_listbox.insert(tk.END, f"📄 {item.name}")
                    
        except PermissionError:
            messagebox.showerror("Error", "Permission denied")
            
    def navigate_to_path(self):
        try:
            path = Path(self.path_var.get())
            if path.exists() and path.is_dir():
                self.current_path = path
                self.refresh_file_list()
        except:
            messagebox.showerror("Error", "Invalid path")
            
    def go_up(self):
        self.current_path = self.current_path.parent
        self.refresh_file_list()
        
    def on_double_click(self, event):
        selection = self.file_listbox.curselection()
        if selection:
            item_text = self.file_listbox.get(selection[0])
            item_name = item_text[2:]  # Remove icon
            
            if item_name == "..":
                self.go_up()
            else:
                item_path = self.current_path / item_name
                if item_path.is_dir():
                    self.current_path = item_path
                    self.refresh_file_list()
                elif item_path.is_file():
                    try:
                        os.startfile(str(item_path))  # Windows
                    except:
                        try:
                            subprocess.run(['open', str(item_path)])  # macOS
                        except:
                            subprocess.run(['xdg-open', str(item_path)])  # Linux
                            
    def create_folder(self):
        name = simpledialog.askstring("New Folder", "Enter folder name:")
        if name:
            try:
                (self.current_path / name).mkdir()
                self.refresh_file_list()
            except:
                messagebox.showerror("Error", "Could not create folder")
                
    def show_context_menu(self, event):
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
            
    def delete_item(self):
        selection = self.file_listbox.curselection()
        if selection:
            item_text = self.file_listbox.get(selection[0])
            item_name = item_text[2:]
            
            if item_name != ".." and messagebox.askyesno("Confirm", f"Delete {item_name}?"):
                try:
                    item_path = self.current_path / item_name
                    if item_path.is_file():
                        item_path.unlink()
                    else:
                        shutil.rmtree(item_path)
                    self.refresh_file_list()
                except:
                    messagebox.showerror("Error", "Could not delete item")
                    
    def rename_item(self):
        selection = self.file_listbox.curselection()
        if selection:
            item_text = self.file_listbox.get(selection[0])
            old_name = item_text[2:]
            
            if old_name != "..":
                new_name = simpledialog.askstring("Rename", "Enter new name:", initialvalue=old_name)
                if new_name and new_name != old_name:
                    try:
                        (self.current_path / old_name).rename(self.current_path / new_name)
                        self.refresh_file_list()
                    except:
                        messagebox.showerror("Error", "Could not rename item")

class SecureVaultApp(BaseApp):
    def __init__(self, parent):
        super().__init__(parent)
        self.vault_file = parent.data_dir / "vault.json"
        self.is_unlocked = False
        self.vault_data = {}
        
    def create_interface(self):
        title = self.create_title("🔒 Secure Vault")
        title.pack(pady=(0, 20))
        
        if not self.is_unlocked:
            self.show_login()
        else:
            self.show_vault()
            
    def show_login(self):
        login_frame = tk.Frame(self.frame, bg=self.parent.colors['bg_primary'])
        login_frame.pack(expand=True)
        
        tk.Label(
            login_frame,
            text="Enter Master Password",
            font=("Segoe UI", 14),
            bg=self.parent.colors['bg_primary'],
            fg=self.parent.colors['text_primary']
        ).pack(pady=20)
        
        self.password_var = tk.StringVar()
        password_entry = tk.Entry(
            login_frame,
            textvariable=self.password_var,
            show="*",
            bg=self.parent.colors['bg_secondary'],
            fg=self.parent.colors['text_primary'],
            font=("Segoe UI", 12),
            relief=tk.FLAT,
            width=30
        )
        password_entry.pack(pady=10)
        password_entry.bind('<Return>', lambda e: self.unlock_vault())
        
        button_frame = tk.Frame(login_frame, bg=self.parent.colors['bg_primary'])
        button_frame.pack(pady=20)
        
        self.create_button("Unlock", self.unlock_vault).pack(side=tk.LEFT, padx=10)
        self.create_button("Create Vault", self.create_vault).pack(side=tk.LEFT, padx=10)
        
    def show_vault(self):
        # Clear and recreate interface
        for widget in self.frame.winfo_children():
            if widget.winfo_class() != 'Label':  # Keep title
                widget.destroy()
                
        # Toolbar
        toolbar = tk.Frame(self.frame, bg=self.parent.colors['bg_primary'])
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        self.create_button("🔑 Add Password", lambda: self.add_entry('password')).pack(side=tk.LEFT, padx=(0, 10))
        self.create_button("📝 Add Note", lambda: self.add_entry('note')).pack(side=tk.LEFT, padx=(0, 10))
        self.create_button("✏️ Edit", self.edit_entry).pack(side=tk.LEFT, padx=(0, 10))
        self.create_button("🗑️ Delete", self.delete_entry).pack(side=tk.LEFT, padx=(0, 10))
        self.create_button("🔒 Lock", self.lock_vault).pack(side=tk.RIGHT)
        
        # Entries list
        self.entries_listbox = tk.Listbox(
            self.frame,
            bg=self.parent.colors['bg_secondary'],
            fg=self.parent.colors['text_primary'],
            selectbackground=self.parent.colors['accent'],
            font=("Segoe UI", 10),
            relief=tk.FLAT
        )
        self.entries_listbox.pack(fill=tk.BOTH, expand=True)
        
        self.refresh_entries()
        
    def unlock_vault(self):
        password = self.password_var.get()
        if not password:
            return
            
        try:
            if self.vault_file.exists():
                with open(self.vault_file, 'r') as f:
                    encrypted_data = json.load(f)
                    
                key = self.derive_key(password)
                fernet = Fernet(key)
                decrypted_data = fernet.decrypt(encrypted_data['data'].encode())
                self.vault_data = json.loads(decrypted_data.decode())
                
                self.is_unlocked = True
                self.show_vault()
            else:
                messagebox.showerror("Error", "Vault does not exist")
        except:
            messagebox.showerror("Error", "Invalid password")
            
    def create_vault(self):
        password = self.password_var.get()
        if not password:
            messagebox.showerror("Error", "Please enter a password")
            return
            
        self.vault_data = {}
        self.save_vault(password)
        self.is_unlocked = True
        self.show_vault()
        
    def save_vault(self, password):
        key = self.derive_key(password)
        fernet = Fernet(key)
        data = json.dumps(self.vault_data).encode()
        encrypted_data = fernet.encrypt(data)
        
        with open(self.vault_file, 'w') as f:
            json.dump({'data': encrypted_data.decode()}, f)
            
    def derive_key(self, password):
        return base64.urlsafe_b64encode(hashlib.pbkdf2_hmac('sha256', password.encode(), b'salt', 100000)[:32])
        
    def lock_vault(self):
        self.is_unlocked = False
        self.vault_data = {}
        self.create_interface()
        
    def refresh_entries(self):
        self.entries_listbox.delete(0, tk.END)
        for entry_id, entry in self.vault_data.items():
            entry_type = "🔑" if entry.get('type') == 'password' else "📝"
            self.entries_listbox.insert(tk.END, f"{entry_type} {entry['title']}")
            
    def add_entry(self, entry_type='password'):
        dialog = VaultEntryDialog(self.parent.root, self.parent.colors, entry_type=entry_type)
        result = dialog.result
        if result:
            entry_id = str(len(self.vault_data) + 1)
            result['type'] = entry_type
            self.vault_data[entry_id] = result
            self.save_vault(self.password_var.get())
            self.refresh_entries()
            
    def edit_entry(self):
        selection = self.entries_listbox.curselection()
        if selection:
            entry_id = str(selection[0] + 1)
            if entry_id in self.vault_data:
                dialog = VaultEntryDialog(self.parent.root, self.parent.colors, self.vault_data[entry_id])
                result = dialog.result
                if result:
                    self.vault_data[entry_id] = result
                    self.refresh_entries()
                    
    def delete_entry(self):
        selection = self.entries_listbox.curselection()
        if selection:
            if messagebox.askyesno("Confirm", "Delete this entry?"):
                entry_id = str(selection[0] + 1)
                if entry_id in self.vault_data:
                    del self.vault_data[entry_id]
                    self.refresh_entries()

class VaultEntryDialog:
    def __init__(self, parent, colors, entry_data=None, entry_type='password'):
        self.result = None
        self.entry_type = entry_type
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"Add {'Password' if entry_type == 'password' else 'Secure Note'}")
        self.dialog.geometry("450x350" if entry_type == 'password' else "450x250")
        self.dialog.configure(bg=colors['bg_primary'])
        self.dialog.grab_set()
        
        # Form fields based on type
        if entry_type == 'password':
            fields = [
                ("Title:", "title"),
                ("Website/Service:", "website"),
                ("Username:", "username"),
                ("Password:", "password"),
                ("Notes:", "notes")
            ]
        else:  # note type
            fields = [
                ("Title:", "title"),
                ("Content:", "content")
            ]
        
        self.vars = {}
        for i, (label, field) in enumerate(fields):
            tk.Label(
                self.dialog,
                text=label,
                bg=colors['bg_primary'],
                fg=colors['text_primary'],
                font=("Segoe UI", 10)
            ).grid(row=i, column=0, sticky=tk.W, padx=10, pady=5)
            
            if field in ["notes", "content"]:
                widget = tk.Text(
                    self.dialog,
                    bg=colors['bg_secondary'],
                    fg=colors['text_primary'],
                    font=("Segoe UI", 10),
                    height=6 if field == "content" else 4,
                    width=30
                )
                if entry_data and field in entry_data:
                    widget.insert(1.0, entry_data[field])
            else:
                self.vars[field] = tk.StringVar()
                if entry_data and field in entry_data:
                    self.vars[field].set(entry_data[field])
                    
                widget = tk.Entry(
                    self.dialog,
                    textvariable=self.vars[field],
                    bg=colors['bg_secondary'],
                    fg=colors['text_primary'],
                    font=("Segoe UI", 10),
                    show="*" if field == "password" else "",
                    width=30
                )
                
            widget.grid(row=i, column=1, padx=10, pady=5)
            
            if field in ["notes", "content"]:
                self.text_widget = widget
                
        # Buttons
        button_frame = tk.Frame(self.dialog, bg=colors['bg_primary'])
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=20)
        
        tk.Button(
            button_frame,
            text="💾 Save",
            command=self.save_entry,
            bg=colors['bg_tertiary'],
            fg=colors['text_primary'],
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            padx=20
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            button_frame,
            text="❌ Cancel",
            command=self.dialog.destroy,
            bg=colors['bg_tertiary'],
            fg=colors['text_primary'],
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            padx=20
        ).pack(side=tk.LEFT, padx=10)
        
        self.dialog.wait_window()
        
    def save_entry(self):
        self.result = {}
        for field, var in self.vars.items():
            self.result[field] = var.get()
        
        if hasattr(self, 'text_widget'):
            text_content = self.text_widget.get(1.0, tk.END).strip()
            if self.entry_type == 'password':
                self.result['notes'] = text_content
            else:
                self.result['content'] = text_content
                
        self.dialog.destroy()

class ExpenseTrackerApp(BaseApp):
    def __init__(self, parent):
        super().__init__(parent)
        self.expenses_file = parent.data_dir / "expenses.json"
        self.expenses = self.load_expenses()
        
    def create_interface(self):
        title = self.create_title("💰 Expense Tracker")
        title.pack(pady=(0, 20))
        
        # Add expense form
        form_frame = tk.LabelFrame(
            self.frame,
            text="Add Expense",
            bg=self.parent.colors['bg_secondary'],
            fg=self.parent.colors['text_primary'],
            font=("Segoe UI", 12, "bold")
        )
        form_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Form fields
        fields_frame = tk.Frame(form_frame, bg=self.parent.colors['bg_secondary'])
        fields_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Amount
        tk.Label(fields_frame, text="Amount:", bg=self.parent.colors['bg_secondary'], 
                fg=self.parent.colors['text_primary']).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.amount_var = tk.StringVar()
        tk.Entry(fields_frame, textvariable=self.amount_var, 
                bg=self.parent.colors['bg_tertiary'], fg=self.parent.colors['text_primary']).grid(row=0, column=1, padx=10, pady=5)
        
        # Category
        tk.Label(fields_frame, text="Category:", bg=self.parent.colors['bg_secondary'], 
                fg=self.parent.colors['text_primary']).grid(row=0, column=2, sticky=tk.W, pady=5)
        self.category_var = tk.StringVar()
        category_combo = ttk.Combobox(fields_frame, textvariable=self.category_var, 
                                    values=["Food", "Transport", "Shopping", "Bills", "Entertainment", "Other"])
        category_combo.grid(row=0, column=3, padx=10, pady=5)
        
        # Description
        tk.Label(fields_frame, text="Description:", bg=self.parent.colors['bg_secondary'], 
                fg=self.parent.colors['text_primary']).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.description_var = tk.StringVar()
        tk.Entry(fields_frame, textvariable=self.description_var, width=40,
                bg=self.parent.colors['bg_tertiary'], fg=self.parent.colors['text_primary']).grid(row=1, column=1, columnspan=3, padx=10, pady=5)
        
        # Add button
        self.create_button("Add Expense", self.add_expense).pack(pady=10)
        
        # Expenses list
        list_frame = tk.LabelFrame(
            self.frame,
            text="Recent Expenses",
            bg=self.parent.colors['bg_secondary'],
            fg=self.parent.colors['text_primary'],
            font=("Segoe UI", 12, "bold")
        )
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview for expenses
        columns = ("Date", "Amount", "Category", "Description")
        self.expenses_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.expenses_tree.heading(col, text=col)
            self.expenses_tree.column(col, width=150)
            
        self.expenses_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Summary
        summary_frame = tk.Frame(self.frame, bg=self.parent.colors['bg_primary'])
        summary_frame.pack(fill=tk.X, pady=10)
        
        self.summary_label = tk.Label(
            summary_frame,
            text="Total Expenses: $0.00",
            font=("Segoe UI", 14, "bold"),
            bg=self.parent.colors['bg_primary'],
            fg=self.parent.colors['accent']
        )
        self.summary_label.pack()
        
        self.refresh_expenses()
        
    def load_expenses(self):
        try:
            if self.expenses_file.exists():
                with open(self.expenses_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return []
        
    def save_expenses(self):
        with open(self.expenses_file, 'w') as f:
            json.dump(self.expenses, f, indent=2)
            
    def add_expense(self):
        try:
            amount = float(self.amount_var.get())
            category = self.category_var.get()
            description = self.description_var.get()
            
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be positive")
                return
                
            expense = {
                'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                'amount': amount,
                'category': category or "Other",
                'description': description
            }
            
            self.expenses.append(expense)
            self.save_expenses()
            self.refresh_expenses()
            
            # Clear form
            self.amount_var.set("")
            self.category_var.set("")
            self.description_var.set("")
            
        except ValueError:
            messagebox.showerror("Error", "Invalid amount")
            
    def refresh_expenses(self):
        # Clear treeview
        for item in self.expenses_tree.get_children():
            self.expenses_tree.delete(item)
            
        # Add recent expenses (last 50)
        total = 0
        for expense in self.expenses[-50:]:
            self.expenses_tree.insert("", 0, values=(
                expense['date'],
                f"${expense['amount']:.2f}",
                expense['category'],
                expense['description']
            ))
            total += expense['amount']
            
        # Update summary
        self.summary_label.config(text=f"Total Expenses: ${total:.2f}")

class ReminderApp(BaseApp):
    def __init__(self, parent):
        super().__init__(parent)
        self.reminders_file = parent.data_dir / "reminders.json"
        self.reminders = self.load_reminders()
        
    def create_interface(self):
        title = self.create_title("⏰ Reminders")
        title.pack(pady=(0, 20))
        
        # Add reminder form
        form_frame = tk.LabelFrame(
            self.frame,
            text="Add Reminder",
            bg=self.parent.colors['bg_secondary'],
            fg=self.parent.colors['text_primary'],
            font=("Segoe UI", 12, "bold")
        )
        form_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Form fields
        fields_frame = tk.Frame(form_frame, bg=self.parent.colors['bg_secondary'])
        fields_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Title
        tk.Label(fields_frame, text="Title:", bg=self.parent.colors['bg_secondary'], 
                fg=self.parent.colors['text_primary']).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.title_var = tk.StringVar()
        tk.Entry(fields_frame, textvariable=self.title_var, width=30,
                bg=self.parent.colors['bg_tertiary'], fg=self.parent.colors['text_primary']).grid(row=0, column=1, padx=10, pady=5)
        
        # Date
        tk.Label(fields_frame, text="Date (YYYY-MM-DD):", bg=self.parent.colors['bg_secondary'], 
                fg=self.parent.colors['text_primary']).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.date_var = tk.StringVar(value=datetime.date.today().strftime("%Y-%m-%d"))
        tk.Entry(fields_frame, textvariable=self.date_var, width=30,
                bg=self.parent.colors['bg_tertiary'], fg=self.parent.colors['text_primary']).grid(row=1, column=1, padx=10, pady=5)
        
        # Time
        tk.Label(fields_frame, text="Time (HH:MM):", bg=self.parent.colors['bg_secondary'], 
                fg=self.parent.colors['text_primary']).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.time_var = tk.StringVar(value="12:00")
        tk.Entry(fields_frame, textvariable=self.time_var, width=30,
                bg=self.parent.colors['bg_tertiary'], fg=self.parent.colors['text_primary']).grid(row=2, column=1, padx=10, pady=5)
        
        # Description
        tk.Label(fields_frame, text="Description:", bg=self.parent.colors['bg_secondary'], 
                fg=self.parent.colors['text_primary']).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.desc_var = tk.StringVar()
        tk.Entry(fields_frame, textvariable=self.desc_var, width=30,
                bg=self.parent.colors['bg_tertiary'], fg=self.parent.colors['text_primary']).grid(row=3, column=1, padx=10, pady=5)
        
        # Add button
        self.create_button("Add Reminder", self.add_reminder).pack(pady=10)
        
        # Reminders list
        list_frame = tk.LabelFrame(
            self.frame,
            text="Upcoming Reminders",
            bg=self.parent.colors['bg_secondary'],
            fg=self.parent.colors['text_primary'],
            font=("Segoe UI", 12, "bold")
        )
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview for reminders
        columns = ("Date", "Time", "Title", "Description")
        self.reminders_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.reminders_tree.heading(col, text=col)
            self.reminders_tree.column(col, width=150)
            
        self.reminders_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Buttons
        button_frame = tk.Frame(list_frame, bg=self.parent.colors['bg_secondary'])
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.create_button("Delete Selected", self.delete_reminder).pack(side=tk.LEFT, padx=10)
        self.create_button("Mark Complete", self.mark_complete).pack(side=tk.LEFT, padx=10)
        
        self.refresh_reminders()
        
    def load_reminders(self):
        try:
            if self.reminders_file.exists():
                with open(self.reminders_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return []
        
    def save_reminders(self):
        with open(self.reminders_file, 'w') as f:
            json.dump(self.reminders, f, indent=2)
            
    def add_reminder(self):
        try:
            title = self.title_var.get().strip()
            date_str = self.date_var.get().strip()
            time_str = self.time_var.get().strip()
            description = self.desc_var.get().strip()
            
            if not title:
                messagebox.showerror("Error", "Title is required")
                return
                
            # Validate date and time
            datetime.datetime.strptime(date_str, "%Y-%m-%d")
            datetime.datetime.strptime(time_str, "%H:%M")
            
            reminder = {
                'id': len(self.reminders) + 1,
                'title': title,
                'date': date_str,
                'time': time_str,
                'description': description,
                'completed': False,
                'created': datetime.datetime.now().isoformat()
            }
            
            self.reminders.append(reminder)
            self.save_reminders()
            self.refresh_reminders()
            
            # Clear form
            self.title_var.set("")
            self.desc_var.set("")
            
        except ValueError:
            messagebox.showerror("Error", "Invalid date or time format")
            
    def refresh_reminders(self):
        # Clear treeview
        for item in self.reminders_tree.get_children():
            self.reminders_tree.delete(item)
            
        # Add active reminders, sorted by date/time
        active_reminders = [r for r in self.reminders if not r.get('completed', False)]
        active_reminders.sort(key=lambda x: f"{x['date']} {x['time']}")
        
        for reminder in active_reminders:
            self.reminders_tree.insert("", tk.END, values=(
                reminder['date'],
                reminder['time'],
                reminder['title'],
                reminder['description']
            ))
            
    def delete_reminder(self):
        selection = self.reminders_tree.selection()
        if selection:
            item = self.reminders_tree.item(selection[0])
            title = item['values'][2]
            
            if messagebox.askyesno("Confirm", f"Delete reminder '{title}'?"):
                # Find and remove reminder
                for i, reminder in enumerate(self.reminders):
                    if reminder['title'] == title and not reminder.get('completed', False):
                        del self.reminders[i]
                        break
                        
                self.save_reminders()
                self.refresh_reminders()
                
    def mark_complete(self):
        selection = self.reminders_tree.selection()
        if selection:
            item = self.reminders_tree.item(selection[0])
            title = item['values'][2]
            
            # Find and mark complete
            for reminder in self.reminders:
                if reminder['title'] == title and not reminder.get('completed', False):
                    reminder['completed'] = True
                    break
                    
            self.save_reminders()
            self.refresh_reminders()

class ChatbotApp(BaseApp):
    def __init__(self, parent):
        super().__init__(parent)
        self.conversation = []
        
    def create_interface(self):
        title = self.create_title("🤖 Chatbot")
        title.pack(pady=(0, 20))
        
        # Chat display
        chat_frame = tk.Frame(self.frame, bg=self.parent.colors['bg_primary'])
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Scrollbar
        scrollbar = tk.Scrollbar(chat_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.chat_display = tk.Text(
            chat_frame,
            bg=self.parent.colors['bg_secondary'],
            fg=self.parent.colors['text_primary'],
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            wrap=tk.WORD,
            state=tk.DISABLED,
            yscrollcommand=scrollbar.set
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.chat_display.yview)
        
        # Input frame
        input_frame = tk.Frame(self.frame, bg=self.parent.colors['bg_primary'])
        input_frame.pack(fill=tk.X)
        
        self.message_var = tk.StringVar()
        message_entry = tk.Entry(
            input_frame,
            textvariable=self.message_var,
            bg=self.parent.colors['bg_secondary'],
            fg=self.parent.colors['text_primary'],
            font=("Segoe UI", 11),
            relief=tk.FLAT
        )
        message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        message_entry.bind('<Return>', lambda e: self.send_message())
        
        self.create_button("Send", self.send_message).pack(side=tk.RIGHT)
        
        # Welcome message
        self.add_message("Bot", "Hello! I'm your AI assistant. How can I help you today?")
        
    def add_message(self, sender, message):
        self.chat_display.config(state=tk.NORMAL)
        timestamp = datetime.datetime.now().strftime("%H:%M")
        
        if sender == "You":
            self.chat_display.insert(tk.END, f"[{timestamp}] You: {message}\n", "user")
        else:
            self.chat_display.insert(tk.END, f"[{timestamp}] Bot: {message}\n", "bot")
            
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        
    def send_message(self):
        message = self.message_var.get().strip()
        if not message:
            return
            
        self.add_message("You", message)
        self.message_var.set("")
        
        # Simple chatbot responses
        response = self.generate_response(message.lower())
        self.add_message("Bot", response)
        
    def generate_response(self, message):
        responses = {
            "hello": "Hello! How are you doing today?",
            "hi": "Hi there! What can I help you with?",
            "how are you": "I'm doing great, thank you for asking! How about you?",
            "what's your name": "I'm NeuraBot, your AI assistant built into NeuraDesk!",
            "time": f"The current time is {datetime.datetime.now().strftime('%H:%M:%S')}",
            "date": f"Today's date is {datetime.date.today().strftime('%B %d, %Y')}",
            "weather": "I don't have access to weather data, but you can check the Weather app!",
            "calculator": "Need to do some math? Try the Calculator app in the sidebar!",
            "notes": "Want to jot something down? The Notes app is perfect for that!",
            "help": "I can help with basic questions, provide information about NeuraDesk apps, and have casual conversations!",
            "bye": "Goodbye! Feel free to chat with me anytime!",
            "thank you": "You're welcome! Happy to help!",
            "thanks": "No problem! Anything else I can help with?"
        }
        
        # Check for exact matches
        for key, response in responses.items():
            if key in message:
                return response
                
        # Default responses
        default_responses = [
            "That's interesting! Tell me more.",
            "I see. What else would you like to know?",
            "Thanks for sharing! Is there anything specific I can help you with?",
            "I'm still learning, but I'm here to help! What else can I assist you with?",
            "That's a good point! What would you like to explore next?",
            "Interesting! Feel free to ask me about NeuraDesk's features or just chat!"
        ]
        
        import random
        return random.choice(default_responses)

class AIAssistantApp(BaseApp):
    def __init__(self, parent):
        super().__init__(parent)
        self.commands = []
        
    def create_interface(self):
        title = self.create_title("🧠 AI Assistant")
        title.pack(pady=(0, 20))
        
        # Command input
        input_frame = tk.LabelFrame(
            self.frame,
            text="Voice/Text Commands",
            bg=self.parent.colors['bg_secondary'],
            fg=self.parent.colors['text_primary'],
            font=("Segoe UI", 12, "bold")
        )
        input_frame.pack(fill=tk.X, pady=(0, 20))
        
        command_frame = tk.Frame(input_frame, bg=self.parent.colors['bg_secondary'])
        command_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.command_var = tk.StringVar()
        command_entry = tk.Entry(
            command_frame,
            textvariable=self.command_var,
            bg=self.parent.colors['bg_tertiary'],
            fg=self.parent.colors['text_primary'],
            font=("Segoe UI", 11),
            relief=tk.FLAT
        )
        command_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        command_entry.bind('<Return>', lambda e: self.process_command())
        
        self.create_button("Execute", self.process_command).pack(side=tk.RIGHT)
        
        # Command history
        history_frame = tk.LabelFrame(
            self.frame,
            text="Command History & Results",
            bg=self.parent.colors['bg_secondary'],
            fg=self.parent.colors['text_primary'],
            font=("Segoe UI", 12, "bold")
        )
        history_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(history_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_display = tk.Text(
            history_frame,
            bg=self.parent.colors['bg_secondary'],
            fg=self.parent.colors['text_primary'],
            font=("Consolas", 10),
            relief=tk.FLAT,
            wrap=tk.WORD,
            state=tk.DISABLED,
            yscrollcommand=scrollbar.set
        )
        self.history_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.config(command=self.history_display.yview)
        
        # Available commands info
        info_frame = tk.Frame(self.frame, bg=self.parent.colors['bg_primary'])
        info_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            info_frame,
            text="Available commands: time, date, calculate [expression], open [app/website], browse [url], system info, clear history, weather, joke, quote",
            font=("Segoe UI", 9),
            bg=self.parent.colors['bg_primary'],
            fg=self.parent.colors['text_secondary'],
            wraplength=800
        ).pack()
        
        # Welcome message
        self.add_to_history("AI Assistant initialized. Ready for commands!")
        
    def add_to_history(self, text):
        self.history_display.config(state=tk.NORMAL)
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.history_display.insert(tk.END, f"[{timestamp}] {text}\n")
        self.history_display.config(state=tk.DISABLED)
        self.history_display.see(tk.END)
        
    def process_command(self):
        command = self.command_var.get().strip().lower()
        if not command:
            return
            
        self.add_to_history(f"Command: {command}")
        self.command_var.set("")
        
        try:
            if command == "time":
                result = f"Current time: {datetime.datetime.now().strftime('%H:%M:%S')}"
                
            elif command == "date":
                result = f"Current date: {datetime.date.today().strftime('%B %d, %Y')}"
                
            elif command.startswith("calculate "):
                expression = command[10:].strip()
                # Safe calculation
                allowed_chars = set('0123456789+-*/.() ')
                if all(c in allowed_chars for c in expression):
                    try:
                        result = f"Result: {eval(expression)}"
                    except:
                        result = "Error: Invalid mathematical expression"
                else:
                    result = "Error: Invalid characters in expression"
                    
            elif command.startswith("open "):
                target = command[5:].strip()
                
                # Check if it's a website URL
                if any(target.startswith(prefix) for prefix in ['http://', 'https://', 'www.']):
                    self.open_website(target)
                    result = f"Opening website: {target}"
                
                # Check popular websites
                elif target in ['google', 'youtube', 'facebook', 'twitter', 'instagram', 'github', 'stackoverflow']:
                    website_urls = {
                        'google': 'https://www.google.com',
                        'youtube': 'https://www.youtube.com',
                        'facebook': 'https://www.facebook.com',
                        'twitter': 'https://www.twitter.com',
                        'instagram': 'https://www.instagram.com',
                        'github': 'https://www.github.com',
                        'stackoverflow': 'https://stackoverflow.com'
                    }
                    self.open_website(website_urls[target])
                    result = f"Opening {target.title()}"
                
                # Check for apps
                else:
                    app_mapping = {
                        "notes": "notes",
                        "calculator": "calculator",
                        "file explorer": "file_explorer",
                        "files": "file_explorer",
                        "vault": "secure_vault",
                        "expenses": "expense_tracker",
                        "reminders": "reminder",
                        "chatbot": "chatbot",
                        "passwords": "password_manager",
                        "locker": "folder_locker",
                        "tasks": "task_manager",
                        "weather": "weather"
                    }
                    
                    if target in app_mapping:
                        self.parent.show_app(app_mapping[target])
                        result = f"Opened {target} app"
                    else:
                        result = f"App or website '{target}' not recognized. Try 'open google' or 'open calculator'"
                    
            elif command == "system info":
                import platform
                result = f"System: {platform.system()} {platform.release()}\nPython: {platform.python_version()}\nArchitecture: {platform.architecture()[0]}"
                
            elif command == "clear history":
                self.history_display.config(state=tk.NORMAL)
                self.history_display.delete(1.0, tk.END)
                self.history_display.config(state=tk.DISABLED)
                result = "Command history cleared"
                
            elif "hello" in command or "hi" in command:
                result = "Hello! I'm your AI assistant. How can I help you today?"
                
            elif command.startswith("browse "):
                url = command[7:].strip()
                if not url.startswith(('http://', 'https://')):
                    url = 'https://' + url
                self.open_website(url)
                result = f"Opening browser for: {url}"
                
            elif command in ["weather", "get weather"]:
                result = "Weather: Sunny, 72°F (22°C)\nHumidity: 65%\nWind: 8 mph NW\nFor detailed weather, use the Weather app"
                
            elif command in ["joke", "tell joke", "funny"]:
                jokes = [
                    "Why don't scientists trust atoms? Because they make up everything!",
                    "Why did the computer go to the doctor? It had a virus!",
                    "How do you organize a space party? You planet!",
                    "Why don't programmers like nature? It has too many bugs!",
                    "What do you call a fake noodle? An impasta!"
                ]
                import random
                result = random.choice(jokes)
                
            elif command in ["quote", "inspire", "motivation"]:
                quotes = [
                    "The only way to do great work is to love what you do. - Steve Jobs",
                    "Innovation distinguishes between a leader and a follower. - Steve Jobs",
                    "Life is what happens to you while you're busy making other plans. - John Lennon",
                    "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
                    "It is during our darkest moments that we must focus to see the light. - Aristotle"
                ]
                import random
                result = random.choice(quotes)
                
            elif "search" in command:
                query = command.replace("search", "").strip()
                if query:
                    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                    self.open_website(search_url)
                    result = f"Searching Google for: {query}"
                else:
                    result = "Please specify what to search for"
                    
            elif "what is" in command or "define" in command:
                term = command.replace("what is", "").replace("define", "").strip()
                if term:
                    search_url = f"https://www.google.com/search?q=define+{term.replace(' ', '+')}"
                    self.open_website(search_url)
                    result = f"Looking up definition for: {term}"
                else:
                    result = "Please specify what to define"
                    
            elif "how to" in command:
                query = command.strip()
                search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                self.open_website(search_url)
                result = f"Searching for: {query}"
                
            elif "help" in command:
                result = """Available commands:
• time, date - Get current time/date
• calculate [expression] - Perform math calculations
• open [app/website] - Open apps or websites (google, youtube, etc.)
• browse [url] - Open any website
• search [query] - Search Google
• what is [term] - Look up definitions
• how to [query] - Search for tutorials
• weather - Quick weather info
• joke - Get a random joke
• quote - Get inspirational quote
• system info - Show system details
• clear history - Clear command history"""
                
            else:
                # Try to be more helpful with unrecognized commands
                if any(word in command for word in ['open', 'start', 'launch']):
                    result = "Try: 'open [app name]' or 'open [website]'. Examples: 'open calculator', 'open google'"
                elif any(word in command for word in ['find', 'search', 'look']):
                    result = "Try: 'search [query]' or 'what is [term]'. Example: 'search python programming'"
                else:
                    result = "Command not recognized. Type 'help' for available commands."
                
        except Exception as e:
            result = f"Error executing command: {str(e)}"
            
        self.add_to_history(f"Result: {result}")
    
    def open_website(self, url):
        """Open a website in the default browser"""
        import webbrowser
        try:
            webbrowser.open(url)
        except Exception as e:
            self.add_to_history(f"Error opening website: {str(e)}")

class PasswordManagerApp(BaseApp):
    def __init__(self, parent):
        super().__init__(parent)
        self.passwords_file = parent.data_dir / "passwords.json"
        self.master_password = None
        self.passwords = {}
        self.is_unlocked = False
        
    def create_interface(self):
        title = self.create_title("🔑 Password Manager")
        title.pack(pady=(0, 20))
        
        if not self.is_unlocked:
            self.show_login()
        else:
            self.show_manager()
            
    def show_login(self):
        login_frame = tk.Frame(self.frame, bg=self.parent.colors['bg_primary'])
        login_frame.pack(expand=True)
        
        tk.Label(
            login_frame,
            text="Enter Master Password",
            font=("Segoe UI", 14),
            bg=self.parent.colors['bg_primary'],
            fg=self.parent.colors['text_primary']
        ).pack(pady=20)
        
        self.master_password_var = tk.StringVar()
        password_entry = tk.Entry(
            login_frame,
            textvariable=self.master_password_var,
            show="*",
            bg=self.parent.colors['bg_secondary'],
            fg=self.parent.colors['text_primary'],
            font=("Segoe UI", 12),
            relief=tk.FLAT,
            width=30
        )
        password_entry.pack(pady=10)
        password_entry.bind('<Return>', lambda e: self.unlock_manager())
        
        button_frame = tk.Frame(login_frame, bg=self.parent.colors['bg_primary'])
        button_frame.pack(pady=20)
        
        self.create_button("Unlock", self.unlock_manager).pack(side=tk.LEFT, padx=10)
        self.create_button("Create New", self.create_manager).pack(side=tk.LEFT, padx=10)
        
    def show_manager(self):
        # Clear and recreate interface
        for widget in self.frame.winfo_children():
            if widget.winfo_class() != 'Label':  # Keep title
                widget.destroy()
                
        # Toolbar
        toolbar = tk.Frame(self.frame, bg=self.parent.colors['bg_primary'])
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        self.create_button("Add Password", self.add_password).pack(side=tk.LEFT, padx=(0, 10))
        self.create_button("Generate Password", self.generate_password).pack(side=tk.LEFT, padx=(0, 10))
        self.create_button("Export", self.export_passwords).pack(side=tk.LEFT, padx=(0, 10))
        self.create_button("Lock", self.lock_manager).pack(side=tk.RIGHT)
        
        # Search
        search_frame = tk.Frame(self.frame, bg=self.parent.colors['bg_primary'])
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(search_frame, text="Search:", bg=self.parent.colors['bg_primary'], 
                fg=self.parent.colors['text_primary']).pack(side=tk.LEFT)
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            bg=self.parent.colors['bg_secondary'],
            fg=self.parent.colors['text_primary'],
            font=("Segoe UI", 10),
            relief=tk.FLAT
        )
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        search_entry.bind('<KeyRelease>', lambda e: self.filter_passwords())
        
        # Passwords list
        columns = ("Website", "Username", "Password", "Notes")
        self.passwords_tree = ttk.Treeview(self.frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.passwords_tree.heading(col, text=col)
            if col == "Password":
                self.passwords_tree.column(col, width=100)
            else:
                self.passwords_tree.column(col, width=150)
                
        self.passwords_tree.pack(fill=tk.BOTH, expand=True)
        
        # Context menu
        self.context_menu = tk.Menu(self.frame, tearoff=0)
        self.context_menu.add_command(label="Copy Password", command=self.copy_password)
        self.context_menu.add_command(label="Copy Username", command=self.copy_username)
        self.context_menu.add_command(label="Edit", command=self.edit_password)
        self.context_menu.add_command(label="Delete", command=self.delete_password)
        
        self.passwords_tree.bind('<Button-3>', self.show_context_menu)
        
        self.refresh_passwords()
        
    def unlock_manager(self):
        password = self.master_password_var.get()
        if not password:
            return
            
        try:
            if self.passwords_file.exists():
                with open(self.passwords_file, 'r') as f:
                    encrypted_data = json.load(f)
                    
                key = self.derive_key(password)
                fernet = Fernet(key)
                decrypted_data = fernet.decrypt(encrypted_data['data'].encode())
                self.passwords = json.loads(decrypted_data.decode())
                
                self.master_password = password
                self.is_unlocked = True
                self.show_manager()
            else:
                messagebox.showerror("Error", "Password manager does not exist")
        except:
            messagebox.showerror("Error", "Invalid master password")
            
    def create_manager(self):
        password = self.master_password_var.get()
        if not password:
            messagebox.showerror("Error", "Please enter a master password")
            return
            
        if len(password) < 6:
            messagebox.showerror("Error", "Master password must be at least 6 characters")
            return
            
        self.passwords = {}
        self.master_password = password
        self.save_passwords()
        self.is_unlocked = True
        self.show_manager()
        
    def save_passwords(self):
        key = self.derive_key(self.master_password)
        fernet = Fernet(key)
        data = json.dumps(self.passwords).encode()
        encrypted_data = fernet.encrypt(data)
        
        with open(self.passwords_file, 'w') as f:
            json.dump({'data': encrypted_data.decode()}, f)
            
    def derive_key(self, password):
        return base64.urlsafe_b64encode(hashlib.pbkdf2_hmac('sha256', password.encode(), b'salt', 100000)[:32])
        
    def lock_manager(self):
        self.is_unlocked = False
        self.passwords = {}
        self.master_password = None
        self.create_interface()
        
    def refresh_passwords(self):
        # Clear treeview
        for item in self.passwords_tree.get_children():
            self.passwords_tree.delete(item)
            
        # Add passwords
        search_term = self.search_var.get().lower() if hasattr(self, 'search_var') else ""
        
        for entry_id, entry in self.passwords.items():
            if not search_term or search_term in entry['website'].lower() or search_term in entry['username'].lower():
                self.passwords_tree.insert("", tk.END, values=(
                    entry['website'],
                    entry['username'],
                    "*" * len(entry['password']),  # Hide password
                    entry.get('notes', '')
                ))
                
    def filter_passwords(self):
        self.refresh_passwords()
        
    def add_password(self):
        dialog = PasswordEntryDialog(self.parent.root, self.parent.colors)
        result = dialog.result
        if result:
            entry_id = str(len(self.passwords) + 1)
            self.passwords[entry_id] = result
            self.save_passwords()
            self.refresh_passwords()
            
    def generate_password(self):
        length = simpledialog.askinteger("Password Length", "Enter password length:", initialvalue=12, minvalue=4, maxvalue=50)
        if length:
            characters = string.ascii_letters + string.digits + "!@#$%^&*"
            password = ''.join(secrets.choice(characters) for _ in range(length))
            
            # Copy to clipboard (simplified)
            self.parent.root.clipboard_clear()
            self.parent.root.clipboard_append(password)
            
            messagebox.showinfo("Generated Password", f"Password generated and copied to clipboard:\n{password}")
            
    def copy_password(self):
        selection = self.passwords_tree.selection()
        if selection:
            item = self.passwords_tree.item(selection[0])
            website = item['values'][0]
            
            # Find the actual password
            for entry in self.passwords.values():
                if entry['website'] == website:
                    self.parent.root.clipboard_clear()
                    self.parent.root.clipboard_append(entry['password'])
                    messagebox.showinfo("Copied", "Password copied to clipboard")
                    break
                    
    def copy_username(self):
        selection = self.passwords_tree.selection()
        if selection:
            item = self.passwords_tree.item(selection[0])
            username = item['values'][1]
            
            self.parent.root.clipboard_clear()
            self.parent.root.clipboard_append(username)
            messagebox.showinfo("Copied", "Username copied to clipboard")
            
    def edit_password(self):
        selection = self.passwords_tree.selection()
        if selection:
            item = self.passwords_tree.item(selection[0])
            website = item['values'][0]
            
            # Find the entry
            for entry_id, entry in self.passwords.items():
                if entry['website'] == website:
                    dialog = PasswordEntryDialog(self.parent.root, self.parent.colors, entry)
                    result = dialog.result
                    if result:
                        self.passwords[entry_id] = result
                        self.save_passwords()
                        self.refresh_passwords()
                    break
                    
    def delete_password(self):
        selection = self.passwords_tree.selection()
        if selection:
            item = self.passwords_tree.item(selection[0])
            website = item['values'][0]
            
            if messagebox.askyesno("Confirm", f"Delete password for {website}?"):
                # Find and delete entry
                for entry_id, entry in list(self.passwords.items()):
                    if entry['website'] == website:
                        del self.passwords[entry_id]
                        break
                        
                self.save_passwords()
                self.refresh_passwords()
                
    def show_context_menu(self, event):
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
            
    def export_passwords(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write("NeuraDesk Password Manager Export\n")
                    f.write("=" * 40 + "\n\n")
                    
                    for entry in self.passwords.values():
                        f.write(f"Website: {entry['website']}\n")
                        f.write(f"Username: {entry['username']}\n")
                        f.write(f"Password: {entry['password']}\n")
                        f.write(f"Notes: {entry.get('notes', '')}\n")
                        f.write("-" * 40 + "\n")
                        
                messagebox.showinfo("Success", "Passwords exported successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")

class PasswordEntryDialog:
    def __init__(self, parent, colors, entry_data=None):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Password Entry")
        self.dialog.geometry("400x250")
        self.dialog.configure(bg=colors['bg_primary'])
        self.dialog.grab_set()
        
        # Form fields
        fields = [
            ("Website:", "website"),
            ("Username:", "username"),
            ("Password:", "password"),
            ("Notes:", "notes")
        ]
        
        self.vars = {}
        for i, (label, field) in enumerate(fields):
            tk.Label(
                self.dialog,
                text=label,
                bg=colors['bg_primary'],
                fg=colors['text_primary'],
                font=("Segoe UI", 10)
            ).grid(row=i, column=0, sticky=tk.W, padx=10, pady=5)
            
            self.vars[field] = tk.StringVar()
            if entry_data and field in entry_data:
                self.vars[field].set(entry_data[field])
                
            entry = tk.Entry(
                self.dialog,
                textvariable=self.vars[field],
                bg=colors['bg_secondary'],
                fg=colors['text_primary'],
                font=("Segoe UI", 10),
                show="*" if field == "password" else None,
                width=30
            )
            entry.grid(row=i, column=1, padx=10, pady=5)
            
        # Buttons
        button_frame = tk.Frame(self.dialog, bg=colors['bg_primary'])
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=20)
        
        tk.Button(
            button_frame,
            text="Save",
            command=self.save_entry,
            bg=colors['bg_tertiary'],
            fg=colors['text_primary'],
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            padx=20
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            button_frame,
            text="Cancel",
            command=self.dialog.destroy,
            bg=colors['bg_tertiary'],
            fg=colors['text_primary'],
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            padx=20
        ).pack(side=tk.LEFT, padx=10)
        
        self.dialog.wait_window()
        
    def save_entry(self):
        self.result = {}
        for field, var in self.vars.items():
            self.result[field] = var.get()
        self.dialog.destroy()

class FolderLockerApp(BaseApp):
    def __init__(self, parent):
        super().__init__(parent)
        self.locked_folders_file = parent.data_dir / "locked_folders.json"
        self.locked_folders = self.load_locked_folders()
        
    def create_interface(self):
        title = self.create_title("🗂️ Folder Locker")
        title.pack(pady=(0, 20))
        
        # Lock folder section
        lock_frame = tk.LabelFrame(
            self.frame,
            text="Lock Folder",
            bg=self.parent.colors['bg_secondary'],
            fg=self.parent.colors['text_primary'],
            font=("Segoe UI", 12, "bold")
        )
        lock_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Folder selection
        folder_frame = tk.Frame(lock_frame, bg=self.parent.colors['bg_secondary'])
        folder_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.folder_path_var = tk.StringVar()
        folder_entry = tk.Entry(
            folder_frame,
            textvariable=self.folder_path_var,
            bg=self.parent.colors['bg_tertiary'],
            fg=self.parent.colors['text_primary'],
            font=("Segoe UI", 10),
            relief=tk.FLAT
        )
        folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        self.create_button("Browse", self.browse_folder).pack(side=tk.RIGHT)
        
        # Password
        password_frame = tk.Frame(lock_frame, bg=self.parent.colors['bg_secondary'])
        password_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(password_frame, text="Password:", bg=self.parent.colors['bg_secondary'], 
                fg=self.parent.colors['text_primary']).pack(side=tk.LEFT)
        
        self.lock_password_var = tk.StringVar()
        tk.Entry(
            password_frame,
            textvariable=self.lock_password_var,
            show="*",
            bg=self.parent.colors['bg_tertiary'],
            fg=self.parent.colors['text_primary'],
            font=("Segoe UI", 10),
            relief=tk.FLAT
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        self.create_button("Lock Folder", self.lock_folder).pack(pady=10)
        
        # Locked folders list
        list_frame = tk.LabelFrame(
            self.frame,
            text="Locked Folders",
            bg=self.parent.colors['bg_secondary'],
            fg=self.parent.colors['text_primary'],
            font=("Segoe UI", 12, "bold")
        )
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Listbox for locked folders
        self.locked_listbox = tk.Listbox(
            list_frame,
            bg=self.parent.colors['bg_tertiary'],
            fg=self.parent.colors['text_primary'],
            selectbackground=self.parent.colors['accent'],
            font=("Consolas", 10),
            relief=tk.FLAT
        )
        self.locked_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Unlock controls
        unlock_frame = tk.Frame(list_frame, bg=self.parent.colors['bg_secondary'])
        unlock_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(unlock_frame, text="Password:", bg=self.parent.colors['bg_secondary'], 
                fg=self.parent.colors['text_primary']).pack(side=tk.LEFT)
        
        self.unlock_password_var = tk.StringVar()
        tk.Entry(
            unlock_frame,
            textvariable=self.unlock_password_var,
            show="*",
            bg=self.parent.colors['bg_tertiary'],
            fg=self.parent.colors['text_primary'],
            font=("Segoe UI", 10),
            relief=tk.FLAT
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        self.create_button("Unlock", self.unlock_folder).pack(side=tk.RIGHT, padx=10)
        
        self.refresh_locked_folders()
        
    def load_locked_folders(self):
        try:
            if self.locked_folders_file.exists():
                with open(self.locked_folders_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return {}
        
    def save_locked_folders(self):
        with open(self.locked_folders_file, 'w') as f:
            json.dump(self.locked_folders, f, indent=2)
            
    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path_var.set(folder)
            
    def lock_folder(self):
        folder_path = self.folder_path_var.get().strip()
        password = self.lock_password_var.get().strip()
        
        if not folder_path or not password:
            messagebox.showerror("Error", "Please select a folder and enter a password")
            return
            
        if not os.path.exists(folder_path):
            messagebox.showerror("Error", "Folder does not exist")
            return
            
        if folder_path in [f['path'] for f in self.locked_folders.values()]:
            messagebox.showerror("Error", "Folder is already locked")
            return
            
        try:
            # Create a simple lock by hiding the folder (Windows)
            if sys.platform == "win32":
                import subprocess
                subprocess.run(['attrib', '+H', folder_path], check=True)
                
            # Store locked folder info
            folder_id = str(len(self.locked_folders) + 1)
            self.locked_folders[folder_id] = {
                'path': folder_path,
                'password_hash': hashlib.sha256(password.encode()).hexdigest(),
                'locked_time': datetime.datetime.now().isoformat()
            }
            
            self.save_locked_folders()
            self.refresh_locked_folders()
            
            # Clear form
            self.folder_path_var.set("")
            self.lock_password_var.set("")
            
            messagebox.showinfo("Success", "Folder locked successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to lock folder: {str(e)}")
            
    def unlock_folder(self):
        selection = self.locked_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select a locked folder")
            return
            
        password = self.unlock_password_var.get().strip()
        if not password:
            messagebox.showerror("Error", "Please enter the password")
            return
            
        folder_id = str(selection[0] + 1)
        if folder_id not in self.locked_folders:
            return
            
        folder_info = self.locked_folders[folder_id]
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        if password_hash != folder_info['password_hash']:
            messagebox.showerror("Error", "Invalid password")
            return
            
        try:
            # Unhide the folder (Windows)
            if sys.platform == "win32":
                import subprocess
                subprocess.run(['attrib', '-H', folder_info['path']], check=True)
                
            # Remove from locked folders
            del self.locked_folders[folder_id]
            self.save_locked_folders()
            self.refresh_locked_folders()
            
            # Clear password
            self.unlock_password_var.set("")
            
            messagebox.showinfo("Success", "Folder unlocked successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to unlock folder: {str(e)}")
            
    def refresh_locked_folders(self):
        self.locked_listbox.delete(0, tk.END)
        for folder_info in self.locked_folders.values():
            folder_name = os.path.basename(folder_info['path'])
            self.locked_listbox.insert(tk.END, f"{folder_name} - {folder_info['path']}")

class TaskManagerApp(BaseApp):
    def __init__(self, parent):
        super().__init__(parent)
        self.tasks_file = parent.data_dir / "tasks.json"
        self.tasks = self.load_tasks()
        
    def create_interface(self):
        title = self.create_title("📋 Task Manager")
        title.pack(pady=(0, 20))
        
        # Add task form
        form_frame = tk.LabelFrame(
            self.frame,
            text="Add Task",
            bg=self.parent.colors['bg_secondary'],
            fg=self.parent.colors['text_primary'],
            font=("Segoe UI", 12, "bold")
        )
        form_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Task input
        input_frame = tk.Frame(form_frame, bg=self.parent.colors['bg_secondary'])
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.task_var = tk.StringVar()
        task_entry = tk.Entry(
            input_frame,
            textvariable=self.task_var,
            bg=self.parent.colors['bg_tertiary'],
            fg=self.parent.colors['text_primary'],
            font=("Segoe UI", 11),
            relief=tk.FLAT
        )
        task_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        task_entry.bind('<Return>', lambda e: self.add_task())
        
        # Priority
        self.priority_var = tk.StringVar(value="Medium")
        priority_combo = ttk.Combobox(
            input_frame,
            textvariable=self.priority_var,
            values=["Low", "Medium", "High", "Urgent"],
            width=10
        )
        priority_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        self.create_button("Add Task", self.add_task).pack(side=tk.RIGHT)
        
        # Tasks list
        list_frame = tk.LabelFrame(
            self.frame,
            text="Tasks",
            bg=self.parent.colors['bg_secondary'],
            fg=self.parent.colors['text_primary'],
            font=("Segoe UI", 12, "bold")
        )
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview for tasks
        columns = ("Status", "Priority", "Task", "Created")
        self.tasks_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=12)
        
        # Configure columns
        self.tasks_tree.heading("Status", text="✓")
        self.tasks_tree.column("Status", width=30)
        
        self.tasks_tree.heading("Priority", text="Priority")
        self.tasks_tree.column("Priority", width=80)
        
        self.tasks_tree.heading("Task", text="Task")
        self.tasks_tree.column("Task", width=300)
        
        self.tasks_tree.heading("Created", text="Created")
        self.tasks_tree.column("Created", width=120)
        
        self.tasks_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Task controls
        controls_frame = tk.Frame(list_frame, bg=self.parent.colors['bg_secondary'])
        controls_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.create_button("Complete Task", self.complete_task).pack(side=tk.LEFT, padx=(0, 10))
        self.create_button("Delete Task", self.delete_task).pack(side=tk.LEFT, padx=(0, 10))
        self.create_button("Clear Completed", self.clear_completed).pack(side=tk.LEFT, padx=(0, 10))
        
        # Statistics
        self.stats_label = tk.Label(
            controls_frame,
            text="",
            bg=self.parent.colors['bg_secondary'],
            fg=self.parent.colors['text_secondary'],
            font=("Segoe UI", 10)
        )
        self.stats_label.pack(side=tk.RIGHT)
        
        self.refresh_tasks()
        
    def load_tasks(self):
        try:
            if self.tasks_file.exists():
                with open(self.tasks_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return []
        
    def save_tasks(self):
        with open(self.tasks_file, 'w') as f:
            json.dump(self.tasks, f, indent=2)
            
    def add_task(self):
        task_text = self.task_var.get().strip()
        if not task_text:
            return
            
        task = {
            'id': len(self.tasks) + 1,
            'text': task_text,
            'priority': self.priority_var.get(),
            'completed': False,
            'created': datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        self.tasks.append(task)
        self.save_tasks()
        self.refresh_tasks()
        
        # Clear form
        self.task_var.set("")
        
    def complete_task(self):
        selection = self.tasks_tree.selection()
        if selection:
            item = self.tasks_tree.item(selection[0])
            task_text = item['values'][2]
            
            # Find and mark task as completed
            for task in self.tasks:
                if task['text'] == task_text and not task['completed']:
                    task['completed'] = True
                    break
                    
            self.save_tasks()
            self.refresh_tasks()
            
    def delete_task(self):
        selection = self.tasks_tree.selection()
        if selection:
            item = self.tasks_tree.item(selection[0])
            task_text = item['values'][2]
            
            if messagebox.askyesno("Confirm", "Delete this task?"):
                # Find and remove task
                self.tasks = [task for task in self.tasks if task['text'] != task_text]
                self.save_tasks()
                self.refresh_tasks()
                
    def clear_completed(self):
        if messagebox.askyesno("Confirm", "Clear all completed tasks?"):
            self.tasks = [task for task in self.tasks if not task['completed']]
            self.save_tasks()
            self.refresh_tasks()
            
    def refresh_tasks(self):
        # Clear treeview
        for item in self.tasks_tree.get_children():
            self.tasks_tree.delete(item)
            
        # Sort tasks by priority and completion status
        priority_order = {"Urgent": 0, "High": 1, "Medium": 2, "Low": 3}
        sorted_tasks = sorted(self.tasks, key=lambda x: (x['completed'], priority_order.get(x['priority'], 4)))
        
        # Add tasks to treeview
        for task in sorted_tasks:
            status = "✓" if task['completed'] else "○"
            priority_color = {
                "Urgent": "🔴",
                "High": "🟠", 
                "Medium": "🟡",
                "Low": "🟢"
            }.get(task['priority'], "⚪")
            
            self.tasks_tree.insert("", tk.END, values=(
                status,
                f"{priority_color} {task['priority']}",
                task['text'],
                task['created']
            ))
            
        # Update statistics
        total_tasks = len(self.tasks)
        completed_tasks = len([t for t in self.tasks if t['completed']])
        pending_tasks = total_tasks - completed_tasks
        
        self.stats_label.config(text=f"Total: {total_tasks} | Pending: {pending_tasks} | Completed: {completed_tasks}")

class WeatherApp(BaseApp):
    def __init__(self, parent):
        super().__init__(parent)
        
    def create_interface(self):
        title = self.create_title("🌤️ Weather")
        title.pack(pady=(0, 20))
        
        # Location input
        location_frame = tk.Frame(self.frame, bg=self.parent.colors['bg_primary'])
        location_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            location_frame,
            text="Location:",
            bg=self.parent.colors['bg_primary'],
            fg=self.parent.colors['text_primary'],
            font=("Segoe UI", 12)
        ).pack(side=tk.LEFT)
        
        self.location_var = tk.StringVar(value="New York")
        location_entry = tk.Entry(
            location_frame,
            textvariable=self.location_var,
            bg=self.parent.colors['bg_secondary'],
            fg=self.parent.colors['text_primary'],
            font=("Segoe UI", 11),
            relief=tk.FLAT,
            width=20
        )
        location_entry.pack(side=tk.LEFT, padx=10)
        location_entry.bind('<Return>', lambda e: self.get_weather())
        
        self.create_button("Get Weather", self.get_weather).pack(side=tk.LEFT, padx=10)
        
        # Weather display
        weather_frame = tk.LabelFrame(
            self.frame,
            text="Current Weather",
            bg=self.parent.colors['bg_secondary'],
            fg=self.parent.colors['text_primary'],
            font=("Segoe UI", 12, "bold")
        )
        weather_frame.pack(fill=tk.BOTH, expand=True)
        
        # Weather info display
        self.weather_display = tk.Text(
            weather_frame,
            bg=self.parent.colors['bg_secondary'],
            fg=self.parent.colors['text_primary'],
            font=("Segoe UI", 12),
            relief=tk.FLAT,
            wrap=tk.WORD,
            height=15,
            state=tk.DISABLED
        )
        self.weather_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Show default weather info
        self.show_default_weather()
        
    def show_default_weather(self):
        self.weather_display.config(state=tk.NORMAL)
        self.weather_display.delete(1.0, tk.END)
        
        weather_info = """
🌤️ Weather Information

Note: This is a demo weather app. In a real implementation, 
you would connect to a weather API service like:

• OpenWeatherMap API
• WeatherAPI
• AccuWeather API

Sample Weather Data for New York:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌡️ Temperature: 22°C (72°F)
🌤️ Condition: Partly Cloudy
💨 Wind: 15 km/h NW
💧 Humidity: 65%
👁️ Visibility: 10 km
🌅 Sunrise: 06:30 AM
🌇 Sunset: 07:45 PM

5-Day Forecast:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Today:     🌤️ 22°C   Partly Cloudy
Tomorrow:  ☀️ 25°C   Sunny
Wed:       🌧️ 18°C   Light Rain
Thu:       ⛅ 20°C   Cloudy
Fri:       ☀️ 24°C   Sunny

💡 To enable real weather data:
1. Sign up for a weather API service
2. Get your API key
3. Update the get_weather() method
4. Parse and display real weather data
        """
        
        self.weather_display.insert(1.0, weather_info)
        self.weather_display.config(state=tk.DISABLED)
        
    def get_weather(self):
        location = self.location_var.get().strip()
        if not location:
            return
            
        # In a real implementation, you would make an API call here
        self.weather_display.config(state=tk.NORMAL)
        self.weather_display.delete(1.0, tk.END)
        
        # Simulate different weather for different cities
        weather_data = {
            "new york": ("🌤️", "22°C", "Partly Cloudy", "15 km/h NW", "65%"),
            "london": ("🌧️", "15°C", "Rainy", "20 km/h SW", "85%"),
            "tokyo": ("☀️", "28°C", "Sunny", "10 km/h E", "55%"),
            "paris": ("⛅", "18°C", "Cloudy", "12 km/h W", "70%"),
            "sydney": ("☀️", "25°C", "Clear", "8 km/h SE", "45%"),
            "moscow": ("❄️", "-5°C", "Snow", "25 km/h N", "90%"),
            "dubai": ("☀️", "35°C", "Hot", "5 km/h S", "30%")
        }
        
        location_key = location.lower()
        if location_key in weather_data:
            icon, temp, condition, wind, humidity = weather_data[location_key]
        else:
            # Default weather for unknown locations
            icon, temp, condition, wind, humidity = ("🌤️", "20°C", "Partly Cloudy", "10 km/h", "60%")
            
        weather_info = f"""
🌤️ Weather for {location.title()}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{icon} Current Conditions:
🌡️ Temperature: {temp}
🌤️ Condition: {condition}
💨 Wind: {wind}
💧 Humidity: {humidity}
👁️ Visibility: 10 km

Last Updated: {datetime.datetime.now().strftime("%H:%M:%S")}

Note: This is simulated weather data for demonstration.
Connect to a real weather API for accurate information.

Popular Weather APIs:
• OpenWeatherMap (openweathermap.org)
• WeatherAPI (weatherapi.com)
• AccuWeather (developer.accuweather.com)
        """
        
        self.weather_display.insert(1.0, weather_info)
        self.weather_display.config(state=tk.DISABLED)

# Run the application
if __name__ == "__main__":
    import os
    import sys
    
    # Ensure display is available
    if not os.environ.get('DISPLAY'):
        os.environ['DISPLAY'] = ':0'
    
    try:
        print("Starting NeuraDesk...")
        app = NeuraDesk()
        print("NeuraDesk initialized successfully")
        app.run()
    except Exception as e:
        print(f"Error starting NeuraDesk: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
