# -*- coding: utf-8 -*-
# Import required libraries
import os
import json
import getpass
import colorama  # For Windows emoji support

# Initialize colorama
colorama.init()

# Constants
USERS_FILE = "users.json"  # File to store user credentials

def welcome_screen():
    """Display a welcome banner when the program starts"""
    print("Welcome To Password Manager!")
    print("|---------------------------|")
    print("|  Made By Bhavyansh Soni  |")
    print("|---------------------------|")

def load_users():
    """Load user credentials from the JSON file
    Returns:
        dict: Dictionary containing username-password pairs
    """
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    """Save user credentials to the JSON file
    Args:
        users (dict): Dictionary containing username-password pairs
    """
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def signup():
    """Handle new user registration
    Returns:
        str: Username if signup successful, None otherwise
    """
    users = load_users()
    username = input("Choose a username: ")
    if username in users:
        print("Username already exists!")
        return None
    password = getpass.getpass("Choose a password: ")  # Hide password input
    users[username] = password
    save_users(users)
    print("Signup successful!")
    return username

def login():
    """Handle user login
    Returns:
        str: Username if login successful, None otherwise
    """
    users = load_users()
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")  # Hide password input
    if username in users and users[username] == password:
        print("Login successful!")
        return username
    else:
        print("Invalid username or password.")
        return None

def get_password_file(username):
    """Generate filename for storing user's passwords
    Args:
        username (str): Username of the current user
    Returns:
        str: Filename for storing passwords
    """
    return f"passwords_{username}.json"

def load_passwords(username):
    """Load passwords for a specific user
    Args:
        username (str): Username of the current user
    Returns:
        dict: Dictionary containing stored passwords
    """
    file = get_password_file(username)
    if not os.path.exists(file):
        return {}
    with open(file, "r") as f:
        return json.load(f)

def save_passwords(username, passwords):
    """Save passwords for a specific user
    Args:
        username (str): Username of the current user
        passwords (dict): Dictionary containing passwords to save
    """
    file = get_password_file(username)
    with open(file, "w") as f:
        json.dump(passwords, f, indent=4)

def add_password(username):
    """Add a new password entry for the user
    Args:
        username (str): Username of the current user
    """
    title = input("Enter the title of the password: ")
    user = input("Enter the username/email: ")
    pwd = input("Enter the password: ")

    passwords = load_passwords(username)
    passwords[title] = {"username": user, "password": pwd}
    save_passwords(username, passwords)
    print(f"Password for '{title}' saved!")

def view_password(username):
    """View all stored passwords for the user
    Args:
        username (str): Username of the current user
    """
    passwords = load_passwords(username)
    if not passwords:
        print("No passwords saved yet.")
        return
    for title in passwords:
        print(f"\n🔐 {title}")
        print(f"   Username: {passwords[title]['username']}")
        print(f"   Password: {passwords[title]['password']}")

def delete_password(username):
    """Delete a stored password entry
    Args:
        username (str): Username of the current user
    """
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
    """Display and handle the main password management menu
    Args:
        username (str): Username of the current user
    """
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
    """Main program loop handling user authentication and menu navigation"""
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

# Start the program if this file is run directly
if __name__ == "__main__":
    main()
