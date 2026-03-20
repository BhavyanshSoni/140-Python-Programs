from time import sleep
import os
from colorama import Fore, init

init()

"""Performs operation s with parameters: txt, d."""
def s(txt, d=0.04):
    for i in txt:
        print(i, end='',flush=True)
        sleep(d)
    print()

"""Performs operation sign_up. Note: This function has high complexity."""
def sign_up():
    global verified, username
    # Fix 1: auto-create Accounts folder so signup/login doesn't crash
    os.makedirs("Accounts", exist_ok=True)
    while True:
        s(Fore.CYAN + "Do you want to Sign-up or Login!")
        s(Fore.LIGHTBLUE_EX + "1. Sign-up!")
        s(Fore.LIGHTBLUE_EX + "2. Login!")

        try:
            account_make_choice = int(input(Fore.LIGHTWHITE_EX + "Enter Choice(1/2):-  "))
            if account_make_choice == 1:
                s(Fore.LIGHTYELLOW_EX + "\nYou Chose to Sign-up")
                username = input(Fore.LIGHTMAGENTA_EX + "\nEnter Your Username:- ")
                pin = input(Fore.LIGHTRED_EX + "\nEnter Pin (It can be Alphabets, Numbers or Symbols):- ")

                # Fix 2: check in local Accounts folder (no hard-coded path)
                if os.path.exists(f"Accounts/{username}.txt"):
                    s("The Pin and Username is already used.Try Something Different")
                    s(Fore.YELLOW + "\nPlease try again...\n")
                    verified = False
                    continue  # Return to start of function

                with open(f"Accounts/{username}.txt", "w") as f:
                    money = 0
                    # Fix 3: always store Name, Pin, Money = 0 on creation
                    f.write(f"Name: {username}\nPin: {pin}\nMoney: {money}")
                s(Fore.LIGHTGREEN_EX + "\nAccount Created ✅")
                verified = True
                break  # Exit loop on success

            elif account_make_choice == 2:
                s(Fore.LIGHTYELLOW_EX + "\nYou Chose to Login")
                username = input(Fore.LIGHTMAGENTA_EX + "\nEnter Your Username:- ")
                pin = input(Fore.LIGHTRED_EX + "\nEnter Your Pin:- ")

                # Fix 4: login against local Accounts folder and correct condition
                if not os.path.exists(f"Accounts/{username}.txt"):
                    s(Fore.RED + "No Account is Active or Created With this Username and Pin. Sign-up First!")
                    s(Fore.YELLOW + "\nPlease try again...\n")
                    verified = False
                    continue  # Return to start of function

                with open(f"Accounts/{username}.txt") as f:
                    details = f.read()
                    pin_check = f"Pin: {pin}"
                    name_check = f"Name: {username}"
                    # old bug: `if pin_check and name_check in details:` always true if pin_check is non-empty
                    if (pin_check in details) and (name_check in details):
                        s(Fore.GREEN + f"\nVerified {username}")
                        verified = True
                        break  # Exit loop on successful login
                    else:
                        s(Fore.RED + "Wrong Pin or Username")
                        s(Fore.YELLOW + "\nPlease try again...\n")
                        verified = False
                        continue  # Return to start of function
            else:
                s(Fore.RED + "Invalid Number Of Choice.")
                s(Fore.YELLOW + "\nPlease try again...\n")
                verified = False
                continue  # Return to start of function

        except ValueError:
            s(Fore.RED + "Invalid Number of Choice!")
            s(Fore.YELLOW + "\nPlease try again...\n")
            verified = False
            continue  # Return to start of function

