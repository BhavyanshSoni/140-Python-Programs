import os

TASKS_FILE = "tasks_data.txt"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as f:
        tasks = [line.strip() for line in f.readlines() if line.strip()]
    return tasks

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        for task in tasks:
            f.write(task + "\n")

def task_menu():
    tasks = load_tasks()
    while True:
        print("\n-- Task Manager --")
        print("1. View tasks")
        print("2. Add task")
        print("3. Remove task")
        print("4. Back to main menu")

        choice = input("Choose option: ").strip()
        if choice == "1":
            if not tasks:
                print("No tasks found.")
            else:
                print("\nYour tasks:")
                for idx, task in enumerate(tasks, 1):
                    print(f"{idx}. {task}")
        elif choice == "2":
            new_task = input("Enter new task: ").strip()
            if new_task:
                tasks.append(new_task)
                save_tasks(tasks)
                print("Task added.")
            else:
                print("Empty task not added.")
        elif choice == "3":
            if not tasks:
                print("No tasks to remove.")
                continue
            print("\nSelect task number to remove:")
            for idx, task in enumerate(tasks, 1):
                print(f"{idx}. {task}")
            try:
                to_remove = int(input("Number: ").strip())
                if 1 <= to_remove <= len(tasks):
                    removed = tasks.pop(to_remove - 1)
                    save_tasks(tasks)
                    print(f"Removed task: {removed}")
                else:
                    print("Invalid number.")
            except ValueError:
                print("Please enter a valid number.")
        elif choice == "4":
            break
        else:
            print("Invalid choice. Try again.")