import os
import json
import time

APP_STORE_FILE = "appstore_data.json"

# Colors for terminal
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033'
    BOLD = '\033[1m'

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def slow_print(text, delay=0.02):
    for c in text:
        print(c, end='', flush=True)
        time.sleep(delay)
    print()

def load_apps():
    if not os.path.exists(APP_STORE_FILE):
        # Create file with some default apps
        default_apps = [
            {
                "name": "Snake Game",
                "desc": "🐍 Classic snake game in terminal",
                "author": "Bhavyansh",
                "category": "Game",
                "install_cmd": "python snake_game.py"
            },
            {
                "name": "ToDo Manager",
                "desc": "✅ Manage daily tasks easily",
                "author": "Bhavyansh",
                "category": "Utility",
                "install_cmd": "python todo_manager.py"
            },
            {
                "name": "Weather CLI",
                "desc": "☀️ Get current weather updates",
                "author": "Bhavyansh",
                "category": "Utility",
                "install_cmd": "python weather_cli.py"
            }
        ]
        with open(APP_STORE_FILE, "w") as f:
            json.dump(default_apps, f, indent=4)
        return default_apps
    else:
        with open(APP_STORE_FILE, "r") as f:
            return json.load(f)

def save_apps(apps):
    with open(APP_STORE_FILE, "w") as f:
        json.dump(apps, f, indent=4)

def list_apps(apps):
    clear()
    print(Colors.OKGREEN + Colors.BOLD + "📱 Welcome to Your Terminal App Store" + Colors.ENDC)
    print(Colors.OKCYAN + "Available Apps:\n" + Colors.ENDC)
    for i, app in enumerate(apps, 1):
        print(f"{Colors.OKBLUE}{i}. {app['name']} {Colors.ENDC}- {app['desc']} ({app['category']}) by {app['author']}")
    print("\nOptions:")
    print(f"{Colors.BOLD}A{Colors.ENDC} - Add new app")
    print(f"{Colors.BOLD}I{Colors.ENDC} + number - Install app (e.g., I1 to install app 1)")
    print(f"{Colors.BOLD}Q{Colors.ENDC} - Quit")

def add_new_app(apps):
    clear()
    print(Colors.HEADER + "➕ Add New App to Store" + Colors.ENDC)
    name = input("Enter app name: ").strip()
    desc = input("Enter short description: ").strip()
    author = input("Enter author name: ").strip()
    category = input("Enter category (Game/Utility/etc): ").strip()
    install_cmd = input("Enter install command or script name: ").strip()
    new_app = {
        "name": name,
        "desc": desc,
        "author": author,
        "category": category,
        "install_cmd": install_cmd
    }
    apps.append(new_app)
    save_apps(apps)
    print(Colors.OKGREEN + "App added successfully!" + Colors.ENDC)
    time.sleep(1)

def install_app(app):
    clear()
    slow_print(Colors.OKCYAN + f"🚀 Installing {app['name']}..." + Colors.ENDC)
    # Here you can add real install logic like os.system(app['install_cmd']) if you want
    time.sleep(1.5)
    slow_print(Colors.OKGREEN + f"✅ {app['name']} installed successfully!" + Colors.ENDC)
    input("\nPress Enter to continue...")

def main():
    apps = load_apps()
    while True:
        list_apps(apps)
        choice = input("\nEnter choice: ").strip().lower()
        if choice == 'q':
            print(Colors.OKGREEN + "👋 Thanks for using Terminal App Store. Bye!" + Colors.ENDC)
            break
        elif choice == 'a':
            add_new_app(apps)
        elif choice.startswith('i'):
            num_part = choice[1:]
            if num_part.isdigit():
                idx = int(num_part) - 1
                if 0 <= idx < len(apps):
                    install_app(apps[idx])
                else:
                    print(Colors.FAIL + "Invalid app number." + Colors.ENDC)
                    time.sleep(1)
            else:
                print(Colors.FAIL + "Invalid install command format. Use I<number>." + Colors.ENDC)
                time.sleep(1)
        else:
            print(Colors.FAIL + "Invalid choice, try again." + Colors.ENDC)
            time.sleep(1)

if __name__ == "__main__":
    main()
