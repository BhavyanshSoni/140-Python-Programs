import os
import json
import getpass

USERS_FILE = "users.json"

def welcome_screen():
    print("Welcome To Password Manager!")
    print("|---------------------------|")
    print("|  Made By Bhavyansh Soni  |")
    print("|---------------------------|")

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def signup():
    users = load_users()
    username = input("Choose a username: ")
    if username in users:
        print("Username already exists!")
        return None
    password = getpass.getpass("Choose a password: ")
    users[username] = password
    save_users(users)
    print("Signup successful!")
    return username

def login():
    users = load_users()
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    if username in users and users[username] == password:
        print("Login successful!")
        return username
    else:
        print("Invalid username or password.")
        return None

def get_password_file(username):
    return f"passwords_{username}.json"

def load_passwords(username):
    file = get_password_file(username)
    if not os.path.exists(file):
        return {}
    with open(file, "r") as f:
        return json.load(f)

def save_passwords(username, passwords):
    file = get_password_file(username)
    with open(file, "w") as f:
        json.dump(passwords, f, indent=4)

def add_password(username):
    title = input("Enter the title of the password: ")
    user = input("Enter the username/email: ")
    pwd = input("Enter the password: ")

    passwords = load_passwords(username)
    passwords[title] = {"username": user, "password": pwd}
    save_passwords(username, passwords)
    print(f"Password for '{title}' saved!")

def view_password(username):
    passwords = load_passwords(username)
    if not passwords:
        print("No passwords saved yet.")
        return
    for title in passwords:
        print(f"\n🔐 {title}")
        print(f"   Username: {passwords[title]['username']}")
        print(f"   Password: {passwords[title]['password']}")

def delete_password(username):
    passwords = load_passwords(username)
    if not passwords:
        print("No passwords to delete.")
        return
    print("Saved Entries:")
    for title in passwords:
        print(f"→ {title}")
    to_delete = input("Enter the title to delete: ")
    if to_delete in passwords:
        del passwords[to_delete]
        save_passwords(username, passwords)
        print(f"Deleted '{to_delete}'")
    else:
        print("Title not found.")

def password_menu(username):
    while True:
        print(f"\n📂 Welcome, {username}")
        print("1. Add Password")
        print("2. View Passwords")
        print("3. Delete Password")
        print("4. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_password(username)
        elif choice == "2":
            view_password(username)
        elif choice == "3":
            delete_password(username)
        elif choice == "4":
            print("Logging out...")
            break
        else:
            print("Invalid choice!")

def main():
    welcome_screen()
    while True:
        print("\n1. Signup")
        print("2. Login")
        print("3. Exit")
        option = input("Choose an option: ")

        if option == "1":
            username = signup()
            if username:
                password_menu(username)
        elif option == "2":
            username = login()
            if username:
                password_menu(username)
        elif option == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid input!")

main()
