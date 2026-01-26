import plyer
import time
import json
import os

REMINDER_FILE = "reminders.json"

def welcome_screen():
    print("Welcome To STUDY ASSISTANT\n---> Made By Bhavyansh Soni")
    print("You Can Make Your Study Easier By Using This\n")

def Menu():
    print("CHOOSE ONE OF THE FOLLOWING \n\n")
    print("┌──────────────────────────────┐")
    print("│        Study Assistant       │")
    print("├──────────────────────────────┤")
    print("| [1] Study                    |")
    print("|──────────────────────────────|")
    print("│ [2] Set Reminders            │")
    print("|──────────────────────────────|")
    print("| [3] View Reminders           │")
    print("|──────────────────────────────|")
    print("| [4] Edit Reminders           │")
    print("|──────────────────────────────|")
    print("| [5] Delete Reminders         │")
    print("|──────────────────────────────|")
    print("| [6] QUIT                     |")
    print("└──────────────────────────────┘")

def load_reminders():
    if not os.path.exists(REMINDER_FILE):
        return []
    with open(REMINDER_FILE, "r") as f:
        return json.load(f)

def save_reminders(reminders):
    with open(REMINDER_FILE, "w") as f:
        json.dump(reminders, f, indent=4)

def study_subjects():
    print("You Chose To Study...\n")
    try:
        subjects = int(input("Enter How Many Subjects You Want To Study: "))
        total_subjects = []
        for i in range(subjects):
            subject_name = input(f"Enter Name Of Subject {i+1}: ")
            total_subjects.append(subject_name) 
        each_sub_time = int(input(f"Enter How Many Hours You Need To Study {subjects} Subjects: "))

        if each_sub_time > 16:
            print("You Can't Study More Than 16 HOURS")
        else:
            total_time = each_sub_time // subjects
            print(f"You Need To Study {total_time} Hours In Each SUBJECT!\n")
            for item in total_subjects:
                print(f"Starting To Study '{item}' For {total_time} Hour\n")
                time.sleep(total_time * 3600)
    except ValueError:
        print("Invalid! Input! ❌")

def set_reminders():
    print("You Chose To Set Reminders")
    reminder_subject_name = input("Enter Name Of Subject You Want To Set Reminder For: ")
    description = input("Enter (Description/Message) Of The Reminder: ")
    try:
        reminder_hour = int(input("Enter At Which Hour You Want The Reminder Reminds You (give in 24 format): "))
        reminder_minute = int(input("Enter At Which Minute You Want The Reminder Reminds You (give in 24 format): "))
    except ValueError:
        print("Invalid Hour or Minute!")
        return

    if reminder_hour > 23 or reminder_minute > 59 or reminder_hour < 0 or reminder_minute < 0:
        print("Invalid Hour or Minute!")
        return

    reminders = load_reminders()
    reminders.append({
        "subject": reminder_subject_name,
        "description": description,
        "hour": reminder_hour,
        "minute": reminder_minute
    })
    save_reminders(reminders)
    print(f"The Reminder Has Been Set. It Will Remind You On {reminder_hour:02d}:{reminder_minute:02d}")

def view_reminders():
    reminders = load_reminders()
    if not reminders:
        print("No reminders set.")
        return
    print("\nYour Reminders:")
    for idx, rem in enumerate(reminders, 1):
        print(f"[{idx}] {rem['subject']} at {rem['hour']:02d}:{rem['minute']:02d} - {rem['description']}")

def edit_reminders():
    reminders = load_reminders()
    if not reminders:
        print("No reminders to edit.")
        return
    view_reminders()
    try:
        idx = int(input("Enter the number of the reminder to edit: ")) - 1
        if idx < 0 or idx >= len(reminders):
            print("Invalid selection.")
            return
        reminder_subject_name = input("Enter new subject name (leave blank to keep current): ")
        description = input("Enter new description (leave blank to keep current): ")
        hour_input = input("Enter new hour (leave blank to keep current): ")
        minute_input = input("Enter new minute (leave blank to keep current): ")

        if reminder_subject_name:
            reminders[idx]['subject'] = reminder_subject_name
        if description:
            reminders[idx]['description'] = description
        if hour_input:
            try:
                hour = int(hour_input)
                if 0 <= hour <= 23:
                    reminders[idx]['hour'] = hour
                else:
                    print("Invalid hour. Keeping previous value.")
            except ValueError:
                print("Invalid hour input. Keeping previous value.")
        if minute_input:
            try:
                minute = int(minute_input)
                if 0 <= minute <= 59:
                    reminders[idx]['minute'] = minute
                else:
                    print("Invalid minute. Keeping previous value.")
            except ValueError:
                print("Invalid minute input. Keeping previous value.")

        save_reminders(reminders)
        print("Reminder updated.")
    except ValueError:
        print("Invalid input.")

def delete_reminders():
    reminders = load_reminders()
    if not reminders:
        print("No reminders to delete.")
        return
    view_reminders()
    try:
        idx = int(input("Enter the number of the reminder to delete: ")) - 1
        if idx < 0 or idx >= len(reminders):
            print("Invalid selection.")
            return
        del reminders[idx]
        save_reminders(reminders)
        print("Reminder deleted.")
    except ValueError:
        print("Invalid input.")

def check_and_notify_reminders():
    reminders = load_reminders()
    current_hour = int(time.strftime("%H"))
    current_minute = int(time.strftime("%M"))
    for rem in reminders:
        if rem['hour'] == current_hour and rem['minute'] == current_minute:
            plyer.notification.notify(
                title=f"Go And Study {rem['subject']}",
                message=rem['description'],
                timeout=5
            )

def main():
    welcome_screen()
    while True:
        Menu()
        choice = input("Enter your choice (1-6): ")
        if choice == "1":
            study_subjects()
        elif choice == "2":
            set_reminders()
        elif choice == "3":
            view_reminders()
        elif choice == "4":
            edit_reminders()
        elif choice == "5":
            delete_reminders()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
        # Check for reminders after each action
        check_and_notify_reminders()
        time.sleep(1)

if __name__ == "__main__":
    main()