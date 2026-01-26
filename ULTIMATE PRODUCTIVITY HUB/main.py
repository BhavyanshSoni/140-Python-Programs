#!/usr/bin/env python3
"""
ProductivityHub - A comprehensive daily utility application
Combines task management, notes, expenses, habits, weather, and quick tools
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime, timedelta
import requests
import random
import string
import math
import threading
import time
import colorama
colorama.init()

class DataManager:
    """Handles data persistence for the application"""
    
    def __init__(self):
        self.data_file = "productivity_data.json"
        self.data = self.load_data()
    
    def load_data(self):
        """Load data from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        
        return {
            "tasks": [],
            "notes": [],
            "expenses": [],
            "habits": [],
            "habit_entries": [],
            "settings": {
                "weather_location": "New York,US"
            }
        }
    
    def save_data(self):
        """Save data to JSON file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.data, f, indent=2, default=str)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {e}")
    
    def get_next_id(self, category):
        """Get next available ID for a category"""
        if not self.data[category]:
            return 1
        return max(item.get('id', 0) for item in self.data[category]) + 1

class TaskManager:
    """Manages task-related operations"""
    
    def __init__(self, data_manager):
        self.data_manager = data_manager
    
    def add_task(self, title, completed=False):
        """Add a new task"""
        task = {
            "id": self.data_manager.get_next_id("tasks"),
            "title": title,
            "completed": completed,
            "created_at": datetime.now().isoformat()
        }
        self.data_manager.data["tasks"].append(task)
        self.data_manager.save_data()
        return task
    
    def update_task(self, task_id, **updates):
        """Update an existing task"""
        for task in self.data_manager.data["tasks"]:
            if task["id"] == task_id:
                task.update(updates)
                self.data_manager.save_data()
                return task
        return None
    
    def delete_task(self, task_id):
        """Delete a task"""
        self.data_manager.data["tasks"] = [
            task for task in self.data_manager.data["tasks"] 
            if task["id"] != task_id
        ]
        self.data_manager.save_data()
    
    def get_tasks(self):
        """Get all tasks sorted by creation date"""
        return sorted(
            self.data_manager.data["tasks"], 
            key=lambda x: x.get("created_at", ""), 
            reverse=True
        )

class NotesManager:
    """Manages note-related operations"""
    
    def __init__(self, data_manager):
        self.data_manager = data_manager
    
    def add_note(self, title, content, color="yellow"):
        """Add a new note"""
        note = {
            "id": self.data_manager.get_next_id("notes"),
            "title": title,
            "content": content,
            "color": color,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        self.data_manager.data["notes"].append(note)
        self.data_manager.save_data()
        return note
    
    def update_note(self, note_id, **updates):
        """Update an existing note"""
        for note in self.data_manager.data["notes"]:
            if note["id"] == note_id:
                note.update(updates)
                note["updated_at"] = datetime.now().isoformat()
                self.data_manager.save_data()
                return note
        return None
    
    def delete_note(self, note_id):
        """Delete a note"""
        self.data_manager.data["notes"] = [
            note for note in self.data_manager.data["notes"] 
            if note["id"] != note_id
        ]
        self.data_manager.save_data()
    
    def get_notes(self):
        """Get all notes sorted by update date"""
        return sorted(
            self.data_manager.data["notes"], 
            key=lambda x: x.get("updated_at", ""), 
            reverse=True
        )

class ExpenseManager:
    """Manages expense-related operations"""
    
    def __init__(self, data_manager):
        self.data_manager = data_manager
    
    def add_expense(self, description, amount, category, date=None):
        """Add a new expense"""
        expense = {
            "id": self.data_manager.get_next_id("expenses"),
            "description": description,
            "amount": float(amount),
            "category": category,
            "date": (date or datetime.now()).isoformat()
        }
        self.data_manager.data["expenses"].append(expense)
        self.data_manager.save_data()
        return expense
    
    def update_expense(self, expense_id, **updates):
        """Update an existing expense"""
        for expense in self.data_manager.data["expenses"]:
            if expense["id"] == expense_id:
                expense.update(updates)
                self.data_manager.save_data()
                return expense
        return None
    
    def delete_expense(self, expense_id):
        """Delete an expense"""
        self.data_manager.data["expenses"] = [
            expense for expense in self.data_manager.data["expenses"] 
            if expense["id"] != expense_id
        ]
        self.data_manager.save_data()
    
    def get_expenses(self):
        """Get all expenses sorted by date"""
        return sorted(
            self.data_manager.data["expenses"], 
            key=lambda x: x.get("date", ""), 
            reverse=True
        )
    
    def get_stats(self):
        """Calculate expense statistics"""
        expenses = self.get_expenses()
        now = datetime.now()
        
        # This week
        start_of_week = now - timedelta(days=now.weekday())
        start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
        
        # This month
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        weekly_total = sum(
            expense["amount"] for expense in expenses
            if datetime.fromisoformat(expense["date"]) >= start_of_week
        )
        
        monthly_total = sum(
            expense["amount"] for expense in expenses
            if datetime.fromisoformat(expense["date"]) >= start_of_month
        )
        
        days_in_month = (now.replace(month=now.month % 12 + 1, day=1) - timedelta(days=1)).day
        daily_average = monthly_total / days_in_month if days_in_month > 0 else 0
        
        return {
            "weekly_total": weekly_total,
            "monthly_total": monthly_total,
            "daily_average": daily_average
        }

class HabitManager:
    """Manages habit-related operations"""
    
    def __init__(self, data_manager):
        self.data_manager = data_manager
    
    def add_habit(self, name, icon="💪", color="blue"):
        """Add a new habit"""
        habit = {
            "id": self.data_manager.get_next_id("habits"),
            "name": name,
            "icon": icon,
            "color": color,
            "streak": 0,
            "last_completed": None,
            "created_at": datetime.now().isoformat()
        }
        self.data_manager.data["habits"].append(habit)
        self.data_manager.save_data()
        return habit
    
    def update_habit(self, habit_id, **updates):
        """Update an existing habit"""
        for habit in self.data_manager.data["habits"]:
            if habit["id"] == habit_id:
                habit.update(updates)
                self.data_manager.save_data()
                return habit
        return None
    
    def delete_habit(self, habit_id):
        """Delete a habit and its entries"""
        self.data_manager.data["habits"] = [
            habit for habit in self.data_manager.data["habits"] 
            if habit["id"] != habit_id
        ]
        self.data_manager.data["habit_entries"] = [
            entry for entry in self.data_manager.data["habit_entries"]
            if entry["habit_id"] != habit_id
        ]
        self.data_manager.save_data()
    
    def toggle_habit_completion(self, habit_id):
        """Toggle habit completion for today"""
        today = datetime.now().date().isoformat()
        existing_entry = None
        
        for entry in self.data_manager.data["habit_entries"]:
            if (entry["habit_id"] == habit_id and 
                datetime.fromisoformat(entry["date"]).date().isoformat() == today):
                existing_entry = entry
                break
        
        habit = next((h for h in self.data_manager.data["habits"] if h["id"] == habit_id), None)
        if not habit:
            return
        
        if existing_entry:
            # Remove entry and decrease streak
            self.data_manager.data["habit_entries"].remove(existing_entry)
            habit["streak"] = max(0, habit["streak"] - 1)
            habit["last_completed"] = None
        else:
            # Add entry and increase streak
            entry = {
                "id": self.data_manager.get_next_id("habit_entries"),
                "habit_id": habit_id,
                "date": datetime.now().isoformat()
            }
            self.data_manager.data["habit_entries"].append(entry)
            habit["streak"] += 1
            habit["last_completed"] = datetime.now().isoformat()
        
        self.data_manager.save_data()
    
    def get_habits(self):
        """Get all habits sorted by creation date"""
        return sorted(
            self.data_manager.data["habits"], 
            key=lambda x: x.get("created_at", "")
        )
    
    def is_completed_today(self, habit_id):
        """Check if habit is completed today"""
        today = datetime.now().date().isoformat()
        return any(
            entry["habit_id"] == habit_id and 
            datetime.fromisoformat(entry["date"]).date().isoformat() == today
            for entry in self.data_manager.data["habit_entries"]
        )

class WeatherWidget:
    """Handles weather information"""
    
    def __init__(self):
        self.api_key = "demo_key"  # Replace with actual API key
        self.cache = {}
        self.cache_timeout = 600  # 10 minutes
    
    def get_weather(self, location="Inida"):
        """Get weather information for a location"""
        cache_key = f"{location}_{int(time.time() // self.cache_timeout)}"
        
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        try:
            # Mock weather data for demo
            weather_conditions = ["Clear", "Clouds", "Rain", "Snow", "Mist"]
            weather_data = {
                "location": location.split(",")[0],
                "temperature": random.randint(45, 85),
                "condition": random.choice(weather_conditions),
                "humidity": random.randint(30, 90),
                "wind_speed": random.randint(0, 25)
            }
            
            self.cache[cache_key] = weather_data
            return weather_data
        except Exception:
            return {
                "location": "Unknown",
                "temperature": 72,
                "condition": "Clear",
                "humidity": 50,
                "wind_speed": 5
            }

class CalculatorWidget:
    """Simple calculator widget"""
    
    def __init__(self, parent):
        self.parent = parent
        self.result_var = tk.StringVar(value="0")
        self.current_input = ""
        self.operator = None
        self.previous_value = None
        
    def create_calculator_window(self):
        """Create calculator popup window"""
        calc_window = tk.Toplevel(self.parent)
        calc_window.title("Calculator")
        calc_window.geometry("300x400")
        calc_window.resizable(False, False)
        
        # Display
        display = tk.Entry(calc_window, textvariable=self.result_var, 
                          font=("Arial", 18), justify="right", state="readonly")
        display.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="ew")
        
        # Button layout
        buttons = [
            ('C', 1, 0), ('±', 1, 1), ('%', 1, 2), ('÷', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('×', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('−', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3),
            ('0', 5, 0, 2), ('.', 5, 2), ('=', 5, 3)
        ]
        
        for button_data in buttons:
            text = button_data[0]
            row = button_data[1]
            col = button_data[2]
            colspan = button_data[3] if len(button_data) > 3 else 1
            
            btn = tk.Button(calc_window, text=text, font=("Arial", 14),
                           command=lambda t=text: self.button_click(t))
            btn.grid(row=row, column=col, columnspan=colspan, padx=2, pady=2, 
                    sticky="nsew", ipadx=10, ipady=10)
        
        # Configure grid weights
        for i in range(6):
            calc_window.grid_rowconfigure(i, weight=1)
        for i in range(4):
            calc_window.grid_columnconfigure(i, weight=1)
    
    def button_click(self, value):
        """Handle calculator button clicks"""
        if value.isdigit() or value == '.':
            if self.current_input == "0" and value != '.':
                self.current_input = value
            else:
                self.current_input += value
            self.result_var.set(self.current_input)
        
        elif value == 'C':
            self.current_input = ""
            self.operator = None
            self.previous_value = None
            self.result_var.set("0")
        
        elif value in ['+', '−', '×', '÷']:
            if self.current_input:
                if self.previous_value is not None and self.operator:
                    self.calculate()
                self.previous_value = float(self.current_input)
                self.operator = value
                self.current_input = ""
        
        elif value == '=':
            self.calculate()
        
        elif value == '±':
            if self.current_input and self.current_input != "0":
                if self.current_input.startswith('-'):
                    self.current_input = self.current_input[1:]
                else:
                    self.current_input = '-' + self.current_input
                self.result_var.set(self.current_input)
    
    def calculate(self):
        """Perform calculation"""
        if self.previous_value is not None and self.operator and self.current_input:
            try:
                current = float(self.current_input)
                if self.operator == '+':
                    result = self.previous_value + current
                elif self.operator == '−':
                    result = self.previous_value - current
                elif self.operator == '×':
                    result = self.previous_value * current
                elif self.operator == '÷':
                    result = self.previous_value / current if current != 0 else 0
                
                self.result_var.set(str(result))
                self.current_input = str(result)
                self.previous_value = None
                self.operator = None
            except (ValueError, ZeroDivisionError):
                self.result_var.set("Error")
                self.current_input = ""

class PasswordGenerator:
    """Password generation utility"""
    
    @staticmethod
    def generate_password(length=12, include_uppercase=True, include_lowercase=True, 
                         include_numbers=True, include_symbols=True):
        """Generate a secure password"""
        charset = ""
        if include_lowercase:
            charset += string.ascii_lowercase
        if include_uppercase:
            charset += string.ascii_uppercase
        if include_numbers:
            charset += string.digits
        if include_symbols:
            charset += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        if not charset:
            return ""
        
        return ''.join(random.choice(charset) for _ in range(length))
    
    @staticmethod
    def create_password_window(parent):
        """Create password generator window"""
        pwd_window = tk.Toplevel(parent)
        pwd_window.title("Password Generator")
        pwd_window.geometry("400x300")
        
        frame = ttk.Frame(pwd_window, padding="10")
        frame.grid(row=0, column=0, sticky="nsew")
        
        # Generated password display
        ttk.Label(frame, text="Generated Password:").grid(row=0, column=0, sticky="w", pady=5)
        password_var = tk.StringVar()
        password_entry = ttk.Entry(frame, textvariable=password_var, width=40, state="readonly")
        password_entry.grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)
        
        # Length setting
        ttk.Label(frame, text="Length:").grid(row=2, column=0, sticky="w", pady=5)
        length_var = tk.IntVar(value=12)
        length_scale = ttk.Scale(frame, from_=4, to=64, variable=length_var, orient="horizontal")
        length_scale.grid(row=2, column=1, sticky="ew", pady=5)
        
        # Character options
        uppercase_var = tk.BooleanVar(value=True)
        lowercase_var = tk.BooleanVar(value=True)
        numbers_var = tk.BooleanVar(value=True)
        symbols_var = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(frame, text="Include Uppercase", variable=uppercase_var).grid(row=3, column=0, sticky="w", pady=2)
        ttk.Checkbutton(frame, text="Include Lowercase", variable=lowercase_var).grid(row=4, column=0, sticky="w", pady=2)
        ttk.Checkbutton(frame, text="Include Numbers", variable=numbers_var).grid(row=5, column=0, sticky="w", pady=2)
        ttk.Checkbutton(frame, text="Include Symbols", variable=symbols_var).grid(row=6, column=0, sticky="w", pady=2)
        
        def generate():
            password = PasswordGenerator.generate_password(
                length=int(length_var.get()),
                include_uppercase=uppercase_var.get(),
                include_lowercase=lowercase_var.get(),
                include_numbers=numbers_var.get(),
                include_symbols=symbols_var.get()
            )
            password_var.set(password)
        
        def copy_password():
            pwd_window.clipboard_clear()
            pwd_window.clipboard_append(password_var.get())
            messagebox.showinfo("Copied", "Password copied to clipboard!")
        
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Generate", command=generate).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Copy", command=copy_password).pack(side="left", padx=5)
        
        # Generate initial password
        generate()

class UnitConverter:
    """Unit conversion utility"""
    
    @staticmethod
    def convert_length(value, from_unit, to_unit):
        """Convert length units"""
        # Convert to meters first
        to_meters = {
            'mm': 0.001, 'cm': 0.01, 'm': 1, 'km': 1000,
            'in': 0.0254, 'ft': 0.3048, 'yd': 0.9144, 'mi': 1609.34
        }
        
        if from_unit not in to_meters or to_unit not in to_meters:
            raise ValueError("Unsupported unit")
        
        meters = value * to_meters[from_unit]
        return meters / to_meters[to_unit]
    
    @staticmethod
    def convert_weight(value, from_unit, to_unit):
        """Convert weight units"""
        # Convert to grams first
        to_grams = {
            'g': 1, 'kg': 1000, 'lb': 453.592, 'oz': 28.3495
        }
        
        if from_unit not in to_grams or to_unit not in to_grams:
            raise ValueError("Unsupported unit")
        
        grams = value * to_grams[from_unit]
        return grams / to_grams[to_unit]
    
    @staticmethod
    def convert_temperature(value, from_unit, to_unit):
        """Convert temperature units"""
        if from_unit == to_unit:
            return value
        
        # Convert to Celsius first
        if from_unit == 'fahrenheit':
            celsius = (value - 32) * 5/9
        elif from_unit == 'kelvin':
            celsius = value - 273.15
        else:
            celsius = value
        
        # Convert from Celsius to target
        if to_unit == 'fahrenheit':
            return celsius * 9/5 + 32
        elif to_unit == 'kelvin':
            return celsius + 273.15
        else:
            return celsius
    
    @staticmethod
    def create_converter_window(parent):
        """Create unit converter window"""
        conv_window = tk.Toplevel(parent)
        conv_window.title("Unit Converter")
        conv_window.geometry("500x400")
        
        notebook = ttk.Notebook(conv_window)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Length conversion
        length_frame = ttk.Frame(notebook)
        notebook.add(length_frame, text="Length")
        UnitConverter._create_conversion_tab(length_frame, "length")
        
        # Weight conversion
        weight_frame = ttk.Frame(notebook)
        notebook.add(weight_frame, text="Weight")
        UnitConverter._create_conversion_tab(weight_frame, "weight")
        
        # Temperature conversion
        temp_frame = ttk.Frame(notebook)
        notebook.add(temp_frame, text="Temperature")
        UnitConverter._create_conversion_tab(temp_frame, "temperature")
    
    @staticmethod
    def _create_conversion_tab(parent, conversion_type):
        """Create a conversion tab"""
        frame = ttk.Frame(parent, padding="10")
        frame.pack(fill="both", expand=True)
        
        units = {
            "length": ["mm", "cm", "m", "km", "in", "ft", "yd", "mi"],
            "weight": ["g", "kg", "lb", "oz"],
            "temperature": ["celsius", "fahrenheit", "kelvin"]
        }
        
        # Input value
        ttk.Label(frame, text="Value:").grid(row=0, column=0, sticky="w", pady=5)
        value_var = tk.StringVar()
        ttk.Entry(frame, textvariable=value_var, width=20).grid(row=0, column=1, pady=5)
        
        # From unit
        ttk.Label(frame, text="From:").grid(row=1, column=0, sticky="w", pady=5)
        from_var = tk.StringVar()
        from_combo = ttk.Combobox(frame, textvariable=from_var, values=units[conversion_type], state="readonly")
        from_combo.grid(row=1, column=1, pady=5)
        
        # To unit
        ttk.Label(frame, text="To:").grid(row=2, column=0, sticky="w", pady=5)
        to_var = tk.StringVar()
        to_combo = ttk.Combobox(frame, textvariable=to_var, values=units[conversion_type], state="readonly")
        to_combo.grid(row=2, column=1, pady=5)
        
        # Result
        ttk.Label(frame, text="Result:").grid(row=3, column=0, sticky="w", pady=5)
        result_var = tk.StringVar()
        ttk.Entry(frame, textvariable=result_var, width=20, state="readonly").grid(row=3, column=1, pady=5)
        
        def convert():
            try:
                value = float(value_var.get())
                from_unit = from_var.get()
                to_unit = to_var.get()
                
                if not from_unit or not to_unit:
                    messagebox.showerror("Error", "Please select both units")
                    return
                
                if conversion_type == "length":
                    result = UnitConverter.convert_length(value, from_unit, to_unit)
                elif conversion_type == "weight":
                    result = UnitConverter.convert_weight(value, from_unit, to_unit)
                elif conversion_type == "temperature":
                    result = UnitConverter.convert_temperature(value, from_unit, to_unit)
                
                result_var.set(f"{result:.6f}".rstrip('0').rstrip('.'))
            except ValueError as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(frame, text="Convert", command=convert).grid(row=4, column=0, columnspan=2, pady=10)

class TimerWidget:
    """Timer/stopwatch utility"""
    
    @staticmethod
    def create_timer_window(parent):
        """Create timer window"""
        timer_window = tk.Toplevel(parent)
        timer_window.title("Timer")
        timer_window.geometry("300x400")
        
        frame = ttk.Frame(timer_window, padding="20")
        frame.pack(fill="both", expand=True)
        
        # Time display
        time_var = tk.StringVar(value="00:00")
        time_label = ttk.Label(frame, textvariable=time_var, font=("Arial", 24, "bold"))
        time_label.pack(pady=20)
        
        # Input frame
        input_frame = ttk.Frame(frame)
        input_frame.pack(pady=10)
        
        ttk.Label(input_frame, text="Minutes:").grid(row=0, column=0, padx=5)
        minutes_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=minutes_var, width=10).grid(row=0, column=1, padx=5)
        
        ttk.Label(input_frame, text="Seconds:").grid(row=0, column=2, padx=5)
        seconds_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=seconds_var, width=10).grid(row=0, column=3, padx=5)
        
        # Control variables
        timer_running = tk.BooleanVar(value=False)
        time_left = tk.IntVar(value=0)
        
        def format_time(total_seconds):
            mins = total_seconds // 60
            secs = total_seconds % 60
            return f"{mins:02d}:{secs:02d}"
        
        def update_timer():
            if timer_running.get() and time_left.get() > 0:
                time_left.set(time_left.get() - 1)
                time_var.set(format_time(time_left.get()))
                if time_left.get() == 0:
                    timer_running.set(False)
                    messagebox.showinfo("Timer", "Time's up!")
                else:
                    timer_window.after(1000, update_timer)
        
        def start_timer():
            try:
                mins = int(minutes_var.get() or "0")
                secs = int(seconds_var.get() or "0")
                total = mins * 60 + secs
                
                if total <= 0:
                    messagebox.showerror("Error", "Please enter a valid time")
                    return
                
                time_left.set(total)
                timer_running.set(True)
                time_var.set(format_time(total))
                update_timer()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers")
        
        def stop_timer():
            timer_running.set(False)
        
        def reset_timer():
            timer_running.set(False)
            time_left.set(0)
            time_var.set("00:00")
            minutes_var.set("")
            seconds_var.set("")
        
        # Control buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Start", command=start_timer).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Stop", command=stop_timer).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Reset", command=reset_timer).pack(side="left", padx=5)

class ProductivityHub:
    """Main application class"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ProductivityHub - Daily Utility App")
        self.root.geometry("1200x800")
        
        # Initialize managers
        self.data_manager = DataManager()
        self.task_manager = TaskManager(self.data_manager)
        self.notes_manager = NotesManager(self.data_manager)
        self.expense_manager = ExpenseManager(self.data_manager)
        self.habit_manager = HabitManager(self.data_manager)
        self.weather = WeatherWidget()
        
        # Create UI
        self.create_ui()
        self.refresh_all()
        
        # Auto-save every 30 seconds
        self.auto_save()
    
    def auto_save(self):
        """Auto-save data periodically"""
        self.data_manager.save_data()
        self.root.after(30000, self.auto_save)  # 30 seconds
    
    def create_ui(self):
        """Create the main user interface"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill="x", pady=(0, 10))
        
        title_label = ttk.Label(header_frame, text="🚀 ProductivityHub", font=("Arial", 20, "bold"))
        title_label.pack(side="left")
        
        # Time display
        self.time_var = tk.StringVar()
        time_label = ttk.Label(header_frame, textvariable=self.time_var, font=("Arial", 12))
        time_label.pack(side="right")
        self.update_time()
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True)
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_tasks_tab()
        self.create_notes_tab()
        self.create_expenses_tab()
        self.create_habits_tab()
        self.create_tools_tab()
    
    def update_time(self):
        """Update the time display"""
        now = datetime.now()
        time_str = now.strftime("%Y-%m-%d %H:%M:%S")
        self.time_var.set(time_str)
        self.root.after(1000, self.update_time)
    
    def create_dashboard_tab(self):
        """Create the dashboard overview tab"""
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="Dashboard")

        # Create scrollable frame
        canvas = tk.Canvas(dashboard_frame)
        scrollbar = ttk.Scrollbar(dashboard_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Dashboard content
        content_frame = ttk.Frame(scrollable_frame, padding="20")
        content_frame.pack(fill="both", expand=True)
        
        # Greeting
        hour = datetime.now().hour
        if hour < 12:
            greeting = "Good Morning! 🌅"
        elif hour < 17:
            greeting = "Good Afternoon! ☀️"
        else:
            greeting = "Good Evening! 🌙"
        
        greeting_label = ttk.Label(content_frame, text=greeting, font=("Arial", 16, "bold"))
        greeting_label.pack(pady=(0, 20))
        
        # Stats frame
        stats_frame = ttk.LabelFrame(content_frame, text="Today's Overview", padding="10")
        stats_frame.pack(fill="x", pady=10)
        
        # Create stats display
        self.stats_frame = stats_frame
        self.update_dashboard_stats()
        
        # Weather widget
        weather_frame = ttk.LabelFrame(content_frame, text="Weather", padding="10")
        weather_frame.pack(fill="x", pady=10)
        
        self.weather_frame = weather_frame
        self.update_weather()
        
        # Quick actions
        actions_frame = ttk.LabelFrame(content_frame, text="Quick Actions", padding="10")
        actions_frame.pack(fill="x", pady=10)
        
        ttk.Button(actions_frame, text="Add Task", 
                  command=self.quick_add_task).pack(side="left", padx=5)
        ttk.Button(actions_frame, text="Add Note", 
                  command=self.quick_add_note).pack(side="left", padx=5)
        ttk.Button(actions_frame, text="Add Expense", 
                  command=self.quick_add_expense).pack(side="left", padx=5)
    
    def update_dashboard_stats(self):
        """Update dashboard statistics"""
        # Clear existing widgets
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        # Tasks stats
        tasks = self.task_manager.get_tasks()
        completed_tasks = sum(1 for task in tasks if task.get("completed", False))
        total_tasks = len(tasks)
        
        task_stats = ttk.Label(self.stats_frame, 
                              text=f"Tasks: {completed_tasks}/{total_tasks} completed")
        task_stats.grid(row=0, column=0, sticky="w", padx=10)
        
        # Notes count
        notes_count = len(self.notes_manager.get_notes())
        notes_stats = ttk.Label(self.stats_frame, text=f"Notes: {notes_count}")
        notes_stats.grid(row=0, column=1, sticky="w", padx=10)
        
        # Expense stats
        expense_stats = self.expense_manager.get_stats()
        expense_label = ttk.Label(self.stats_frame, 
                                 text=f"Monthly Expenses: ${expense_stats['monthly_total']:.2f}")
        expense_label.grid(row=1, column=0, sticky="w", padx=10)
        
        # Habits stats
        habits = self.habit_manager.get_habits()
        completed_today = sum(1 for habit in habits 
                            if self.habit_manager.is_completed_today(habit["id"]))
        habits_stats = ttk.Label(self.stats_frame, 
                               text=f"Habits Today: {completed_today}/{len(habits)}")
        habits_stats.grid(row=1, column=1, sticky="w", padx=10)
    
    def update_weather(self):
        """Update weather display"""
        # Clear existing widgets
        for widget in self.weather_frame.winfo_children():
            widget.destroy()
        
        try:
            weather_data = self.weather.get_weather()
            
            location_label = ttk.Label(self.weather_frame, 
                                     text=f"📍 {weather_data['location']}", 
                                     font=("Arial", 12, "bold"))
            location_label.pack()
            
            temp_label = ttk.Label(self.weather_frame, 
                                 text=f"🌡️ {weather_data['temperature']}°F - {weather_data['condition']}")
            temp_label.pack()
            
            details_label = ttk.Label(self.weather_frame, 
                                    text=f"💧 {weather_data['humidity']}% humidity • 💨 {weather_data['wind_speed']} mph wind")
            details_label.pack()
            
        except Exception as e:
            error_label = ttk.Label(self.weather_frame, text="Weather data unavailable")
            error_label.pack()
    
    def quick_add_task(self):
        """Quick add task dialog"""
        title = simpledialog.askstring("Add Task", "Enter task title:")
        if title:
            self.task_manager.add_task(title.strip())
            self.refresh_tasks()
            self.update_dashboard_stats()
    
    def quick_add_note(self):
        """Quick add note dialog"""
        title = simpledialog.askstring("Add Note", "Enter note title:")
        if title:
            content = simpledialog.askstring("Add Note", "Enter note content:")
            if content:
                self.notes_manager.add_note(title.strip(), content.strip())
                self.refresh_notes()
                self.update_dashboard_stats()
    
    def quick_add_expense(self):
        """Quick add expense dialog"""
        description = simpledialog.askstring("Add Expense", "Enter expense description:")
        if description:
            amount = simpledialog.askfloat("Add Expense", "Enter amount:")
            if amount is not None and amount > 0:
                self.expense_manager.add_expense(description.strip(), amount, "Other")
                self.refresh_expenses()
                self.update_dashboard_stats()
    
    def create_tasks_tab(self):
        """Create the tasks management tab"""
        tasks_frame = ttk.Frame(self.notebook)
        self.notebook.add(tasks_frame, text="Tasks")
        
        # Header with add button
        header_frame = ttk.Frame(tasks_frame)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(header_frame, text="Task Management", 
                 font=("Arial", 14, "bold")).pack(side="left")
        ttk.Button(header_frame, text="Add Task", 
                  command=self.add_task_dialog).pack(side="right")
        
        # Tasks list
        list_frame = ttk.Frame(tasks_frame)
        list_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Create treeview for tasks
        columns = ("ID", "Task", "Status", "Created")
        self.tasks_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        self.tasks_tree.heading("ID", text="ID")
        self.tasks_tree.heading("Task", text="Task")
        self.tasks_tree.heading("Status", text="Status")
        self.tasks_tree.heading("Created", text="Created")
        
        self.tasks_tree.column("ID", width=50)
        self.tasks_tree.column("Task", width=300)
        self.tasks_tree.column("Status", width=100)
        self.tasks_tree.column("Created", width=150)
        
        # Scrollbar for tasks
        tasks_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tasks_tree.yview)
        self.tasks_tree.configure(yscrollcommand=tasks_scrollbar.set)
        
        self.tasks_tree.pack(side="left", fill="both", expand=True)
        tasks_scrollbar.pack(side="right", fill="y")
        
        # Context menu for tasks
        self.tasks_context_menu = tk.Menu(self.root, tearoff=0)
        self.tasks_context_menu.add_command(label="Toggle Complete", command=self.toggle_task)
        self.tasks_context_menu.add_command(label="Edit", command=self.edit_task_dialog)
        self.tasks_context_menu.add_command(label="Delete", command=self.delete_task)
        
        self.tasks_tree.bind("<Button-3>", self.show_tasks_context_menu)
        self.tasks_tree.bind("<Double-1>", self.toggle_task)
    
    def show_tasks_context_menu(self, event):
        """Show context menu for tasks"""
        if self.tasks_tree.selection():
            self.tasks_context_menu.post(event.x_root, event.y_root)
    
    def add_task_dialog(self):
        """Show add task dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Task")
        dialog.geometry("400x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill="both", expand=True)
        
        ttk.Label(frame, text="Task Title:").pack(anchor="w")
        title_var = tk.StringVar()
        title_entry = ttk.Entry(frame, textvariable=title_var, width=40)
        title_entry.pack(fill="x", pady=5)
        title_entry.focus()
        
        def save_task():
            title = title_var.get().strip()
            if title:
                self.task_manager.add_task(title)
                self.refresh_tasks()
                self.update_dashboard_stats()
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Please enter a task title")
        
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill="x", pady=10)
        
        ttk.Button(button_frame, text="Cancel", 
                  command=dialog.destroy).pack(side="right", padx=5)
        ttk.Button(button_frame, text="Save", 
                  command=save_task).pack(side="right")
        
        # Bind Enter key to save
        dialog.bind('<Return>', lambda e: save_task())
    
    def edit_task_dialog(self):
        """Show edit task dialog"""
        selection = self.tasks_tree.selection()
        if not selection:
            return
        
        item = self.tasks_tree.item(selection[0])
        task_id = int(item['values'][0])
        
        # Find the task
        task = next((t for t in self.task_manager.get_tasks() if t['id'] == task_id), None)
        if not task:
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Task")
        dialog.geometry("400x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill="both", expand=True)
        
        ttk.Label(frame, text="Task Title:").pack(anchor="w")
        title_var = tk.StringVar(value=task['title'])
        title_entry = ttk.Entry(frame, textvariable=title_var, width=40)
        title_entry.pack(fill="x", pady=5)
        
        completed_var = tk.BooleanVar(value=task.get('completed', False))
        ttk.Checkbutton(frame, text="Completed", variable=completed_var).pack(anchor="w", pady=5)
        
        def save_task():
            title = title_var.get().strip()
            if title:
                self.task_manager.update_task(task_id, title=title, completed=completed_var.get())
                self.refresh_tasks()
                self.update_dashboard_stats()
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Please enter a task title")
        
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill="x", pady=10)
        
        ttk.Button(button_frame, text="Cancel", 
                  command=dialog.destroy).pack(side="right", padx=5)
        ttk.Button(button_frame, text="Save", 
                  command=save_task).pack(side="right")
    
    def toggle_task(self, event=None):
        """Toggle task completion"""
        selection = self.tasks_tree.selection()
        if not selection:
            return
        
        item = self.tasks_tree.item(selection[0])
        task_id = int(item['values'][0])
        
        # Find the task
        task = next((t for t in self.task_manager.get_tasks() if t['id'] == task_id), None)
        if task:
            new_status = not task.get('completed', False)
            self.task_manager.update_task(task_id, completed=new_status)
            self.refresh_tasks()
            self.update_dashboard_stats()
    
    def delete_task(self):
        """Delete selected task"""
        selection = self.tasks_tree.selection()
        if not selection:
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?"):
            item = self.tasks_tree.item(selection[0])
            task_id = int(item['values'][0])
            self.task_manager.delete_task(task_id)
            self.refresh_tasks()
            self.update_dashboard_stats()
    
    def refresh_tasks(self):
        """Refresh the tasks display"""
        # Clear existing items
        for item in self.tasks_tree.get_children():
            self.tasks_tree.delete(item)
        
        # Add tasks
        for task in self.task_manager.get_tasks():
            status = "✅ Completed" if task.get('completed', False) else "⏳ Pending"
            created = datetime.fromisoformat(task['created_at']).strftime("%Y-%m-%d %H:%M")
            
            self.tasks_tree.insert("", "end", values=(
                task['id'],
                task['title'],
                status,
                created
            ))
    
    def create_notes_tab(self):
        """Create the notes management tab"""
        notes_frame = ttk.Frame(self.notebook)
        self.notebook.add(notes_frame, text="Notes")
        
        # Header with add button and search
        header_frame = ttk.Frame(notes_frame)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(header_frame, text="Notes", 
                 font=("Arial", 14, "bold")).pack(side="left")
        
        # Search frame
        search_frame = ttk.Frame(header_frame)
        search_frame.pack(side="right")
        
        ttk.Button(search_frame, text="Add Note", 
                  command=self.add_note_dialog).pack(side="right", padx=(10, 0))
        
        self.notes_search_var = tk.StringVar()
        self.notes_search_var.trace("w", self.filter_notes)
        search_entry = ttk.Entry(search_frame, textvariable=self.notes_search_var, width=20)
        search_entry.pack(side="right", padx=5)
        ttk.Label(search_frame, text="Search:").pack(side="right")
        
        # Notes list
        list_frame = ttk.Frame(notes_frame)
        list_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Create treeview for notes
        columns = ("ID", "Title", "Color", "Updated")
        self.notes_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        self.notes_tree.heading("ID", text="ID")
        self.notes_tree.heading("Title", text="Title")
        self.notes_tree.heading("Color", text="Color")
        self.notes_tree.heading("Updated", text="Updated")
        
        self.notes_tree.column("ID", width=50)
        self.notes_tree.column("Title", width=300)
        self.notes_tree.column("Color", width=100)
        self.notes_tree.column("Updated", width=150)
        
        # Scrollbar for notes
        notes_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.notes_tree.yview)
        self.notes_tree.configure(yscrollcommand=notes_scrollbar.set)
        
        self.notes_tree.pack(side="left", fill="both", expand=True)
        notes_scrollbar.pack(side="right", fill="y")
        
        # Context menu for notes
        self.notes_context_menu = tk.Menu(self.root, tearoff=0)
        self.notes_context_menu.add_command(label="View/Edit", command=self.edit_note_dialog)
        self.notes_context_menu.add_command(label="Delete", command=self.delete_note)
        
        self.notes_tree.bind("<Button-3>", self.show_notes_context_menu)
        self.notes_tree.bind("<Double-1>", self.edit_note_dialog)
    
    def show_notes_context_menu(self, event):
        """Show context menu for notes"""
        if self.notes_tree.selection():
            self.notes_context_menu.post(event.x_root, event.y_root)
    
    def filter_notes(self, *args):
        """Filter notes based on search query"""
        self.refresh_notes()
    
    def add_note_dialog(self):
        """Show add note dialog"""
        self.show_note_dialog()
    
    def edit_note_dialog(self, event=None):
        """Show edit note dialog"""
        selection = self.notes_tree.selection()
        if not selection:
            return
        
        item = self.notes_tree.item(selection[0])
        note_id = int(item['values'][0])
        
        # Find the note
        note = next((n for n in self.notes_manager.get_notes() if n['id'] == note_id), None)
        if note:
            self.show_note_dialog(note)
    
    def show_note_dialog(self, note=None):
        """Show note dialog for add or edit"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Note" if note else "Add Note")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill="both", expand=True)
        
        # Title
        ttk.Label(frame, text="Title:").pack(anchor="w")
        title_var = tk.StringVar(value=note['title'] if note else "")
        title_entry = ttk.Entry(frame, textvariable=title_var, width=50)
        title_entry.pack(fill="x", pady=5)
        
        # Color
        color_frame = ttk.Frame(frame)
        color_frame.pack(fill="x", pady=5)
        ttk.Label(color_frame, text="Color:").pack(side="left")
        
        color_var = tk.StringVar(value=note['color'] if note else "yellow")
        colors = ["yellow", "blue", "green", "pink", "purple"]
        color_combo = ttk.Combobox(color_frame, textvariable=color_var, values=colors, state="readonly")
        color_combo.pack(side="left", padx=10)
        
        # Content
        ttk.Label(frame, text="Content:").pack(anchor="w", pady=(10, 0))
        content_text = tk.Text(frame, wrap="word", height=15)
        content_text.pack(fill="both", expand=True, pady=5)
        
        if note:
            content_text.insert("1.0", note['content'])
        
        def save_note():
            title = title_var.get().strip()
            content = content_text.get("1.0", "end-1c").strip()
            
            if not title or not content:
                messagebox.showerror("Error", "Please enter both title and content")
                return
            
            if note:
                self.notes_manager.update_note(note['id'], title=title, content=content, color=color_var.get())
            else:
                self.notes_manager.add_note(title, content, color_var.get())
            
            self.refresh_notes()
            self.update_dashboard_stats()
            dialog.destroy()
        
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill="x", pady=10)
        
        ttk.Button(button_frame, text="Cancel", 
                  command=dialog.destroy).pack(side="right", padx=5)
        ttk.Button(button_frame, text="Save", 
                  command=save_note).pack(side="right")
    
    def delete_note(self):
        """Delete selected note"""
        selection = self.notes_tree.selection()
        if not selection:
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this note?"):
            item = self.notes_tree.item(selection[0])
            note_id = int(item['values'][0])
            self.notes_manager.delete_note(note_id)
            self.refresh_notes()
            self.update_dashboard_stats()
    
    def refresh_notes(self):
        """Refresh the notes display"""
        # Clear existing items
        for item in self.notes_tree.get_children():
            self.notes_tree.delete(item)
        
        # Get search query
        search_query = self.notes_search_var.get().lower()
        
        # Add notes
        for note in self.notes_manager.get_notes():
            # Filter by search query
            if search_query and search_query not in note['title'].lower() and search_query not in note['content'].lower():
                continue
            
            updated = datetime.fromisoformat(note['updated_at']).strftime("%Y-%m-%d %H:%M")
            
            self.notes_tree.insert("", "end", values=(
                note['id'],
                note['title'],
                note['color'].title(),
                updated
            ))
    
    def create_expenses_tab(self):
        """Create the expenses management tab"""
        expenses_frame = ttk.Frame(self.notebook)
        self.notebook.add(expenses_frame, text="Expenses")
        
        # Header with add button and stats
        header_frame = ttk.Frame(expenses_frame)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(header_frame, text="Expense Tracker", 
                 font=("Arial", 14, "bold")).pack(side="left")
        ttk.Button(header_frame, text="Add Expense", 
                  command=self.add_expense_dialog).pack(side="right")
        
        # Stats frame
        stats_frame = ttk.LabelFrame(expenses_frame, text="Spending Summary", padding="10")
        stats_frame.pack(fill="x", padx=10, pady=5)
        
        self.expense_stats_frame = stats_frame
        self.update_expense_stats()
        
        # Expenses list
        list_frame = ttk.Frame(expenses_frame)
        list_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))
        
        # Create treeview for expenses
        columns = ("ID", "Description", "Amount", "Category", "Date")
        self.expenses_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=12)
        
        self.expenses_tree.heading("ID", text="ID")
        self.expenses_tree.heading("Description", text="Description")
        self.expenses_tree.heading("Amount", text="Amount")
        self.expenses_tree.heading("Category", text="Category")
        self.expenses_tree.heading("Date", text="Date")
        
        self.expenses_tree.column("ID", width=50)
        self.expenses_tree.column("Description", width=200)
        self.expenses_tree.column("Amount", width=100)
        self.expenses_tree.column("Category", width=150)
        self.expenses_tree.column("Date", width=150)
        
        # Scrollbar for expenses
        expenses_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.expenses_tree.yview)
        self.expenses_tree.configure(yscrollcommand=expenses_scrollbar.set)
        
        self.expenses_tree.pack(side="left", fill="both", expand=True)
        expenses_scrollbar.pack(side="right", fill="y")
        
        # Context menu for expenses
        self.expenses_context_menu = tk.Menu(self.root, tearoff=0)
        self.expenses_context_menu.add_command(label="Edit", command=self.edit_expense_dialog)
        self.expenses_context_menu.add_command(label="Delete", command=self.delete_expense)
        
        self.expenses_tree.bind("<Button-3>", self.show_expenses_context_menu)
        self.expenses_tree.bind("<Double-1>", self.edit_expense_dialog)
    
    def show_expenses_context_menu(self, event):
        """Show context menu for expenses"""
        if self.expenses_tree.selection():
            self.expenses_context_menu.post(event.x_root, event.y_root)
    
    def update_expense_stats(self):
        """Update expense statistics display"""
        # Clear existing widgets
        for widget in self.expense_stats_frame.winfo_children():
            widget.destroy()
        
        stats = self.expense_manager.get_stats()
        
        weekly_label = ttk.Label(self.expense_stats_frame, 
                               text=f"This Week: {stats['weekly_total']:.2f}.Rs")
        weekly_label.grid(row=0, column=0, padx=20)
        
        monthly_label = ttk.Label(self.expense_stats_frame, 
                                text=f"This Month: {stats['monthly_total']:.2f}.Rs")
        monthly_label.grid(row=0, column=1, padx=20)
        
        daily_label = ttk.Label(self.expense_stats_frame, 
                              text=f"Daily Average: {stats['daily_average']:.2f}.Rs")
        daily_label.grid(row=0, column=2, padx=20)
    
    def add_expense_dialog(self):
        """Show add expense dialog"""
        self.show_expense_dialog()
    
    def edit_expense_dialog(self, event=None):
        """Show edit expense dialog"""
        selection = self.expenses_tree.selection()
        if not selection:
            return
        
        item = self.expenses_tree.item(selection[0])
        expense_id = int(item['values'][0])
        
        # Find the expense
        expense = next((e for e in self.expense_manager.get_expenses() if e['id'] == expense_id), None)
        if expense:
            self.show_expense_dialog(expense)
    
    def show_expense_dialog(self, expense=None):
        """Show expense dialog for add or edit"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Expense" if expense else "Add Expense")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill="both", expand=True)
        
        # Description
        ttk.Label(frame, text="Description:").pack(anchor="w")
        description_var = tk.StringVar(value=expense['description'] if expense else "")
        description_entry = ttk.Entry(frame, textvariable=description_var, width=40)
        description_entry.pack(fill="x", pady=5)
        
        # Amount
        ttk.Label(frame, text="Amount:").pack(anchor="w", pady=(10, 0))
        amount_var = tk.StringVar(value=str(expense['amount']) if expense else "")
        amount_entry = ttk.Entry(frame, textvariable=amount_var, width=20)
        amount_entry.pack(anchor="w", pady=5)
        
        # Category
        ttk.Label(frame, text="Category:").pack(anchor="w", pady=(10, 0))
        category_var = tk.StringVar(value=expense['category'] if expense else "Other")
        categories = ["Food & Dining", "Transportation", "Shopping", "Entertainment", 
                     "Bills & Utilities", "Healthcare", "Travel", "Other"]
        category_combo = ttk.Combobox(frame, textvariable=category_var, values=categories)
        category_combo.pack(anchor="w", pady=5)
        
        # Date
        ttk.Label(frame, text="Date:").pack(anchor="w", pady=(10, 0))
        if expense:
            date_str = datetime.fromisoformat(expense['date']).strftime("%Y-%m-%d")
        else:
            date_str = datetime.now().strftime("%Y-%m-%d")
        date_var = tk.StringVar(value=date_str)
        date_entry = ttk.Entry(frame, textvariable=date_var, width=20)
        date_entry.pack(anchor="w", pady=5)
        
        def save_expense():
            description = description_var.get().strip()
            amount_str = amount_var.get().strip()
            category = category_var.get()
            date_str = date_var.get()
            
            if not description or not amount_str:
                messagebox.showerror("Error", "Please enter description and amount")
                return
            
            try:
                amount = float(amount_str)
                if amount <= 0:
                    raise ValueError("Amount must be positive")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid positive amount")
                return
            
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Please enter date in YYYY-MM-DD format")
                return
            
            if expense:
                self.expense_manager.update_expense(expense['id'], 
                                                  description=description, 
                                                  amount=amount, 
                                                  category=category, 
                                                  date=date_obj.isoformat())
            else:
                self.expense_manager.add_expense(description, amount, category, date_obj)
            
            self.refresh_expenses()
            self.update_expense_stats()
            self.update_dashboard_stats()
            dialog.destroy()
        
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill="x", pady=20)
        
        ttk.Button(button_frame, text="Cancel", 
                  command=dialog.destroy).pack(side="right", padx=5)
        ttk.Button(button_frame, text="Save", 
                  command=save_expense).pack(side="right")
    
    def delete_expense(self):
        """Delete selected expense"""
        selection = self.expenses_tree.selection()
        if not selection:
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this expense?"):
            item = self.expenses_tree.item(selection[0])
            expense_id = int(item['values'][0])
            self.expense_manager.delete_expense(expense_id)
            self.refresh_expenses()
            self.update_expense_stats()
            self.update_dashboard_stats()
    
    def refresh_expenses(self):
        """Refresh the expenses display"""
        # Clear existing items
        for item in self.expenses_tree.get_children():
            self.expenses_tree.delete(item)
        
        # Add expenses
        for expense in self.expense_manager.get_expenses():
            date_str = datetime.fromisoformat(expense['date']).strftime("%Y-%m-%d")
            
            self.expenses_tree.insert("", "end", values=(
                expense['id'],
                expense['description'],
                f"${expense['amount']:.2f}",
                expense['category'],
                date_str
            ))
    
    def create_habits_tab(self):
        """Create the habits management tab"""
        habits_frame = ttk.Frame(self.notebook)
        self.notebook.add(habits_frame, text="Habits")
        
        # Header with add button
        header_frame = ttk.Frame(habits_frame)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(header_frame, text="Habit Tracker", 
                 font=("Arial", 14, "bold")).pack(side="left")
        ttk.Button(header_frame, text="Add Habit", 
                  command=self.add_habit_dialog).pack(side="right")
        
        # Habits list
        list_frame = ttk.Frame(habits_frame)
        list_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Create treeview for habits
        columns = ("ID", "Icon", "Habit", "Streak", "Today", "Color")
        self.habits_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        self.habits_tree.heading("ID", text="ID")
        self.habits_tree.heading("Icon", text="Icon")
        self.habits_tree.heading("Habit", text="Habit")
        self.habits_tree.heading("Streak", text="Streak")
        self.habits_tree.heading("Today", text="Today")
        self.habits_tree.heading("Color", text="Color")
        
        self.habits_tree.column("ID", width=50)
        self.habits_tree.column("Icon", width=60)
        self.habits_tree.column("Habit", width=200)
        self.habits_tree.column("Streak", width=100)
        self.habits_tree.column("Today", width=100)
        self.habits_tree.column("Color", width=100)
        
        # Scrollbar for habits
        habits_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.habits_tree.yview)
        self.habits_tree.configure(yscrollcommand=habits_scrollbar.set)
        
        self.habits_tree.pack(side="left", fill="both", expand=True)
        habits_scrollbar.pack(side="right", fill="y")
        
        # Context menu for habits
        self.habits_context_menu = tk.Menu(self.root, tearoff=0)
        self.habits_context_menu.add_command(label="Toggle Today", command=self.toggle_habit)
        self.habits_context_menu.add_command(label="Edit", command=self.edit_habit_dialog)
        self.habits_context_menu.add_command(label="Delete", command=self.delete_habit)
        
        self.habits_tree.bind("<Button-3>", self.show_habits_context_menu)
        self.habits_tree.bind("<Double-1>", self.toggle_habit)
    
    def show_habits_context_menu(self, event):
        """Show context menu for habits"""
        if self.habits_tree.selection():
            self.habits_context_menu.post(event.x_root, event.y_root)
    
    def add_habit_dialog(self):
        """Show add habit dialog"""
        self.show_habit_dialog()
    
    def edit_habit_dialog(self, event=None):
        """Show edit habit dialog"""
        selection = self.habits_tree.selection()
        if not selection:
            return
        
        item = self.habits_tree.item(selection[0])
        habit_id = int(item['values'][0])
        
        # Find the habit
        habit = next((h for h in self.habit_manager.get_habits() if h['id'] == habit_id), None)
        if habit:
            self.show_habit_dialog(habit)
    
    def show_habit_dialog(self, habit=None):
        """Show habit dialog for add or edit"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Habit" if habit else "Add Habit")
        dialog.geometry("400x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill="both", expand=True)
        
        # Name
        ttk.Label(frame, text="Habit Name:").pack(anchor="w")
        name_var = tk.StringVar(value=habit['name'] if habit else "")
        name_entry = ttk.Entry(frame, textvariable=name_var, width=40)
        name_entry.pack(fill="x", pady=5)
        
        # Icon
        ttk.Label(frame, text="Icon:").pack(anchor="w", pady=(10, 0))
        icon_var = tk.StringVar(value=habit['icon'] if habit else "💪")
        icons = ["💪", "📚", "🏃", "🧘", "💧", "🎯", "🌱", "✍️", "🎨", "🎵"]
        icon_combo = ttk.Combobox(frame, textvariable=icon_var, values=icons, width=20)
        icon_combo.pack(anchor="w", pady=5)
        
        # Color
        ttk.Label(frame, text="Color:").pack(anchor="w", pady=(10, 0))
        color_var = tk.StringVar(value=habit['color'] if habit else "blue")
        colors = ["blue", "green", "purple", "red", "yellow", "pink"]
        color_combo = ttk.Combobox(frame, textvariable=color_var, values=colors, state="readonly")
        color_combo.pack(anchor="w", pady=5)
        
        def save_habit():
            name = name_var.get().strip()
            
            if not name:
                messagebox.showerror("Error", "Please enter a habit name")
                return
            
            if habit:
                self.habit_manager.update_habit(habit['id'], 
                                              name=name, 
                                              icon=icon_var.get(), 
                                              color=color_var.get())
            else:
                self.habit_manager.add_habit(name, icon_var.get(), color_var.get())
            
            self.refresh_habits()
            self.update_dashboard_stats()
            dialog.destroy()
        
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill="x", pady=20)
        
        ttk.Button(button_frame, text="Cancel", 
                  command=dialog.destroy).pack(side="right", padx=5)
        ttk.Button(button_frame, text="Save", 
                  command=save_habit).pack(side="right")
        
        if habit:
            def delete_habit_action():
                if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this habit?"):
                    self.habit_manager.delete_habit(habit['id'])
                    self.refresh_habits()
                    self.update_dashboard_stats()
                    dialog.destroy()
            
            ttk.Button(button_frame, text="Delete", 
                      command=delete_habit_action).pack(side="left")
    
    def toggle_habit(self, event=None):
        """Toggle habit completion for today"""
        selection = self.habits_tree.selection()
        if not selection:
            return
        
        item = self.habits_tree.item(selection[0])
        habit_id = int(item['values'][0])
        
        self.habit_manager.toggle_habit_completion(habit_id)
        self.refresh_habits()
        self.update_dashboard_stats()
    
    def delete_habit(self):
        """Delete selected habit"""
        selection = self.habits_tree.selection()
        if not selection:
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this habit?"):
            item = self.habits_tree.item(selection[0])
            habit_id = int(item['values'][0])
            self.habit_manager.delete_habit(habit_id)
            self.refresh_habits()
            self.update_dashboard_stats()
    
    def refresh_habits(self):
        """Refresh the habits display"""
        # Clear existing items
        for item in self.habits_tree.get_children():
            self.habits_tree.delete(item)
        
        # Add habits
        for habit in self.habit_manager.get_habits():
            completed_today = "✅ Done" if self.habit_manager.is_completed_today(habit['id']) else "⏳ Pending"
            streak_text = f"🔥 {habit['streak']} days"
            
            self.habits_tree.insert("", "end", values=(
                habit['id'],
                habit['icon'],
                habit['name'],
                streak_text,
                completed_today,
                habit['color'].title()
            ))
    
    def create_tools_tab(self):
        """Create the quick tools tab"""
        tools_frame = ttk.Frame(self.notebook)
        self.notebook.add(tools_frame, text="Quick Tools")
        
        # Header
        header_frame = ttk.Frame(tools_frame)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(header_frame, text="Quick Tools", 
                 font=("Arial", 14, "bold")).pack(side="left")
        
        # Tools grid
        tools_grid = ttk.Frame(tools_frame)
        tools_grid.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Calculator
        calc_frame = ttk.LabelFrame(tools_grid, text="Calculator", padding="20")
        calc_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        ttk.Label(calc_frame, text="🧮", font=("Arial", 24)).pack()
        ttk.Label(calc_frame, text="Perform calculations").pack()
        ttk.Button(calc_frame, text="Open Calculator", 
                  command=self.open_calculator).pack(pady=10)
        
        # Password Generator
        pwd_frame = ttk.LabelFrame(tools_grid, text="Password Generator", padding="20")
        pwd_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        ttk.Label(pwd_frame, text="🔐", font=("Arial", 24)).pack()
        ttk.Label(pwd_frame, text="Generate secure passwords").pack()
        ttk.Button(pwd_frame, text="Generate Password", 
                  command=self.open_password_generator).pack(pady=10)
        
        # Unit Converter
        conv_frame = ttk.LabelFrame(tools_grid, text="Unit Converter", padding="20")
        conv_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        ttk.Label(conv_frame, text="🔄", font=("Arial", 24)).pack()
        ttk.Label(conv_frame, text="Convert units").pack()
        ttk.Button(conv_frame, text="Open Converter", 
                  command=self.open_unit_converter).pack(pady=10)
        
        # Timer
        timer_frame = ttk.LabelFrame(tools_grid, text="Timer", padding="20")
        timer_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        ttk.Label(timer_frame, text="⏰", font=("Arial", 24)).pack()
        ttk.Label(timer_frame, text="Countdown timer").pack()
        ttk.Button(timer_frame, text="Open Timer", 
                  command=self.open_timer).pack(pady=10)
        
        # Configure grid weights
        tools_grid.grid_columnconfigure(0, weight=1)
        tools_grid.grid_columnconfigure(1, weight=1)
        tools_grid.grid_rowconfigure(0, weight=1)
        tools_grid.grid_rowconfigure(1, weight=1)
    
    def open_calculator(self):
        """Open calculator tool"""
        calc = CalculatorWidget(self.root)
        calc.create_calculator_window()
    
    def open_password_generator(self):
        """Open password generator tool"""
        PasswordGenerator.create_password_window(self.root)
    
    def open_unit_converter(self):
        """Open unit converter tool"""
        UnitConverter.create_converter_window(self.root)
    
    def open_timer(self):
        """Open timer tool"""
        TimerWidget.create_timer_window(self.root)
    
    def refresh_all(self):
        """Refresh all displays"""
        self.refresh_tasks()
        self.refresh_notes()
        self.refresh_expenses()
        self.refresh_habits()
        self.update_dashboard_stats()
        self.update_expense_stats()
        self.update_weather()
    
    def run(self):
        """Start the application"""
        # Center the window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Start the main loop
        self.root.mainloop()

def main():
    """Main function to run the application"""
    app = ProductivityHub()
    app.run()

if __name__ == "__main__":
    main()