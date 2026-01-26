import random
import time
from colorama import Fore, Style, init
init(autoreset=True)

# ====== DATA ======
ghosts = {
    "Spirit":       ["Spirit Box", "EMF Level 5", "Ghost Writing"],
    "Deogen":       ["Spirit Box", "Ghost Writing", "D.O.T.S Projector"],
    "Demon":        ["Freezing Temps", "Ghost Writing", "Fingerprints"],
    "Jinn":         ["EMF Level 5", "Fingerprints", "Freezing Temps"],
    "Revenant":     ["Ghost Writing", "Ghost Orbs", "Freezing Temps"],
    "Banshee":      ["Ghost Orbs", "Fingerprints", "D.O.T.S Projector"],
    "Oni":          ["EMF Level 5", "Freezing Temps", "D.O.T.S Projector"],
    "Yokai":        ["Spirit Box", "Ghost Orbs", "D.O.T.S Projector"],
    "Hantu":        ["Freezing Temps", "Ghost Writing", "Fingerprints"],
    "Poltergeist":  ["Spirit Box", "Ghost Writing", "Fingerprints"],
    "Mimic":        ["Spirit Box", "EMF Level 5", "Ghost Writing", "Freezing Temps"]  # Mimic: all four evidences, tricky!
}

tools = {
    "EMF Reader": "EMF Level 5",
    "Spirit Box": "Spirit Box",
    "Thermometer": "Freezing Temps",
    "UV Light": "Fingerprints",
    "Ghost Writing Book": "Ghost Writing",
    "D.O.T.S Projector": "D.O.T.S Projector",
    "Video Camera": "Ghost Orbs",
    "Salt": None,
    "Crucifix": None
}

maps = {
    "Small House": {
        "Living Room": {"north": "Kitchen", "east": "Bathroom"},
        "Kitchen": {"south": "Living Room", "east": "Garage"},
        "Bathroom": {"west": "Living Room"},
        "Garage": {"west": "Kitchen", "north": "Basement"},
        "Basement": {"south": "Garage"}
    },
    "Apartment": {
        "Lobby": {"north": "Hallway"},
        "Hallway": {"south": "Lobby", "east": "Bedroom", "west": "Bathroom"},
        "Bedroom": {"west": "Hallway"},
        "Bathroom": {"east": "Hallway"},
    }
}

tasks_list = [
    ("Check EMF Reader in Kitchen", "EMF Level 5", "Kitchen"),
    ("Place Salt at Bathroom Door", None, "Bathroom"),
    ("Use Thermometer in Basement", "Freezing Temps", "Basement"),
    ("Use Spirit Box in Garage", "Spirit Box", "Garage"),
    ("Look for Fingerprints with UV Light in Living Room", "Fingerprints", "Living Room"),
    ("Set up Video Camera in Garage", "Ghost Orbs", "Garage"),
]

# ===== GLOBALS =====
money = 0
current_room = None
tasks = []
completed_tasks = []
ghost_room = None
ghost_name = None
ghost_evidence = []
difficulty = "Medium"
tools_selected = []
current_map = None

# ===== COLORS & EMOJIS HELPERS =====
def print_red(text): print(Fore.RED + text + Style.RESET_ALL)
def print_green(text): print(Fore.GREEN + text + Style.RESET_ALL)
def print_yellow(text): print(Fore.YELLOW + text + Style.RESET_ALL)
def print_cyan(text): print(Fore.CYAN + text + Style.RESET_ALL)

# ===== UTILS =====
def sleep_sec(sec=1.5):
    time.sleep(sec)

def clear_screen():
    print("\n" * 30)

