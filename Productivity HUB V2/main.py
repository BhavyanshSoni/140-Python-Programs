import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import json
import os
from datetime import datetime, timedelta
import threading
import time
from PIL import Image, ImageTk
import sqlite3
import hashlib
import webbrowser
from tkcalendar import Calendar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class ProductivityHub:
    def __init__(self, root):
        self.root = root
        self.root.title("Productivity Hub V2 - Ultimate Daily Work Manager")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1a1a2e')
        
        # Initialize database
        self.init_database()
        
        # Load data
        self.load_data()
        
        # Create main interface
        self.create_interface()
        
        # Start auto-save timer
        self.start_auto_save()
        
    def init_database(self):
        """Initialize SQLite database for storing projects and tasks"""
        self.conn = sqlite3.connect('productivity_hub.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        
        # Create tables
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'active',
                priority TEXT DEFAULT 'medium',
                created_date TEXT,
                deadline TEXT,
                progress INTEGER DEFAULT 0
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'pending',
                priority TEXT DEFAULT 'medium',
                due_date TEXT,
                completed_date TEXT,
                FOREIGN KEY (project_id) REFERENCES projects (id)
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT,
                category TEXT,
                created_date TEXT,
                modified_date TEXT
            )
        ''')
        
        self.conn.commit()
        
    def load_data(self):
        """Load existing data from database"""
        self.projects = {}
        self.tasks = {}
        self.notes = {}
        
        # Load projects
        self.cursor.execute("SELECT * FROM projects")
        for row in self.cursor.fetchall():
            self.projects[row[0]] = {
                'name': row[1],
                'description': row[2],
                'status': row[3],
                'priority': row[4],
                'created_date': row[5],
                'deadline': row[6],
                'progress': row[7]
            }
            
        # Load tasks
        self.cursor.execute("SELECT * FROM tasks")
        for row in self.cursor.fetchall():
            self.tasks[row[0]] = {
                'project_id': row[1],
                'title': row[2],
                'description': row[3],
                'status': row[4],
                'priority': row[5],
                'due_date': row[6],
                'completed_date': row[7]
            }
            
        # Load notes
        self.cursor.execute("SELECT * FROM notes")
        for row in self.cursor.fetchall():
            self.notes[row[0]] = {
                'title': row[1],
                'content': row[2],
                'category': row[3],
                'created_date': row[4],
                'modified_date': row[5]
            }
        
    def create_interface(self):
        """Create the main interface with modern design"""
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Custom colors
        colors = {
            'bg_dark': '#1a1a2e',
            'bg_medium': '#16213e',
            'bg_light': '#0f3460',
            'accent': '#e94560',
            'text_light': '#ffffff',
            'text_gray': '#b8b8b8'
        }
        
        # Configure styles
        style.configure('Title.TLabel', 
                       background=colors['bg_dark'], 
                       foreground=colors['accent'],
                       font=('Segoe UI', 24, 'bold'))
        
        style.configure('Header.TLabel',
                       background=colors['bg_medium'],
                       foreground=colors['text_light'],
                       font=('Segoe UI', 12, 'bold'))
        
        style.configure('Card.TFrame',
                       background=colors['bg_medium'],
                       relief='flat',
                       borderwidth=2)
        
        # Main container
        main_frame = tk.Frame(self.root, bg=colors['bg_dark'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(main_frame, 
                               text="🚀 PRODUCTIVITY HUB V2", 
                               style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_projects_tab()
        self.create_tasks_tab()
        self.create_notes_tab()
        self.create_calendar_tab()
        self.create_analytics_tab()
        self.create_settings_tab()
        
    def create_dashboard_tab(self):
        """Create the main dashboard tab"""
        dashboard_frame = tk.Frame(self.notebook, bg='#1a1a2e')
        self.notebook.add(dashboard_frame, text="📊 Dashboard")
        
        # Top stats row
        stats_frame = tk.Frame(dashboard_frame, bg='#1a1a2e')
        stats_frame.pack(fill='x', padx=20, pady=20)
        
        # Stats cards
        stats_data = [
            ("📁 Total Projects", len(self.projects), "#e94560"),
            ("✅ Completed Tasks", len([t for t in self.tasks.values() if t['status'] == 'completed']), "#4CAF50"),
            ("⏰ Pending Tasks", len([t for t in self.tasks.values() if t['status'] == 'pending']), "#FF9800"),
            ("📝 Notes", len(self.notes), "#2196F3")
        ]
        
        for i, (title, count, color) in enumerate(stats_data):
            card = tk.Frame(stats_frame, bg='#16213e', relief='flat', bd=2)
            card.grid(row=0, column=i, padx=10, pady=10, sticky='ew')
            stats_frame.columnconfigure(i, weight=1)
            
            tk.Label(card, text=title, bg='#16213e', fg='#ffffff', 
                    font=('Segoe UI', 10)).pack(pady=(10, 5))
            tk.Label(card, text=str(count), bg='#16213e', fg=color, 
                    font=('Segoe UI', 24, 'bold')).pack(pady=(0, 10))
        
        # Quick actions
        actions_frame = tk.Frame(dashboard_frame, bg='#1a1a2e')
        actions_frame.pack(fill='x', padx=20, pady=20)
        
        tk.Label(actions_frame, text="Quick Actions", bg='#1a1a2e', fg='#ffffff',
                font=('Segoe UI', 16, 'bold')).pack(anchor='w', pady=(0, 10))
        
        actions_buttons = [
            ("➕ New Project", self.add_new_project),
            ("📋 New Task", self.add_new_task),
            ("📝 New Note", self.add_new_note),
            ("📅 View Calendar", lambda: self.notebook.select(4))
        ]
        
        for text, command in actions_buttons:
            btn = tk.Button(actions_frame, text=text, command=command,
                           bg='#0f3460', fg='#ffffff', font=('Segoe UI', 10),
                           relief='flat', padx=20, pady=10)
            btn.pack(side='left', padx=(0, 10))
        
        # Recent activity
        activity_frame = tk.Frame(dashboard_frame, bg='#1a1a2e')
        activity_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(activity_frame, text="Recent Activity", bg='#1a1a2e', fg='#ffffff',
                font=('Segoe UI', 16, 'bold')).pack(anchor='w', pady=(0, 10))
        
        # Activity list
        activity_list = tk.Frame(activity_frame, bg='#16213e')
        activity_list.pack(fill='both', expand=True)
        
        # Sample activities (in real app, this would be loaded from database)
        activities = [
            "📁 Created new project: Website Redesign",
            "✅ Completed task: Design mockups",
            "📝 Added note: Meeting notes from client call",
            "⏰ Task due soon: Frontend development"
        ]
        
        for activity in activities:
            tk.Label(activity_list, text=activity, bg='#16213e', fg='#b8b8b8',
                    font=('Segoe UI', 10), anchor='w').pack(fill='x', padx=10, pady=5)

    def create_projects_tab(self):
        """Create the projects management tab"""
        projects_frame = tk.Frame(self.notebook, bg='#1a1a2e')
        self.notebook.add(projects_frame, text="📁 Projects")

        # Header
        tk.Label(projects_frame, text="Your Projects", bg='#1a1a2e', fg='#e94560',
                 font=('Segoe UI', 18, 'bold')).pack(anchor='w', padx=20, pady=(20, 10))

        # Projects list
        self.projects_tree = ttk.Treeview(projects_frame, columns=('Name', 'Status', 'Priority', 'Deadline', 'Progress'), show='headings', height=15)
        self.projects_tree.pack(fill='both', expand=True, padx=20, pady=10)
        for col in self.projects_tree['columns']:
            self.projects_tree.heading(col, text=col)
            self.projects_tree.column(col, anchor='center')
        self.refresh_projects_tree()

        # Buttons
        btn_frame = tk.Frame(projects_frame, bg='#1a1a2e')
        btn_frame.pack(fill='x', padx=20, pady=10)
        tk.Button(btn_frame, text="Add Project", command=self.add_new_project, bg='#0f3460', fg='#fff', font=('Segoe UI', 10), relief='flat').pack(side='left', padx=5)
        tk.Button(btn_frame, text="Edit Project", command=self.edit_selected_project, bg='#0f3460', fg='#fff', font=('Segoe UI', 10), relief='flat').pack(side='left', padx=5)
        tk.Button(btn_frame, text="Delete Project", command=self.delete_selected_project, bg='#e94560', fg='#fff', font=('Segoe UI', 10), relief='flat').pack(side='left', padx=5)

    def refresh_projects_tree(self):
        for i in self.projects_tree.get_children():
            self.projects_tree.delete(i)
        for pid, proj in self.projects.items():
            self.projects_tree.insert('', 'end', iid=pid, values=(
                proj['name'], proj['status'], proj['priority'], proj['deadline'], f"{proj['progress']}%"
            ))

    def add_new_project(self):
        self.project_editor_window()

    def edit_selected_project(self):
        selected = self.projects_tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select a project to edit.")
            return
        pid = int(selected[0])
        self.project_editor_window(pid)

    def delete_selected_project(self):
        selected = self.projects_tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select a project to delete.")
            return
        pid = int(selected[0])
        if messagebox.askyesno("Delete Project", "Are you sure you want to delete this project?"):
            self.cursor.execute("DELETE FROM projects WHERE id=?", (pid,))
            self.conn.commit()
            self.load_data()
            self.refresh_projects_tree()

    def project_editor_window(self, pid=None):
        win = tk.Toplevel(self.root)
        win.title("Project Editor")
        win.geometry("400x400")
        win.configure(bg='#1a1a2e')

        # Fields
        tk.Label(win, text="Project Name:", bg='#1a1a2e', fg='#fff').pack(anchor='w', padx=20, pady=(20, 0))
        name_var = tk.StringVar()
        tk.Entry(win, textvariable=name_var, font=('Segoe UI', 12)).pack(fill='x', padx=20, pady=5)

        tk.Label(win, text="Description:", bg='#1a1a2e', fg='#fff').pack(anchor='w', padx=20, pady=(10, 0))
        desc_text = tk.Text(win, height=4, font=('Segoe UI', 12))
        desc_text.pack(fill='x', padx=20, pady=5)

        tk.Label(win, text="Priority:", bg='#1a1a2e', fg='#fff').pack(anchor='w', padx=20, pady=(10, 0))
        priority_var = tk.StringVar(value='medium')
        ttk.Combobox(win, textvariable=priority_var, values=['low', 'medium', 'high'], state='readonly').pack(fill='x', padx=20, pady=5)

        tk.Label(win, text="Deadline (YYYY-MM-DD):", bg='#1a1a2e', fg='#fff').pack(anchor='w', padx=20, pady=(10, 0))
        deadline_var = tk.StringVar()
        tk.Entry(win, textvariable=deadline_var, font=('Segoe UI', 12)).pack(fill='x', padx=20, pady=5)

        tk.Label(win, text="Progress (%):", bg='#1a1a2e', fg='#fff').pack(anchor='w', padx=20, pady=(10, 0))
        progress_var = tk.IntVar(value=0)
        tk.Scale(win, from_=0, to=100, orient='horizontal', variable=progress_var, bg='#1a1a2e', fg='#fff').pack(fill='x', padx=20, pady=5)

        # If editing, populate fields
        if pid:
            proj = self.projects[pid]
            name_var.set(proj['name'])
            desc_text.insert('1.0', proj['description'])
            priority_var.set(proj['priority'])
            deadline_var.set(proj['deadline'])
            progress_var.set(proj['progress'])

        def save_project():
            name = name_var.get().strip()
            desc = desc_text.get('1.0', 'end').strip()
            priority = priority_var.get()
            deadline = deadline_var.get()
            progress = progress_var.get()
            if not name:
                messagebox.showerror("Error", "Project name is required.")
                return
            if pid:
                self.cursor.execute('''UPDATE projects SET name=?, description=?, priority=?, deadline=?, progress=? WHERE id=?''',
                                   (name, desc, priority, deadline, progress, pid))
            else:
                self.cursor.execute('''INSERT INTO projects (name, description, priority, created_date, deadline, progress) VALUES (?, ?, ?, ?, ?, ?)''',
                                   (name, desc, priority, datetime.now().strftime('%Y-%m-%d'), deadline, progress))
            self.conn.commit()
            self.load_data()
            self.refresh_projects_tree()
            win.destroy()

        tk.Button(win, text="Save", command=save_project, bg='#4CAF50', fg='#fff', font=('Segoe UI', 12), relief='flat').pack(pady=20)

    # --- Tasks Tab ---
    def create_tasks_tab(self):
        tasks_frame = tk.Frame(self.notebook, bg='#1a1a2e')
        self.notebook.add(tasks_frame, text="📋 Tasks")

        tk.Label(tasks_frame, text="Your Tasks", bg='#1a1a2e', fg='#e94560',
                 font=('Segoe UI', 18, 'bold')).pack(anchor='w', padx=20, pady=(20, 10))

        self.tasks_tree = ttk.Treeview(tasks_frame, columns=('Title', 'Project', 'Status', 'Priority', 'Due Date'), show='headings', height=15)
        self.tasks_tree.pack(fill='both', expand=True, padx=20, pady=10)
        for col in self.tasks_tree['columns']:
            self.tasks_tree.heading(col, text=col)
            self.tasks_tree.column(col, anchor='center')
        self.refresh_tasks_tree()

        btn_frame = tk.Frame(tasks_frame, bg='#1a1a2e')
        btn_frame.pack(fill='x', padx=20, pady=10)
        tk.Button(btn_frame, text="Add Task", command=self.add_new_task, bg='#0f3460', fg='#fff', font=('Segoe UI', 10), relief='flat').pack(side='left', padx=5)
        tk.Button(btn_frame, text="Edit Task", command=self.edit_selected_task, bg='#0f3460', fg='#fff', font=('Segoe UI', 10), relief='flat').pack(side='left', padx=5)
        tk.Button(btn_frame, text="Delete Task", command=self.delete_selected_task, bg='#e94560', fg='#fff', font=('Segoe UI', 10), relief='flat').pack(side='left', padx=5)
        tk.Button(btn_frame, text="Mark Complete", command=self.mark_task_complete, bg='#4CAF50', fg='#fff', font=('Segoe UI', 10), relief='flat').pack(side='left', padx=5)

    def refresh_tasks_tree(self):
        for i in self.tasks_tree.get_children():
            self.tasks_tree.delete(i)
        for tid, task in self.tasks.items():
            project_name = self.projects.get(task['project_id'], {}).get('name', 'No Project')
            self.tasks_tree.insert('', 'end', iid=tid, values=(
                task['title'], project_name, task['status'], task['priority'], task['due_date']
            ))

    def add_new_task(self):
        self.task_editor_window()

    def edit_selected_task(self):
        selected = self.tasks_tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select a task to edit.")
            return
        tid = int(selected[0])
        self.task_editor_window(tid)

    def delete_selected_task(self):
        selected = self.tasks_tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select a task to delete.")
            return
        tid = int(selected[0])
        if messagebox.askyesno("Delete Task", "Are you sure you want to delete this task?"):
            self.cursor.execute("DELETE FROM tasks WHERE id=?", (tid,))
            self.conn.commit()
            self.load_data()
            self.refresh_tasks_tree()

    def mark_task_complete(self):
        selected = self.tasks_tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select a task to mark as complete.")
            return
        tid = int(selected[0])
        self.cursor.execute("UPDATE tasks SET status='completed', completed_date=? WHERE id=?", (datetime.now().strftime('%Y-%m-%d'), tid))
        self.conn.commit()
        self.load_data()
        self.refresh_tasks_tree()

    def task_editor_window(self, tid=None):
        win = tk.Toplevel(self.root)
        win.title("Task Editor")
        win.geometry("400x500")
        win.configure(bg='#1a1a2e')

        tk.Label(win, text="Task Title:", bg='#1a1a2e', fg='#fff').pack(anchor='w', padx=20, pady=(20, 0))
        title_var = tk.StringVar()
        tk.Entry(win, textvariable=title_var, font=('Segoe UI', 12)).pack(fill='x', padx=20, pady=5)

        tk.Label(win, text="Description:", bg='#1a1a2e', fg='#fff').pack(anchor='w', padx=20, pady=(10, 0))
        desc_text = tk.Text(win, height=4, font=('Segoe UI', 12))
        desc_text.pack(fill='x', padx=20, pady=5)

        tk.Label(win, text="Project:", bg='#1a1a2e', fg='#fff').pack(anchor='w', padx=20, pady=(10, 0))
        project_var = tk.StringVar()
        project_names = [self.projects[pid]['name'] for pid in self.projects]
        project_ids = list(self.projects.keys())
        project_combo = ttk.Combobox(win, textvariable=project_var, values=project_names, state='readonly')
        project_combo.pack(fill='x', padx=20, pady=5)

        tk.Label(win, text="Priority:", bg='#1a1a2e', fg='#fff').pack(anchor='w', padx=20, pady=(10, 0))
        priority_var = tk.StringVar(value='medium')
        ttk.Combobox(win, textvariable=priority_var, values=['low', 'medium', 'high'], state='readonly').pack(fill='x', padx=20, pady=5)

        tk.Label(win, text="Due Date (YYYY-MM-DD):", bg='#1a1a2e', fg='#fff').pack(anchor='w', padx=20, pady=(10, 0))
        due_var = tk.StringVar()
        tk.Entry(win, textvariable=due_var, font=('Segoe UI', 12)).pack(fill='x', padx=20, pady=5)

        # If editing, populate fields
        if tid:
            task = self.tasks[tid]
            title_var.set(task['title'])
            desc_text.insert('1.0', task['description'])
            if task['project_id'] in self.projects:
                project_var.set(self.projects[task['project_id']]['name'])
            priority_var.set(task['priority'])
            due_var.set(task['due_date'])

        def save_task():
            title = title_var.get().strip()
            desc = desc_text.get('1.0', 'end').strip()
            priority = priority_var.get()
            due = due_var.get()
            project_name = project_var.get()
            project_id = None
            for pid, proj in self.projects.items():
                if proj['name'] == project_name:
                    project_id = pid
                    break
            if not title:
                messagebox.showerror("Error", "Task title is required.")
                return
            if tid:
                self.cursor.execute('''UPDATE tasks SET title=?, description=?, project_id=?, priority=?, due_date=? WHERE id=?''',
                                   (title, desc, project_id, priority, due, tid))
            else:
                self.cursor.execute('''INSERT INTO tasks (title, description, project_id, priority, due_date) VALUES (?, ?, ?, ?, ?)''',
                                   (title, desc, project_id, priority, due))
            self.conn.commit()
            self.load_data()
            self.refresh_tasks_tree()
            win.destroy()

        tk.Button(win, text="Save", command=save_task, bg='#4CAF50', fg='#fff', font=('Segoe UI', 12), relief='flat').pack(pady=20)

    # --- Notes Tab ---
    def create_notes_tab(self):
        notes_frame = tk.Frame(self.notebook, bg='#1a1a2e')
        self.notebook.add(notes_frame, text="📝 Notes")

        tk.Label(notes_frame, text="Your Notes", bg='#1a1a2e', fg='#e94560',
                 font=('Segoe UI', 18, 'bold')).pack(anchor='w', padx=20, pady=(20, 10))

        self.notes_tree = ttk.Treeview(notes_frame, columns=('Title', 'Category', 'Created', 'Modified'), show='headings', height=15)
        self.notes_tree.pack(fill='both', expand=True, padx=20, pady=10)
        for col in self.notes_tree['columns']:
            self.notes_tree.heading(col, text=col)
            self.notes_tree.column(col, anchor='center')
        self.refresh_notes_tree()

        btn_frame = tk.Frame(notes_frame, bg='#1a1a2e')
        btn_frame.pack(fill='x', padx=20, pady=10)
        tk.Button(btn_frame, text="Add Note", command=self.add_new_note, bg='#0f3460', fg='#fff', font=('Segoe UI', 10), relief='flat').pack(side='left', padx=5)
        tk.Button(btn_frame, text="Edit Note", command=self.edit_selected_note, bg='#0f3460', fg='#fff', font=('Segoe UI', 10), relief='flat').pack(side='left', padx=5)
        tk.Button(btn_frame, text="Delete Note", command=self.delete_selected_note, bg='#e94560', fg='#fff', font=('Segoe UI', 10), relief='flat').pack(side='left', padx=5)
        tk.Button(btn_frame, text="View Note", command=self.view_selected_note, bg='#2196F3', fg='#fff', font=('Segoe UI', 10), relief='flat').pack(side='left', padx=5)

    def refresh_notes_tree(self):
        for i in self.notes_tree.get_children():
            self.notes_tree.delete(i)
        for nid, note in self.notes.items():
            self.notes_tree.insert('', 'end', iid=nid, values=(
                note['title'], note['category'], note['created_date'], note['modified_date']
            ))

    def add_new_note(self):
        self.note_editor_window()

    def edit_selected_note(self):
        selected = self.notes_tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select a note to edit.")
            return
        nid = int(selected[0])
        self.note_editor_window(nid)

    def delete_selected_note(self):
        selected = self.notes_tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select a note to delete.")
            return
        nid = int(selected[0])
        if messagebox.askyesno("Delete Note", "Are you sure you want to delete this note?"):
            self.cursor.execute("DELETE FROM notes WHERE id=?", (nid,))
            self.conn.commit()
            self.load_data()
            self.refresh_notes_tree()

    def view_selected_note(self):
        selected = self.notes_tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select a note to view.")
            return
        nid = int(selected[0])
        note = self.notes[nid]
        win = tk.Toplevel(self.root)
        win.title(note['title'])
        win.geometry("500x400")
        win.configure(bg='#1a1a2e')
        tk.Label(win, text=note['title'], bg='#1a1a2e', fg='#e94560', font=('Segoe UI', 16, 'bold')).pack(pady=10)
        scrolled = scrolledtext.ScrolledText(win, font=('Segoe UI', 12), wrap='word')
        scrolled.pack(fill='both', expand=True, padx=20, pady=10)
        scrolled.insert('1.0', note['content'])
        scrolled.config(state='disabled')

    def note_editor_window(self, nid=None):
        win = tk.Toplevel(self.root)
        win.title("Note Editor")
        win.geometry("400x400")
        win.configure(bg='#1a1a2e')

        tk.Label(win, text="Title:", bg='#1a1a2e', fg='#fff').pack(anchor='w', padx=20, pady=(20, 0))
        title_var = tk.StringVar()
        tk.Entry(win, textvariable=title_var, font=('Segoe UI', 12)).pack(fill='x', padx=20, pady=5)

        tk.Label(win, text="Category:", bg='#1a1a2e', fg='#fff').pack(anchor='w', padx=20, pady=(10, 0))
        category_var = tk.StringVar()
        tk.Entry(win, textvariable=category_var, font=('Segoe UI', 12)).pack(fill='x', padx=20, pady=5)

        tk.Label(win, text="Content:", bg='#1a1a2e', fg='#fff').pack(anchor='w', padx=20, pady=(10, 0))
        content_text = tk.Text(win, height=8, font=('Segoe UI', 12))
        content_text.pack(fill='x', padx=20, pady=5)

        # If editing, populate fields
        if nid:
            note = self.notes[nid]
            title_var.set(note['title'])
            category_var.set(note['category'])
            content_text.insert('1.0', note['content'])

        def save_note():
            title = title_var.get().strip()
            category = category_var.get().strip()
            content = content_text.get('1.0', 'end').strip()
            now = datetime.now().strftime('%Y-%m-%d')
            if not title:
                messagebox.showerror("Error", "Note title is required.")
                return
            if nid:
                self.cursor.execute('''UPDATE notes SET title=?, category=?, content=?, modified_date=? WHERE id=?''',
                                   (title, category, content, now, nid))
            else:
                self.cursor.execute('''INSERT INTO notes (title, category, content, created_date, modified_date) VALUES (?, ?, ?, ?, ?)''',
                                   (title, category, content, now, now))
            self.conn.commit()
            self.load_data()
            self.refresh_notes_tree()
            win.destroy()

        tk.Button(win, text="Save", command=save_note, bg='#4CAF50', fg='#fff', font=('Segoe UI', 12), relief='flat').pack(pady=20)

    # --- Calendar Tab ---
    def create_calendar_tab(self):
        calendar_frame = tk.Frame(self.notebook, bg='#1a1a2e')
        self.notebook.add(calendar_frame, text="📅 Calendar")

        tk.Label(calendar_frame, text="Calendar", bg='#1a1a2e', fg='#e94560',
                 font=('Segoe UI', 18, 'bold')).pack(anchor='w', padx=20, pady=(20, 10))

        self.cal = Calendar(calendar_frame, selectmode='day', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
        self.cal.pack(padx=20, pady=20)

        tk.Button(calendar_frame, text="Show Tasks for Date", command=self.show_tasks_for_date, bg='#0f3460', fg='#fff', font=('Segoe UI', 10), relief='flat').pack(pady=10)

    def show_tasks_for_date(self):
        date = self.cal.get_date()
        tasks = [t for t in self.tasks.values() if t['due_date'] == date]
        msg = "\n".join([f"{t['title']} ({t['priority']})" for t in tasks]) if tasks else "No tasks for this date."
        messagebox.showinfo("Tasks for " + date, msg)

    # --- Analytics Tab ---
    def create_analytics_tab(self):
        analytics_frame = tk.Frame(self.notebook, bg='#1a1a2e')
        self.notebook.add(analytics_frame, text="📈 Analytics")

        tk.Label(analytics_frame, text="Productivity Analytics", bg='#1a1a2e', fg='#e94560',
                 font=('Segoe UI', 18, 'bold')).pack(anchor='w', padx=20, pady=(20, 10))

        statuses = ['completed', 'pending']
        counts = [len([t for t in self.tasks.values() if t['status'] == s]) for s in statuses]
        if sum(counts) == 0:
            tk.Label(analytics_frame, text="No tasks to display analytics.", bg='#1a1a2e', fg='#b8b8b8', font=('Segoe UI', 14)).pack(pady=40)
        else:
            fig, ax = plt.subplots(figsize=(4, 4), dpi=100)
            ax.pie(counts, labels=statuses, autopct='%1.1f%%', colors=['#4CAF50', '#FF9800'])
            ax.set_title("Task Status Distribution")
            canvas = FigureCanvasTkAgg(fig, master=analytics_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(padx=20, pady=20)

    # --- Settings Tab ---
    def create_settings_tab(self):
        settings_frame = tk.Frame(self.notebook, bg='#1a1a2e')
        self.notebook.add(settings_frame, text="⚙️ Settings")

        tk.Label(settings_frame, text="Settings", bg='#1a1a2e', fg='#e94560',
                 font=('Segoe UI', 18, 'bold')).pack(anchor='w', padx=20, pady=(20, 10))

        # Example: Export data
        tk.Button(settings_frame, text="Export Data (JSON)", command=self.export_data, bg='#0f3460', fg='#fff', font=('Segoe UI', 10), relief='flat').pack(pady=10)
        tk.Button(settings_frame, text="Import Data (JSON)", command=self.import_data, bg='#0f3460', fg='#fff', font=('Segoe UI', 10), relief='flat').pack(pady=10)

    def export_data(self):
        data = {
            'projects': self.projects,
            'tasks': self.tasks,
            'notes': self.notes
        }
        file = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file:
            with open(file, 'w') as f:
                json.dump(data, f, indent=4)
            messagebox.showinfo("Export", "Data exported successfully.")

    def import_data(self):
        file = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file:
            with open(file, 'r') as f:
                data = json.load(f)
            # Import projects
            for proj in data.get('projects', {}).values():
                self.cursor.execute('''INSERT INTO projects (name, description, status, priority, created_date, deadline, progress) VALUES (?, ?, ?, ?, ?, ?, ?)''',
                                   (proj['name'], proj['description'], proj['status'], proj['priority'], proj['created_date'], proj['deadline'], proj['progress']))
            # Import tasks
            for task in data.get('tasks', {}).values():
                self.cursor.execute('''INSERT INTO tasks (project_id, title, description, status, priority, due_date, completed_date) VALUES (?, ?, ?, ?, ?, ?, ?)''',
                                   (task['project_id'], task['title'], task['description'], task['status'], task['priority'], task['due_date'], task['completed_date']))
            # Import notes
            for note in data.get('notes', {}).values():
                self.cursor.execute('''INSERT INTO notes (title, content, category, created_date, modified_date) VALUES (?, ?, ?, ?, ?)''',
                                   (note['title'], note['content'], note['category'], note['created_date'], note['modified_date']))
            self.conn.commit()
            self.load_data()
            self.refresh_projects_tree()
            self.refresh_tasks_tree()
            self.refresh_notes_tree()
            messagebox.showinfo("Import", "Data imported successfully.")

    # --- Auto-save and Exit ---
    def start_auto_save(self):
        def auto_save():
            while True:
                time.sleep(60)
                self.conn.commit()
        t = threading.Thread(target=auto_save, daemon=True)
        t.start()

    def on_exit(self):
        self.conn.commit()
        self.conn.close()
        self.root.destroy()

# --- Main ---
if __name__ == "__main__":
    root = tk.Tk()
    app = ProductivityHub(root)
    root.protocol("WM_DELETE_WINDOW", app.on_exit)
    root.mainloop()