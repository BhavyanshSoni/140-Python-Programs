from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner
from kivy.uix.checkbox import CheckBox
from kivy.clock import Clock
import json
import os
from datetime import datetime
from plyer import notification
from kivy.config import Config
Config.set('graphics', 'fullscreen', 'auto')  # 'auto' or '1' for fullscreen
Config.set('graphics', 'resizable', False)

TASK_FILE = "tasks.json"

PRIORITY_COLORS = {
    "High": (1, 0.3, 0.3, 1),    # red-ish
    "Medium": (1, 0.7, 0, 1),    # orange-ish
    "Low": (0.3, 1, 0.3, 1)      # green-ish
}

class TaskBox(BoxLayout):
    def __init__(self, task, time, priority, done, main_app, **kwargs):
        super().__init__(orientation='horizontal', size_hint_y=None, height=40, spacing=10, **kwargs)
        self.task = task
        self.time_str = time
        self.priority = priority
        self.done = done if isinstance(done, bool) else False
        self.main_app = main_app

        self.checkbox = CheckBox(active=self.done)
        self.checkbox.bind(active=self.toggle_done)
        self.add_widget(self.checkbox)

        self.lbl_task = Label(text=task)
        self.lbl_time = Label(text=time)
        self.lbl_priority = Label(text=priority, color=PRIORITY_COLORS.get(priority, (1,1,1,1)))

        self.add_widget(self.lbl_task)
        self.add_widget(self.lbl_time)
        self.add_widget(self.lbl_priority)

        self.btn_edit = Button(text="Edit", size_hint_x=0.2)
        self.btn_edit.bind(on_press=self.edit_task)
        self.add_widget(self.btn_edit)

        self.btn_delete = Button(text="Delete", size_hint_x=0.2)
        self.btn_delete.bind(on_press=self.remove_task)
        self.add_widget(self.btn_delete)

    def toggle_done(self, checkbox, value):
        self.done = value
        self.main_app.save_all_tasks()

    def edit_task(self, instance):
        self.main_app.open_edit_popup(self)

    def remove_task(self, instance):
        self.main_app.remove_task(self)

