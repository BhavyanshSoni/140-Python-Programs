import random
from time import *

def main_screen():
    print("****HACKER TERMINAL 🐱‍💻****\n")
    sleep(1.5)
    print("Target: Secure File Server")
    sleep(1.5)
    print(f"Now Let's Start\n")
    sleep(1.5)

def first_level():
    attempts = 3
    print(">>Level 1<<\n")
    sleep(1.5)
    print("Password format: a number between 1 to 10\n")
    sleep(1.5)
    print(f"Attempts Left: {attempts}")
    sleep(1.5)
    password = random.randint(1,10)
    print(password)
    for i in range(attempts):
        try:
            user_password = int(input("> Enter Password: "))
            sleep(2.5)
            if user_password == password:
                print("Access GRANTED!\n")
                sleep(1.5)
                print("> Level 2 Unlocked... 🔓")
            else:
                attempts -= 1
                print("Access Denied 🔒!\n")
                sleep(1)
                print(f"Attempts Left: {attempts}")
                sleep(1.5)
        except ValueError as v:
            print("Access Denied 🔒!\n")
            sleep(1.5)

def second_level():
    attempts = 3
    print(">>Level 2<<\n")
    sleep(1.5)
    print("Password format: a lowercase letter from a to z\n")
    sleep(1.5)
    print(f"Attempts Left: {attempts}")
    sleep(1.5)
    lowercase = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u","v", "w", "x", "y", "z"]
    password = random.choice(lowercase)
    print(password)
    for i in range(attempts):
        try:
            user_password = input("> Enter Password: ")
            sleep(2.5)
            if user_password.lower() == password:
                print("Access GRANTED!\n")
                sleep(1.5)
                print(">> Level 3 Unlocked... 🔓")
            else:
                attempts -= 1
                print("Access Denied 🔒!\n")
                sleep(1)
                print(f"Attempts Left: {attempts}")
                sleep(1.5)
        except ValueError as v:
            print("Access Denied 🔒!\n")
            sleep(1.5)

def level_three_moves():
    print(">> Level 3: Movement Puzzle <<\n")
    sleep(1.5)
    
    grid = [["A1", "A2", "A3"],
            ["B1", "B2", "B3"],
            ["C1", "C2", "C3"]]

    position = [0, 0]  # Start at A1
    visited = [tuple(position)]
    corners_visited = 1  # Already at A1
    attempts = 10  # Max 10 moves

    print("Move using: U = Up, D = Down, L = Left, R = Right")
    print("Goal: Reach A3 or B3 passing EXACTLY 2 corners without entering Row C\n")

    while attempts > 0:
        print(f"Current Position: {grid[position[0]][position[1]]}")
        move = input("> Move (U/D/L/R): ").upper()
        new_pos = position.copy()

        if move.upper() == "U":
            new_pos[0] -= 1
        elif move.upper() == "D":
            new_pos[0] += 1
        elif move.upper() == "L":
            new_pos[1] -= 1
        elif move.upper() == "R":
            new_pos[1] += 1
        else:
            print("❌ Invalid input!")
            continue

        # Check grid bounds
        if not (0 <= new_pos[0] < 3 and 0 <= new_pos[1] < 3):
            print("❌ Out of bounds!")
            continue

        # Rule: Cannot go to Row C (row index 2)
        if new_pos[0] == 2:
            print("💀 You entered Row C (FORBIDDEN)! Game Over!")
            return

        # Rule: No revisits
        if tuple(new_pos) in visited:
            print("❌ You can't visit the same cell again!")
            continue

        # Count corners
        if new_pos in [[0,0], [0,2]]:
            corners_visited += 1

        visited.append(tuple(new_pos))
        position = new_pos
        attempts -= 1

        # Check win
        if grid[position[0]][position[1]] in ["A3", "B3"]:
            if corners_visited == 2:
                print(f"✅ You reached {grid[position[0]][position[1]]} with exactly 2 corners! Access GRANTED 🔓")
                return
            else:
                print(f"❌ Reached end but with {corners_visited} corners (need exactly 2).")
                return

    print("⏱️ Out of moves! Game Over.")
    print("🔒 Access Denied! You failed to navigate the grid correctly.\n")
    
def third_level():
    print("A1  A2  A3")
    print("B1  B2  B3")
    print("C1  C2  C3")
    print("D1  D2  D3")
    print("E1  E2  E3\n")
    print("🔐 Clues:")
    print("1. Start at A1\n2. You cannot visit any cell in Row C\n3. You must pass through exactly 2 corners\n4. Diagonal moves are forbidden\n")
    level_three_moves()


# main_screen()
# first_level()
# second_level()
third_level()
