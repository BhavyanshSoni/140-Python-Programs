from random import choice
import time
from colorama import Fore, Style, init

# The Welcome TEXT
print("Welcome To The Tournament Of Death 💀☠!")
print("In This Tournament You Have To Choose The Correct Gate To WIN The Tournament. Or You Will Be Dead ☠")
print("You will have 3 Lives!")
print("Best Of Luck!")

# Variables
Lives = 3
Gates = {
    "Gate 1":"safe",
    "Gate 2":"not safe",
    "Gate 3":"safe",
}


try:
    while Lives > 0:
        # Randomize gates' safety
        safe_gate = choice(list(Gates.keys()))
        init(autoreset=True)

        for gate in Gates:
            Gates[gate] = "not safe"
            print(Fore.CYAN + f"{gate}: " + (Fore.GREEN + "SAFE" if Gates[gate] == "safe" else Fore.RED + "NOT SAFE"))
        time.sleep(1)
        print(Fore.YELLOW + "\nShuffling the gates...")
        time.sleep(1)
        Gates[safe_gate] = "safe"

        print("\nChoose a gate:")
        for gate in Gates:
            print(gate)
        try:
            user_choice = input("Enter your gate (e.g., Gate 1): ").strip().title()
        except (EOFError, KeyboardInterrupt):
            print("\nInput interrupted. Exiting game.")
            break

        if user_choice in Gates:
            if Gates[user_choice] == "safe":
                print("You chose the correct gate! You survived this round.")
            else:
                Lives -= 1
                print(f"Wrong gate! {Fore.RED}You lost a life. Lives left: {Lives}{Style.RESET_ALL}")
        else:
            print("Invalid gate. Please choose a valid gate.")

        if Lives == 0:
            print("You are" + Fore.RED + " dead ☠." + Fore.RED + " Game Over!")
            break
except Exception as e:
    print(Fore.RED + f"An unexpected error occurred: {e}" + Style.RESET_ALL)
    print(Fore.RED + "No gate was safe. You are dead ☠. Game Over!" + Style.RESET_ALL)
    # Ensure at least one gate is safe before exiting
    if not any(status == "safe" for status in Gates.values()):
        print(Fore.RED + "No gate was safe. You are dead ☠. Game Over!" + Style.RESET_ALL)
    exit()