"""Performs operation deposit. Note: This function has high complexity."""
def deposit():
    s("So Now let's Deposit Money")
    while True:
        try:
            add_money = int(input("Enter the amount you want to deposit:- "))
        except ValueError:
            s(Fore.RED + "Invalid Amount!")
            s(Fore.YELLOW + "\nPlease try again...")
            continue

        if add_money <= 0:
            s(Fore.RED + "Invalid Amount!")
            s(Fore.YELLOW + "\nPlease try again...")
            continue

        # Fix 5: actually update stored Money instead of searching for exact match
        with open(f"Accounts/{username}.txt", "r") as f:
            details_lines = f.read().splitlines()

        current_money = 0
        for line in details_lines:
            if line.startswith("Money:"):
                try:
                    current_money = int(line.split(":", 1)[1].strip())
                except ValueError:
                    current_money = 0
                break

        new_money = current_money + add_money
        new_lines = []
        replaced = False
        for line in details_lines:
            if line.startswith("Money:"):
                new_lines.append(f"Money: {new_money}")
                replaced = True
            else:
                new_lines.append(line)
        if not replaced:
            new_lines.append(f"Money: {new_money}")

        with open(f"Accounts/{username}.txt", "w") as f:
            f.write("\n".join(new_lines))

        s(Fore.GREEN + "Money Deposited Successfully")
        break

"""Performs operation debit. Note: This function has high complexity."""
def debit():
    s("So Now let's Debit Money")
    while True:
        try:
            take_money = int(input("Enter the amount you want to debit:- "))
        except ValueError:
            s(Fore.RED + "Invalid Amount!")
            s(Fore.YELLOW + "\nPlease try again...")
            continue

        if take_money <= 0:
            s(Fore.RED + "Invalid Amount!")
            s(Fore.YELLOW + "\nPlease try again...")
            continue

        # Fix 6: subtract from current Money (with insufficient funds check)
        with open(f"Accounts/{username}.txt", "r") as f:
            details_lines = f.read().splitlines()

        current_money = 0
        for line in details_lines:
            if line.startswith("Money:"):
                try:
                    current_money = int(line.split(":", 1)[1].strip())
                except ValueError:
                    current_money = 0
                break

        if take_money > current_money:
            s(Fore.RED + "Insufficient Funds")
            s(Fore.CYAN + f"Your Current Balance: {current_money}")
            s("What do you want to do now!")
            s("1. Debit Money")
            s("2. Deposit Money")
            try:
                choice = int(input("Enter Choice (1/2):- "))
                if choice == 1:
                    continue  # Try debit again
                elif choice == 2:
                    deposit()  # Go to deposit
                    break  # Exit debit after depositing
                else:
                    s(Fore.RED + "Invalid Choice!")
                    s(Fore.YELLOW + "\nPlease try again...")
                    continue
            except ValueError:
                s(Fore.RED + "Invalid Choice!")
                s(Fore.YELLOW + "\nPlease try again...")
                continue

        new_money = current_money - take_money
        new_lines = []
        replaced = False
        for line in details_lines:
            if line.startswith("Money:"):
                new_lines.append(f"Money: {new_money}")
                replaced = True
            else:
                new_lines.append(line)
        if not replaced:
            new_lines.append(f"Money: {new_money}")

        with open(f"Accounts/{username}.txt", "w") as f:
            f.write("\n".join(new_lines))

        s(Fore.GREEN + "Money Debited Successfully")
        break

"""Performs operation change_pin."""
def change_pin():
    s("Now Let's Change your Pin!")
    

"""Performs operation change_username."""
def change_username():
    pass

"""Performs operation main. Note: This function has high complexity."""
def main():
    if verified == True:
        while True:
            s("What do you want to do now!")
            s("1. Deposit Money")
            s("2. Debit Money")
            s("3. Change Pin")
            s("4. Change Username")
            s("5. Exit!")

            try:
                action_choice = int(input("Enter Choice (1/2/3/4/5):- "))
                if action_choice == 1:
                    deposit()
                elif action_choice == 2:
                    debit()
                elif action_choice == 3:
                    change_pin()
                elif action_choice == 3:
                    change_username()
                else:
                    s("\nThanks For Using This Program")
                    s("GoodBye...")
                    break
            except:
                s(Fore.RED + "Invalid Choice!")
                s(Fore.YELLOW + "\nPlesae try again...")
                continue
    else:
        s(Fore.RED + "You are not verified. Please sign-up first!")

sign_up()
main()
