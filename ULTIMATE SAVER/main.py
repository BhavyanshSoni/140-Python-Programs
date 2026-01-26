import os
import time
from colorama import init, Fore, Style

init(autoreset=True)    

def slow_print(text, color=Fore.WHITE, delay=0.03):
    for char in text:
        print(color + char, end='', flush=True)
        time.sleep(delay)
    print(Style.RESET_ALL)

def get_filename(title, category):
    safe_title = title.replace(' ', '_')
    return f"{category}_{safe_title}.txt"

def list_items(category):
    files = [f for f in os.listdir('.') if f.startswith(f"{category}_") and f.endswith('.txt')]
    return files

def save_item(category):
    slow_print(f"You chose to save a {category}!", Fore.CYAN)
    title = input(Fore.YELLOW + f"Enter the title/name for your {category}: ")
    content = input(Fore.YELLOW + f"Enter the content for your {category}: ")
    filename = get_filename(title, category)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    slow_print(f"{category.capitalize()} saved as '{filename}'!", Fore.GREEN)
    time.sleep(1)

def edit_item(category):
    files = list_items(category)
    if not files:
        slow_print(f"Sorry, no {category.replace('_', ' ')}s here. You should save first.", Fore.RED)
        return
    slow_print(f"Available {category.replace('_', ' ')}s:", Fore.CYAN)
    for i, file in enumerate(files, 1):
        slow_print(f"{i}. {file[len(category)+1:-4].replace('_', ' ')}", Fore.YELLOW)
    try:
        idx = int(input(Fore.CYAN + f"Select which {category.replace('_', ' ')} to edit (1-{len(files)}): ")) - 1
        if idx < 0 or idx >= len(files):
            slow_print("Invalid selection!", Fore.RED)
            return
        filename = files[idx]
        with open(filename, 'r', encoding='utf-8') as f:
            old_content = f.read()
        slow_print(f"Current content:\n{old_content}", Fore.CYAN)
        new_content = input(Fore.YELLOW + "Enter new content: ")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(new_content)
        slow_print(f"{category.capitalize()} updated!", Fore.GREEN)
        time.sleep(1)
    except (ValueError, KeyboardInterrupt):
        slow_print("Invalid input!", Fore.RED)

def delete_item(category):
    files = list_items(category)
    if not files:
        slow_print(f"Sorry, no {category.replace('_', ' ')}s here. You should save first.", Fore.RED)
        return
    slow_print(f"Available {category.replace('_', ' ')}s:", Fore.CYAN)
    for i, file in enumerate(files, 1):
        slow_print(f"{i}. {file[len(category)+1:-4].replace('_', ' ')}", Fore.YELLOW)
    try:
        idx = int(input(Fore.CYAN + f"Select which {category.replace('_', ' ')} to delete (1-{len(files)}): ")) - 1
        if idx < 0 or idx >= len(files):
            slow_print("Invalid selection!", Fore.RED)
            return
        filename = files[idx]
        os.remove(filename)
        slow_print(f"{category.capitalize()} '{filename[len(category)+1:-4].replace('_', ' ')}' deleted!", Fore.GREEN)
        time.sleep(1)
    except (ValueError, KeyboardInterrupt):
        slow_print("Invalid input!", Fore.RED)

def main_menu():
    slow_print("Welcome To The ULTIMATE SAVER!", Fore.MAGENTA)
    slow_print("|----------------------|", Fore.MAGENTA)
    slow_print("|Made By BHAVYANSH SONI|", Fore.MAGENTA)
    slow_print("|----------------------|", Fore.MAGENTA)
    slow_print("In This Programme You Can Save Your:", Fore.CYAN)
    slow_print("1. Notes 📜!\n2. Passwords 🔑!\n3. Phone Number 📞!\n4. Code Snippet 👨🏻‍💻!\n5. Reciepe 🧾!\n", Fore.CYAN)
    categories = ["note", "password", "phone_number", "code_snippet", "reciepe"]
    while True:
        slow_print("What do you want to manage?", Fore.YELLOW)
        for i, cat in enumerate(categories, 1):
            slow_print(f"{i}. {cat.replace('_', ' ').title()}", Fore.YELLOW)
        slow_print("6. Exit", Fore.YELLOW)
        try:
            choice = int(input(Fore.CYAN + "(1-6)>> "))
            if choice == 6:
                slow_print("Goodbye!", Fore.MAGENTA)
                break
            if 1 <= choice <= 5:
                category = categories[choice-1]
                action_menu(category)
            else:
                slow_print("Invalid choice!", Fore.RED)
        except (ValueError, KeyboardInterrupt):
            slow_print("❌ Invalid! Action!", Fore.RED)
            break

def action_menu(category):
    while True:
        slow_print(f"\nWhat do you want to do with {category.replace('_', ' ')}?", Fore.YELLOW)
        slow_print("1. Save", Fore.GREEN)
        slow_print("2. Edit", Fore.CYAN)
        slow_print("3. Delete", Fore.RED)
        slow_print("4. Back to main menu", Fore.YELLOW)
        try:
            action = int(input(Fore.CYAN + "(1-4)>> "))
            if action == 1:
                save_item(category)
            elif action == 2:
                edit_item(category)
            elif action == 3:
                delete_item(category)
            elif action == 4:
                break
            else:
                slow_print("Invalid action!", Fore.RED)
        except (ValueError, KeyboardInterrupt):
            slow_print("❌ Invalid! Action!", Fore.RED)
            break

if __name__ == "__main__":
    main_menu()