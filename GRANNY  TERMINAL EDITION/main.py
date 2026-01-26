import random
import time
import threading
from colorama import Fore, Style, init
init(autoreset=True)

# ================= COLORS ====================
def print_red(text): print(Fore.RED + text + Style.RESET_ALL)
def print_green(text): print(Fore.GREEN + text + Style.RESET_ALL)
def print_yellow(text): print(Fore.YELLOW + text + Style.RESET_ALL)
def print_cyan(text): print(Fore.CYAN + text + Style.RESET_ALL)

def sleep(sec=1.5):
    time.sleep(sec)

# ================= GAME DATA =================
rooms = ["Bedroom", "Bathroom", "Kitchen", "Garage", "Basement", "Main Hall", "Shed", "Security Room", "Boat Room"]
items_pool = ["Cutting Pliers", "Door Key", "Crowbar", "Boat Steering Wheel", "Gasoline", "Padlock Key", "Boat Key", "Helicopter Manual", "Helicopter Key"]
escape_routes = {
    "Main Door": ["Door Key", "Cutting Pliers", "Padlock Key"],
    "Boat": ["Boat Steering Wheel", "Gasoline", "Cutting Pliers", "Boat Key"],
    "Helicopter": ["Gasoline", "Crowbar", "Padlock Key", "Helicopter Manual", "Helicopter Key"]
}

game_state = {
    "difficulty": "Normal",
    "day": 1,
    "max_days": 5,
    "inventory": [],
    "item_locations": {},
    "player_room": "Bedroom",
    "granny_room": None,
    "grandpa_room": None,
    "escape_route": None,
    "escaped": False
}

# ================ INIT FUNCTIONS =================
def intro():
    print_red("""
   ____                     _              ____ _               _             
  / ___|_ __ __ _ _ __ ___ (_)_ __   __ _ |  _ \ | __ _ _   _  | | ___   __ _ 
 | |  _| '__/ _` | '_ ` _ \| | '_ \ / _` || | | || '__| | | | | |/ _ \ / _` |
 | |_| | | | (_| | | | | | | | | | | (_| || |_| || |  | |_| | | | (_) | (_| |
  \____|_|  \__,_|_| |_| |_|_|_| |_|\__, ||____/ |_|   \__, | |_|\___/ \__, |
                                    |___/              |___/           |___/ 
    """)
    print_yellow("Granny and Grandpa are watching... Survive 5 days and escape the mansion!")
    sleep(2)

def choose_difficulty():
    print("\nChoose Difficulty:")
    print("1. Easy")
    print("2. Normal")
    print("3. Hard")
    while True:
        choice = input("Enter (1-3): ").strip()
        if choice == "1": game_state["difficulty"] = "Easy"; break
        elif choice == "2": game_state["difficulty"] = "Normal"; break
        elif choice == "3": game_state["difficulty"] = "Hard"; break
        else: print_red("Invalid choice.")
    print_green(f"Difficulty set to: {game_state['difficulty']}")

def assign_items():
    locations = random.sample(rooms, k=len(items_pool))
    game_state["item_locations"] = dict(zip(items_pool, locations))

def choose_escape_route():
    print("\nEscape Routes:")
    for i, route in enumerate(escape_routes, 1):
        print(f"{i}. {route}")
    while True:
        choice = input("Choose escape path (1-3): ").strip()
        if choice in ["1", "2", "3"]:
            game_state["escape_route"] = list(escape_routes.keys())[int(choice)-1]
            break
        else:
            print_red("Invalid choice.")
    print_green(f"Escape route selected: {game_state['escape_route']}")

# ================= GAMEPLAY ==================
def move_to_room():
    print("\nAvailable Rooms:")
    for i, r in enumerate(rooms):
        print(f"{i+1}. {r}")
    while True:
        try:
            choice = int(input("Move to room: "))
            if 1 <= choice <= len(rooms):
                game_state["player_room"] = rooms[choice-1]
                print_green(f"You moved to {rooms[choice-1]}")
                break
        except:
            print_red("Invalid input.")

def search_room():
    found = False
    for item, loc in game_state["item_locations"].items():
        if loc == game_state["player_room"] and item not in game_state["inventory"]:
            print_cyan(f"🔍 You found: {item}")
            game_state["inventory"].append(item)
            found = True
    if not found:
        print("Nothing useful found here.")

def granny_grandpa_attack():
    chance = {"Easy": 0.2, "Normal": 0.4, "Hard": 0.7}[game_state["difficulty"]]
    if random.random() < chance:
        print_red("\n👣 You hear loud footsteps... Granny or Grandpa is nearby!")
        print_yellow("Type 'hide' in 3 seconds or get knocked out!")

        caught = True

        def timer():
            nonlocal caught
            time.sleep(3)
            if caught:
                print_red("\nToo slow! They've caught you. You lost a day.")
                game_state["day"] += 1
                if game_state["day"] > game_state["max_days"]:
                    print_red("\n💀 GAME OVER! They got you too many times.")
                    exit()

        t = threading.Thread(target=timer)
        t.start()
        user_input = input(">> ").strip().lower()
        if user_input == "hide":
            caught = False
            print_green("✅ You hid successfully.")
        else:
            print_red("Wrong input! You got caught.")
            game_state["day"] += 1
            if game_state["day"] > game_state["max_days"]:
                print_red("\n💀 GAME OVER! They got you too many times.")
                exit()
        t.join()

def try_escape():
    needed_items = escape_routes[game_state["escape_route"]]
    missing = [item for item in needed_items if item not in game_state["inventory"]]
    if missing:
        print_red(f"Cannot escape yet. Missing {len(missing)} item(s): {', '.join(missing)}")
    else:
        print_green("🚁 YOU ESCAPED SUCCESSFULLY! 🎉 Congratulations!")
        game_state["escaped"] = True
        exit()

# ================= MAIN LOOP ==================
def play_game():
    intro()
    choose_difficulty()
    assign_items()
    choose_escape_route()

    while game_state["day"] <= game_state["max_days"]:
        print_yellow(f"\n📅 Day {game_state['day']} | Room: {game_state['player_room']} | Inventory: {game_state['inventory']}")
        print("\n1. Move Room\n2. Search Room\n3. Try to Escape\n4. Quit")
        choice = input("Choose action (1-4): ").strip()

        if choice == "1":
            move_to_room()
        elif choice == "2":
            search_room()
            granny_grandpa_attack()
        elif choice == "3":
            try_escape()
        elif choice == "4":
            print_red("Exiting game. Bye!")
            break
        else:
            print_red("Invalid choice.")

if __name__ == "__main__":
    play_game()
