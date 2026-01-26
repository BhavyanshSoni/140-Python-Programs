from nt import execv
from time import sleep
import os
from colorama import Fore, Style, init

init()

def slow_print(text, delay=0.05):
    for char in text:
        print(char, end = '', flush=True)
        sleep(delay)
    print()

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_welcome():
        """Display welcome screen with animation"""
        clear_screen()
        banner = """
╔═══════════════════════════════════════╗
║         The TV SHOW                   ║
║         By: Bhavyansh Soni            ║
╚═══════════════════════════════════════╝
        """
        for line in banner.split('\n'):
            slow_print(Fore.CYAN + line + Style.RESET_ALL)
        sleep(1)

def add_show():
    slow_print("You Chose To Add Show!")
    try:
        channel = int(input("On Which Channel You Want To Add Your Show? (1-5)>> "))
        if channel < 1 or channel > 5:
            slow_print("❌ Channel number must be between 1 and 5!")
            return
        show = input("What To Display? >> ")
        with open(f"{channel}.txt", "w") as f:
            f.write(show)
        slow_print(f"✅ Show successfully added to channel {channel}!")
    except ValueError:
        slow_print("❌ Invalid Channel Number!")

def remove_show():
    """Remove a show from a channel"""
    slow_print("You Chose To Remove Show!")
    try:
        channel = int(input("From Which Channel You Want To Remove The Show? (1-5)>> "))
        if channel < 1 or channel > 5:
            slow_print("❌ Channel number must be between 1 and 5!")
            return
        
        filename = f"{channel}.txt"
        if os.path.exists(filename):
            os.remove(filename)
            slow_print(f"✅ Show removed from channel {channel}!")
        else:
            slow_print(f"❌ No show found on channel {channel}!")
    except ValueError:
        slow_print("❌ Invalid Channel Number!")

def display_shows():
    """Display all shows from all channels"""
    slow_print("📺 Current Shows:")
    print()
    for channel in range(1, 6):
        filename = f"{channel}.txt"
        if os.path.exists(filename):
            try:
                with open(filename, "r") as f:
                    show = f.read().strip()
                slow_print(f"{Fore.GREEN}Channel {channel}: {show}{Style.RESET_ALL}")
            except:
                slow_print(f"{Fore.RED}Error reading channel {channel}{Style.RESET_ALL}")
        else:
            slow_print(f"{Fore.YELLOW}Channel {channel}: No show{Style.RESET_ALL}")
    print()

def menu():
    slow_print("What You Want To Do: ")
    slow_print("1. Add Show!")
    slow_print("2. Remove Show!")
    slow_print("3. Display Show!")
    slow_print("4. Exit!")
    try:
        action = int(input("(1-4) >> "))
        if action < 1 or action > 4:
            slow_print("❌ Please choose a number between 1 and 4!")
            return None
        return action
    except ValueError:
        slow_print("❌ Invalid Action!")
        return None

def main():
    display_welcome()
    while True:
        action = menu()
        if action is None:
            continue
            
        if action == 1:
            add_show()
        elif action == 2:
            remove_show()
        elif action == 3:
            display_shows()
        elif action == 4:
            slow_print("👋 Thank you for using The TV SHOW!")
            break
        
        sleep(1)
        clear_screen()

if __name__ == "__main__":
    main()