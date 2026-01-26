import datetime
import os

def new_entry():
    date = datetime.date.today().isoformat()
    mood = input("Enter your mood (Happy/Sad/Angry/Neutral): ")
    note = input("Write your journal:\n")

    file_name = f"{date}.txt"
    with open(file_name, "a", encoding="utf-8") as f:
        f.write(f"[{mood.upper()}]\n{note}\n\n")

    print(f"✔️ Entry saved to {file_name}")

def view_entries():
    files = [f for f in os.listdir() if f.endswith(".txt")]
    for i, f in enumerate(files):
        print(f"{i+1}. {f}")
    
    choice = int(input("Choose a file number to view: ")) - 1
    with open(files[choice], "r", encoding="utf-8") as f:
        print("\n--- Journal Entry ---\n")
        print(f.read())

while True:
    print("\n[Smart Journal]")
    print("1. New Entry\n2. View Past Entries\n3. Exit")
    choice = input("> ")

    if choice == "1":
        new_entry()
    elif choice == "2":
        view_entries()
    elif choice == "3":
        break
    else:
        print("Invalid choice.")