# ===== TITLE =====
def title_banner():
    clear_screen()
    print_red("""
██████╗ ██╗  ██╗ █████╗ ███████╗███╗   ███╗ ██████╗ ██████╗ ██╗ ██████╗ ██████╗ ██╗ █████╗ 
██╔══██╗██║  ██║██╔══██╗██╔════╝████╗ ████║██╔═══██╗██╔══██╗██║██╔═══██╗██╔══██╗██║██╔══██╗
██████╔╝███████║███████║███████╗██╔████╔██║██║   ██║██████╔╝██║██║   ██║██████╔╝██║███████║
██╔═══╝ ██╔══██║██╔══██║╚════██║██║╚██╔╝██║██║   ██║██╔═══╝ ██║██║   ██║██╔═══╝ ██║██╔══██║
██║     ██║  ██║██║  ██║███████║██║ ╚═╝ ██║╚██████╔╝██║     ██║╚██████╔╝██║     ██║██║  ██║
╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚═╝     ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝
""")
    print_cyan("👻 Welcome to PHASMOPHOBIA: TERMINAL PRO EDITION 👻\n")
    sleep_sec(1)

# ===== WELCOME & DIFFICULTY SELECT =====
def welcome():
    global difficulty
    print_yellow("Choose your difficulty level:")
    print("1. Easy  (3 evidences shown, 3 tools)")
    print("2. Medium(3 evidences shown, 4 tools)")
    print("3. Hard  (2 evidences shown, 4 tools)")
    while True:
        choice = input("Enter choice (1-3): ").strip()
        if choice == "1":
            difficulty = "Easy"
            break
        elif choice == "2":
            difficulty = "Medium"
            break
        elif choice == "3":
            difficulty = "Hard"
            break
        else:
            print_red("Invalid choice. Try again.")
    print_green(f"Difficulty set to: {difficulty}")
    sleep_sec(1)

def map_select():
    global current_map, current_room
    print_yellow("\nChoose a map to investigate:")
    for i, m in enumerate(maps.keys(), 1):
        print(f"{i}. {m}")
    while True:
        try:
            choice = int(input("Enter map number: "))
            if 1 <= choice <= len(maps):
                current_map = list(maps.keys())[choice-1]
                current_room = list(maps[current_map].keys())[0]
                print_green(f"Map selected: {current_map}")
                sleep_sec(1)
                break
            else:
                print_red("Invalid choice.")
        except:
            print_red("Please enter a number.")

def assign_ghost():
    global ghost_name, ghost_room, ghost_evidence
    ghost_name = random.choice(list(ghosts.keys()))
    ghost_evidence = ghosts[ghost_name]
    ghost_room = random.choice(list(maps[current_map].keys()))

def assign_tasks():
    global tasks, completed_tasks
    tasks = random.sample(tasks_list, 3)
    completed_tasks = []

def show_status():
    global money, current_room, tasks, completed_tasks
    print_cyan(f"\n💰 Money: ₹{money}")
    print_cyan(f"📍 Current Room: {current_room}")
    print_cyan(f"📋 Tasks Remaining: {len(tasks)-len(completed_tasks)}")
    for i, t in enumerate(tasks):
        status = "✅ COMPLETED" if t in completed_tasks else "❌ PENDING"
        print(f"  {i+1}. {t[0]} [{status}]")

def move_room():
    global current_room
    exits = maps[current_map][current_room]
    print_yellow("\nAvailable exits:")
    for d, r in exits.items():
        print(f"- {d.title()} -> {r}")
    choice = input("Where do you want to go? (north/south/east/west): ").lower()
    if choice in exits:
        current_room = exits[choice]
        print_green(f"You moved to {current_room} {chr(128101)}")
    else:
        print_red("Invalid direction!")

def pick_tools():
    global difficulty
    max_tools = 5 if difficulty in ["Easy", "Medium"] else 4
    print_yellow(f"\nSelect up to {max_tools} tools to carry:")
    for i, t in enumerate(tools.keys(), 1):
        print(f"{i}. {t}")
    chosen = []
    while len(chosen) < max_tools:
        try:
            choice = int(input(f"Pick tool {len(chosen)+1} (1-{len(tools)}): "))
            tool = list(tools.keys())[choice-1]
            if tool not in chosen:
                chosen.append(tool)
            else:
                print_red("Already selected that tool.")
        except:
            print_red("Invalid input.")
    print_green(f"Tools selected: {', '.join(chosen)}")
    sleep_sec(1)
    return chosen