class ToDoApp(App):
    def build(self):
        self.title = "TO-DO List By Bhavyansh Soni 😎"
        self.tasks = self.load_tasks()

        self.root = BoxLayout(orientation='vertical', padding=10, spacing=10)

        input_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)
        self.input_task = TextInput(hint_text="Enter task", multiline=False)
        self.input_time = TextInput(hint_text="HH:MM (24-hour)", size_hint_x=0.3, multiline=False)
        self.priority_spinner = Spinner(text='Medium', values=['High', 'Medium', 'Low'], size_hint_x=0.3)

        btn_add = Button(text="Add Task", size_hint_x=0.3)
        btn_add.bind(on_press=self.add_task)

        input_layout.add_widget(self.input_task)
        input_layout.add_widget(self.input_time)
        input_layout.add_widget(self.priority_spinner)
        input_layout.add_widget(btn_add)

        self.root.add_widget(input_layout)

        self.task_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.task_layout.bind(minimum_height=self.task_layout.setter('height'))
        scroll_view = ScrollView()
        scroll_view.add_widget(self.task_layout)

        self.root.add_widget(scroll_view)

        self.load_task_widgets()
        Clock.schedule_interval(self.check_reminders, 30)

        return self.root

    def load_tasks(self):
        if os.path.exists(TASK_FILE):
            with open(TASK_FILE, "r") as f:
                tasks = json.load(f)
                for t in tasks:
                    if "done" not in t:
                        t["done"] = False
                return tasks
        return []

    def save_tasks(self):
        tasks_to_save = []
        for widget in self.task_layout.children:
            tasks_to_save.append({
                'task': widget.task,
                'time': widget.time_str,
                'priority': widget.priority,
                'done': widget.done
            })
        with open(TASK_FILE, 'w') as f:
            json.dump(tasks_to_save, f, indent=4)

    def load_task_widgets(self):
        self.task_layout.clear_widgets()
        for t in self.tasks:
            self.task_layout.add_widget(TaskBox(t['task'], t['time'], t['priority'], t.get('done', False), self))

    def add_task(self, instance):
        task = self.input_task.text.strip()
        time_str = self.input_time.text.strip()
        priority = self.priority_spinner.text

        if not task:
            self.show_message("Task cannot be empty!")
            return
        if not self.validate_time(time_str):
            self.show_message("Invalid time format! Use HH:MM (24-hour).")
            return

        new_task_widget = TaskBox(task, time_str, priority, False, self)
        self.task_layout.add_widget(new_task_widget)
        self.tasks.append({
            'task': task,
            'time': time_str,
            'priority': priority,
            'done': False
        })
        self.save_tasks()
        self.input_task.text = ""
        self.input_time.text = ""
        self.priority_spinner.text = "Medium"
        self.show_message("Task added!")

    def validate_time(self, time_str):
        try:
            datetime.strptime(time_str, "%H:%M")
            return True
        except:
            return False

    def remove_task(self, task_widget):
        self.task_layout.remove_widget(task_widget)
        self.save_all_tasks()
        self.show_message("Task removed!")

    def save_all_tasks(self):
        self.tasks = []
        for widget in self.task_layout.children:
            self.tasks.append({
                'task': widget.task,
                'time': widget.time_str,
                'priority': widget.priority,
                'done': widget.done
            })
        self.save_tasks()

    def check_reminders(self, dt):
        now = datetime.now().strftime("%H:%M")
        for widget in self.task_layout.children:
            if widget.time_str == now and not widget.done:
                notification.notify(
                    title="Task Reminder 🔔",
                    message=f"{widget.task} (Priority: {widget.priority})",
                    timeout=5
                )

    def open_edit_popup(self, task_widget):
        from kivy.uix.popup import Popup
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        input_task = TextInput(text=task_widget.task, multiline=False)
        input_time = TextInput(text=task_widget.time_str, multiline=False)
        priority_spinner = Spinner(text=task_widget.priority, values=['High', 'Medium', 'Low'])

        btn_save = Button(text="Save")
        btn_cancel = Button(text="Cancel")

        layout.add_widget(Label(text="Edit Task"))
        layout.add_widget(input_task)
        layout.add_widget(input_time)
        layout.add_widget(priority_spinner)

        btn_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)
        btn_layout.add_widget(btn_save)
        btn_layout.add_widget(btn_cancel)
        layout.add_widget(btn_layout)

        popup = Popup(title="Edit Task", content=layout, size_hint=(0.8, 0.6))

        def save_edit(instance):
            new_task = input_task.text.strip()
            new_time = input_time.text.strip()
            new_priority = priority_spinner.text
            if not new_task:
                self.show_message("Task cannot be empty!")
                return
            if not self.validate_time(new_time):
                self.show_message("Invalid time format!")
                return
            task_widget.task = new_task
            task_widget.time_str = new_time
            task_widget.priority = new_priority
            task_widget.lbl_task.text = new_task
            task_widget.lbl_time.text = new_time
            task_widget.lbl_priority.text = new_priority
            task_widget.lbl_priority.color = PRIORITY_COLORS.get(new_priority, (1,1,1,1))
            self.save_all_tasks()
            popup.dismiss()
            self.show_message("Task updated!")

        btn_save.bind(on_press=save_edit)
        btn_cancel.bind(on_press=lambda x: popup.dismiss())

        popup.open()

    def show_message(self, text):
        from kivy.uix.popup import Popup
        layout = BoxLayout(orientation='vertical', padding=10)
        label = Label(text=text)
        btn = Button(text="OK", size_hint=(1, 0.3))
        layout.add_widget(label)
        layout.add_widget(btn)
        popup = Popup(title="Message", content=layout, size_hint=(0.6, 0.4))
        btn.bind(on_press=popup.dismiss)
        popup.open()

if __name__ == '__main__':
    ToDoApp().run()
