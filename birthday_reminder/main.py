# Created by Bhavyansh Soni
# Birthday Reminder - Track and manage birthdays with cyberpunk style

import sys
import os
import time
import json
from datetime import datetime, timedelta

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.terminal_styles import *

class BirthdayReminder:
    def __init__(self):
        self.running = True
        self.birthdays = []
        self.notifications_enabled = True
        
    def add_birthday(self):
        """Add a new birthday"""
        clear_screen()
        print_banner("🎂 ADD BIRTHDAY 🎂")
        print()
        
        name = get_input("Enter name: ")
        if not name:
            print_error("Name cannot be empty!")
            time.sleep(1)
            return
        
        # Get birth date
        try:
            date_str = get_input("Enter birth date (YYYY-MM-DD): ")
            birth_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            
            # Calculate age
            today = datetime.now().date()
            age = today.year - birth_date.year
            if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
                age -= 1
            
            # Optional additional info
            relationship = get_input("Relationship (optional): ")
            gift_ideas = get_input("Gift ideas (optional): ")
            
            birthday_data = {
                "name": name,
                "birth_date": date_str,
                "age": age,
                "relationship": relationship,
                "gift_ideas": gift_ideas,
                "added_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            self.birthdays.append(birthday_data)
            print_success(f"Birthday added for {name}!")
            
        except ValueError:
            print_error("Invalid date format! Use YYYY-MM-DD")
        
        time.sleep(1)
    
    def view_birthdays(self):
        """View all birthdays"""
        clear_screen()
        print_banner("🎉 BIRTHDAY LIST 🎉")
        print()
        
        if not self.birthdays:
            print_warning("No birthdays recorded!")
            press_enter_to_continue()
            return
        
        # Sort by upcoming birthdays
        sorted_birthdays = sorted(self.birthdays, key=lambda x: self.get_next_birthday_date(x["birth_date"]))
        
        for i, birthday in enumerate(sorted_birthdays, 1):
            next_birthday = self.get_next_birthday_date(birthday["birth_date"])
            days_until = (next_birthday - datetime.now().date()).days
            
            print(f"{Colors.ACCENT}{i:2d}. {Colors.PRIMARY}{birthday['name']}{Colors.RESET}")
            print(f"     Age: {birthday['age']} | Next: {next_birthday}")
            if days_until == 0:
                print(f"     {Colors.WARNING}🎂 TODAY IS THEIR BIRTHDAY! 🎂{Colors.RESET}")
            elif days_until == 1:
                print(f"     {Colors.ERROR}🔔 Tomorrow! ({days_until} day){Colors.RESET}")
            elif days_until <= 7:
                print(f"     {Colors.WARNING}🔔 Soon! ({days_until} days){Colors.RESET}")
            else:
                print(f"     {Colors.GRAY}In {days_until} days{Colors.RESET}")
            
            if birthday["relationship"]:
                print(f"     Relationship: {birthday['relationship']}")
            if birthday["gift_ideas"]:
                print(f"     Gift ideas: {birthday['gift_ideas']}")
            print()
        
        press_enter_to_continue()
    
    def get_next_birthday_date(self, birth_date_str):
        """Calculate next birthday date"""
        birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
        today = datetime.now().date()
        
        # Get this year's birthday
        this_year_birthday = birth_date.replace(year=today.year)
        
        # If birthday has passed this year, use next year
        if this_year_birthday < today:
            return birth_date.replace(year=today.year + 1)
        else:
            return this_year_birthday
    
    def upcoming_birthdays(self):
        """Show upcoming birthdays within 30 days"""
        clear_screen()
        print_banner("📅 UPCOMING BIRTHDAYS 📅")
        print()
        
        if not self.birthdays:
            print_warning("No birthdays recorded!")
            press_enter_to_continue()
            return
        
        upcoming = []
        today = datetime.now().date()
        
        for birthday in self.birthdays:
            next_birthday = self.get_next_birthday_date(birthday["birth_date"])
            days_until = (next_birthday - today).days
            
            if days_until <= 30:
                upcoming.append((birthday, days_until, next_birthday))
        
        if not upcoming:
            print_info("No birthdays in the next 30 days!")
            press_enter_to_continue()
            return
        
        # Sort by days until birthday
        upcoming.sort(key=lambda x: x[1])
        
        for birthday, days_until, next_birthday in upcoming:
            if days_until == 0:
                print(f"{Colors.WARNING}🎂 TODAY: {Colors.PRIMARY}{birthday['name']}{Colors.RESET}")
            elif days_until == 1:
                print(f"{Colors.ERROR}🔔 TOMORROW: {Colors.PRIMARY}{birthday['name']}{Colors.RESET}")
            else:
                print(f"{Colors.ACCENT}{days_until} days: {Colors.PRIMARY}{birthday['name']} ({next_birthday}){Colors.RESET}")
        
        print()
        press_enter_to_continue()
    
    def birthday_statistics(self):
        """Show birthday statistics"""
        clear_screen()
        print_banner("📊 BIRTHDAY STATISTICS 📊")
        print()
        
        if not self.birthdays:
            print_warning("No birthdays recorded!")
            press_enter_to_continue()
            return
        
        total_birthdays = len(self.birthdays)
        slow_print(f"Total Birthdays: {total_birthdays}", 0.02, Colors.ACCENT)
        
        # Age statistics
        ages = [b["age"] for b in self.birthdays]
        avg_age = sum(ages) / len(ages)
        slow_print(f"Average Age: {avg_age:.1f} years", 0.02, Colors.ACCENT)
        slow_print(f"Youngest: {min(ages)} years", 0.02, Colors.ACCENT)
        slow_print(f"Oldest: {max(ages)} years", 0.02, Colors.ACCENT)
        
        # Month distribution
        print()
        slow_print("Birthdays by Month:", 0.02, Colors.PRIMARY)
        month_counts = {}
        for birthday in self.birthdays:
            month = datetime.strptime(birthday["birth_date"], "%Y-%m-%d").month
            month_name = datetime.strptime(str(month), "%m").strftime("%B")
            month_counts[month_name] = month_counts.get(month_name, 0) + 1
        
        for month, count in sorted(month_counts.items()):
            print(f"{Colors.SECONDARY}{month}: {Colors.WHITE}{count} birthdays{Colors.RESET}")
        
        print()
        press_enter_to_continue()
    
    def delete_birthday(self):
        """Delete a birthday entry"""
        clear_screen()
        print_banner("🗑️ DELETE BIRTHDAY 🗑️")
        print()
        
        if not self.birthdays:
            print_warning("No birthdays to delete!")
            time.sleep(1)
            return
        
        for i, birthday in enumerate(self.birthdays, 1):
            print(f"{Colors.ACCENT}{i:2d}. {Colors.PRIMARY}{birthday['name']}{Colors.RESET} ({birthday['birth_date']})")
        
        print()
        choice = get_input("Enter number to delete (or press Enter to cancel): ")
        
        if choice.isdigit():
            try:
                index = int(choice) - 1
                if 0 <= index < len(self.birthdays):
                    deleted_birthday = self.birthdays.pop(index)
                    print_success(f"Deleted birthday for {deleted_birthday['name']}")
                else:
                    print_error("Invalid selection!")
            except ValueError:
                print_error("Invalid input!")
        
        time.sleep(1)
    
    def main_menu(self):
        """Display main menu"""
        while self.running:
            clear_screen()
            
            # Birthday cake ASCII art
            cake_art = """
                  🕯️
                ████████
               ██🍓🍓🍓██
              ████████████
             ██🍎🍎🍎🍎██
            ████████████████
            """
            
            print_ascii_art(cake_art, Colors.WARNING)
            print_banner("🎂 BIRTHDAY REMINDER 🎂")
            print()
            slow_print("Never forget a special day again!", 0.02, Colors.PRIMARY)
            print()
            
            print_menu_item(1, "🎂 Add Birthday")
            print_menu_item(2, "🎉 View All Birthdays")
            print_menu_item(3, "📅 Upcoming Birthdays")
            print_menu_item(4, "📊 Statistics")
            print_menu_item(5, "🗑️ Delete Birthday")
            print_menu_item(6, "❌ Exit")
            
            print()
            choice = get_input("Enter your choice (1-6): ")
            
            if choice == '1':
                self.add_birthday()
            elif choice == '2':
                self.view_birthdays()
            elif choice == '3':
                self.upcoming_birthdays()
            elif choice == '4':
                self.birthday_statistics()
            elif choice == '5':
                self.delete_birthday()
            elif choice == '6':
                slow_print("Keep celebrating life! 🎉", 0.02, Colors.SECONDARY)
                self.running = False
            else:
                print_error("Invalid choice! Please select 1-6.")
                time.sleep(1)

def main():
    """Main function to run Birthday Reminder"""
    try:
        birthday_reminder = BirthdayReminder()
        birthday_reminder.main_menu()
    except KeyboardInterrupt:
        print()
        slow_print("Program interrupted by user.", 0.02, Colors.WARNING)
    except Exception as e:
        print_error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