def open_journal():
    print_cyan("\n📖 Ghost Journal:")
    for g, ev in ghosts.items():
        print(f"- {g}: {', '.join(ev)}")
    sleep_sec(1)
    print()

def provide_evidence(tools_selected):
    global ghost_evidence, current_room, ghost_room, difficulty
    print_yellow("\n🔍 Investigating...\n")
    time.sleep(1)
    # Determine how many evidences to show based on difficulty
    ev_to_show = 3 if difficulty in ["Easy", "Medium"] else 2
    evidences_shown = 0

    for tool in tools_selected:
        ev_detected = tools[tool]
        if current_room == ghost_room and ev_detected in ghost_evidence and evidences_shown < ev_to_show:
            print_green(f"✅ {tool}: Detected '{ev_detected}' {chr(128373)}")
            evidences_shown += 1
        elif ev_detected is None:
            print_yellow(f"🔹 {tool}: Used, but no direct evidence.")
        else:
            print_red(f"❌ {tool}: No evidence detected here.")
        sleep_sec(1)
    if evidences_shown == 0:
        print_red("No evidence found in this room.")
    print()

def check_task_completion():
    global completed_tasks, money, current_room
    completed_any = False
    for task in tasks:
        if task in completed_tasks:
            continue
        task_name, ev_needed, task_room = task
        if current_room == task_room:
            completed_tasks.append(task)
            reward = {"Easy": 30, "Medium": 50, "Hard": 70}[difficulty]
            money += reward
            print_green(f"✅ Task completed: {task_name}! You earned ₹{reward} {chr(128176)}")
            completed_any = True
    if not completed_any:
        print_red("No task to complete here.")
    sleep_sec(1)

def guess_ghost():
    global money, ghost_name, difficulty
    print_cyan("\n🎯 Ghosts List:")
    for g in ghosts.keys():
        print(f"- {g}")
    guess = input("\nYour final guess who the ghost is: ").strip().title()
    print_yellow("\nChecking your guess...\n")
    time.sleep(2)
    if guess == ghost_name:
        reward = {"Easy": 100, "Medium": 150, "Hard": 250}[difficulty]
        money += reward
        print_green(f"🎉 Correct! The ghost was {ghost_name}. You WIN! You earned ₹{reward} 🎉")
        return True
    else:
        penalty = {"Easy": 30, "Medium": 50, "Hard": 80}[difficulty]
        money -= penalty
        print_red(f"💀 WRONG! The ghost was {ghost_name}. You lose! You lost ₹{penalty} 💀")
        return False

def play_again():
    while True:
        again = input("\nDo you want to play again? (yes/no): ").strip().lower()
        if again in ["yes", "y"]:
            return True
        elif again in ["no", "n"]:
            print_yellow("Thanks for playing! Goodbye 👻")
            return False
        else:
            print_red("Please answer yes or no.")

def main_game():
    global money, current_room, tasks, completed_tasks, ghost_name, ghost_room, ghost_evidence, tools_selected
    title_banner()
    welcome()
    map_select()
    assign_ghost()
    assign_tasks()
    tools_selected = pick_tools()
    
    while True:
        show_status()
        print_yellow("\nOptions:")
        print("1. Move Rooms 🧭")
        print("2. Investigate with Tools 🛠️")
        print("3. Open Ghost Journal 📖")
        print("4. Complete Task Check ✅")
        print("5. Guess the Ghost 👻")
        print("6. Quit Game ❌")
        choice = input("Choose an action (1-6): ").strip()

        if choice == "1":
            move_room()
        elif choice == "2":
            provide_evidence(tools_selected)
        elif choice == "3":
            open_journal()
        elif choice == "4":
            check_task_completion()
        elif choice == "5":
            if guess_ghost():
                break
        elif choice == "6":
            print_yellow("Exiting game. Thanks for playing! 👻")
            break
        else:
            print_red("Invalid choice, try again.")
        sleep_sec(0.5)

    if play_again():
        main_game()
    else:
        print_green("\nGame Over. Your final money balance: ₹" + str(money))
        print_cyan("See you next time! 👻")

if __name__ == "__main__":
    main_game()
