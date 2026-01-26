import json
import os
from datetime import datetime
from plyer import notification
import time

TASK_FILE = "tasks.json"

PRIORITY_COLORS = {
    "High": "🔴",
    "Medium": "🟠",
    "Low": "🟢"
}

def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, 'r') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASK_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

def add_task(tasks):
    task = input("Enter Task: ").strip()
    time_str = input("Enter Time (HH:MM 24-hour format): ").strip()
    priority = input("Priority (High/Medium/Low): ").capitalize().strip()
    
    if not task:
        print("⚠️ Task cannot be empty!")
        return
    try:
        datetime.strptime(time_str, "%H:%M")
    except ValueError:
        print("⚠️ Invalid time format!")
        return
    
    tasks.append({
        "task": task,
        "time": time_str,
        "priority": priority,
        "done": False
    })
    save_tasks(tasks)
    print("✅ Task added successfully!")

def show_tasks(tasks):
    if not tasks:
        print("📭 No tasks available.")
        return
    for idx, t in enumerate(tasks):
        status = "✅" if t['done'] else "❌"
        icon = PRIORITY_COLORS.get(t['priority'], '')
        print(f"{idx+1}. {status} [{t['time']}] {icon} {t['priority']} - {t['task']}")

def delete_task(tasks):
    show_tasks(tasks)
    try:
        idx = int(input("Enter task number to delete: ")) - 1
        if 0 <= idx < len(tasks):
            tasks.pop(idx)
            save_tasks(tasks)
            print("🗑️ Task deleted.")
        else:
            print("❌ Invalid task number.")
    except ValueError:
        print("⚠️ Please enter a valid number.")

def mark_done(tasks):
    show_tasks(tasks)
    try:
        idx = int(input("Enter task number to mark as done: ")) - 1
        if 0 <= idx < len(tasks):
            tasks[idx]["done"] = True
            save_tasks(tasks)
            print("✔️ Task marked as done.")
        else:
            print("❌ Invalid task number.")
    except ValueError:
        print("⚠️ Please enter a valid number.")

def edit_task(tasks):
    show_tasks(tasks)
    try:
        idx = int(input("Enter task number to edit: ")) - 1
        if 0 <= idx < len(tasks):
            task = input("New Task (leave blank to keep same): ").strip()
            time_str = input("New Time (HH:MM, leave blank to keep same): ").strip()
            priority = input("New Priority (High/Medium/Low): ").capitalize().strip()

            if task:
                tasks[idx]["task"] = task
            if time_str:
                try:
                    datetime.strptime(time_str, "%H:%M")
                    tasks[idx]["time"] = time_str
                except ValueError:
                    print("⚠️ Invalid time format!")
            if priority in PRIORITY_COLORS:
                tasks[idx]["priority"] = priority
            
            save_tasks(tasks)
            print("✏️ Task updated.")
        else:
            print("❌ Invalid task number.")
    except ValueError:
        print("⚠️ Please enter a valid number.")

def check_reminders(tasks):
    now = datetime.now().strftime("%H:%M")
    for t in tasks:
        if t['time'] == now and not t['done']:
            notification.notify(
                title="🔔 Task Reminder",
                message=f"{t['task']} (Priority: {t['priority']})",
                timeout=5
            )
            t['done'] = True
    save_tasks(tasks)

def main():
    tasks = load_tasks()
    print("📋 Welcome to Console TO-DO List by Bhavyansh 😎")

    while True:
        print("\n--- MENU ---")
        print("1. Add Task")
        print("2. Show Tasks")
        print("3. Delete Task")
        print("4. Mark Task as Done")
        print("5. Edit Task")
        print("6. Exit")

        choice = input("Enter choice: ").strip()

        if choice == '1':
            add_task(tasks)
        elif choice == '2':
            show_tasks(tasks)
        elif choice == '3':
            delete_task(tasks)
        elif choice == '4':
            mark_done(tasks)
        elif choice == '5':
            edit_task(tasks)
        elif choice == '6':
            print("👋 Exiting... Have a productive day!")
            break
        else:
            print("❌ Invalid choice!")

        check_reminders(tasks)  # Check after each action

        time.sleep(2)

if __name__ == "__main__":
    main()
