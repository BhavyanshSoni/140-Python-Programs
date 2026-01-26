import os
import random
import time

# Colors & emojis
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033'
    BOLD = '\033[1m'

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def slow_print(text, delay=0.02):
    for c in text:
        print(c, end='', flush=True)
        time.sleep(delay)
    print()

def get_int_input(prompt, min_val, max_val):
    while True:
        try:
            val = int(input(prompt))
            if val < min_val or val > max_val:
                print(Colors.WARNING + f"Enter number between {min_val} and {max_val}" + Colors.ENDC)
                continue
            return val
        except ValueError:
            print(Colors.FAIL + "Invalid input, enter a number." + Colors.ENDC)

# Game 1: Tic Tac Toe (2 players)
def game_tic_tac_toe(players):
    board = [' '] * 9

    def print_board():
        print(f"""
         {board[0]} | {board[1]} | {board[2]} 
        ---+---+---
         {board[3]} | {board[4]} | {board[5]} 
        ---+---+---
         {board[6]} | {board[7]} | {board[8]} 
        """)

    def check_winner(p):
        combos = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        for c in combos:
            if board[c[0]] == board[c[1]] == board[c[2]] == p:
                return True
        return False

    current = 0
    symbols = ['X', 'O']
    total_moves = 0
    clear()
    print(Colors.OKGREEN + "🎮 Tic Tac Toe - 2 Players" + Colors.ENDC)

    while total_moves < 9:
        print_board()
        player = players[current]
        print(f"{Colors.OKCYAN}{player}'s turn ({symbols[current]}){Colors.ENDC}")
        move = get_int_input("Enter cell (1-9): ", 1, 9) -1
        if board[move] != ' ':
            print(Colors.WARNING + "Cell already taken, try again." + Colors.ENDC)
            continue
        board[move] = symbols[current]
        total_moves +=1
        if check_winner(symbols[current]):
            print_board()
            print(Colors.OKGREEN + f"🏆 {player} wins!" + Colors.ENDC)
            input("Press Enter to return to Game Hub...")
            return
        current = 1 - current

    print_board()
    print(Colors.WARNING + "🤝 It's a draw!" + Colors.ENDC)
    input("Press Enter to return to Game Hub...")

# Game 2: Rock Paper Scissors (2 players)
def game_rps(players):
    choices = ['rock', 'paper', 'scissors']
    score = {players[0]:0, players[1]:0}
    rounds = 3
    clear()
    print(Colors.OKGREEN + "✊ Rock Paper Scissors - Best of 3" + Colors.ENDC)

    for r in range(1, rounds+1):
        print(f"Round {r}")
        p1_choice = input(f"{players[0]}, enter rock/paper/scissors: ").lower()
        while p1_choice not in choices:
            print(Colors.FAIL + "Invalid choice, try again." + Colors.ENDC)
            p1_choice = input(f"{players[0]}, enter rock/paper/scissors: ").lower()
        clear()
        p2_choice = input(f"{players[1]}, enter rock/paper/scissors: ").lower()
        while p2_choice not in choices:
            print(Colors.FAIL + "Invalid choice, try again." + Colors.ENDC)
            p2_choice = input(f"{players[1]}, enter rock/paper/scissors: ").lower()
        clear()
        print(f"{players[0]} chose {p1_choice}, {players[1]} chose {p2_choice}")

        if p1_choice == p2_choice:
            print("🤝 Draw this round")
        elif (p1_choice == 'rock' and p2_choice == 'scissors') or \
             (p1_choice == 'paper' and p2_choice == 'rock') or \
             (p1_choice == 'scissors' and p2_choice == 'paper'):
            print(f"🏆 {players[0]} wins this round!")
            score[players[0]] +=1
        else:
            print(f"🏆 {players[1]} wins this round!")
            score[players[1]] +=1
        time.sleep(1)

    print(f"\nFinal Score: {players[0]} {score[players[0]]} - {score[players[1]]} {players[1]}")
    if score[players[0]] > score[players[1]]:
        print(Colors.OKGREEN + f"🎉 {players[0]} wins the game!" + Colors.ENDC)
    elif score[players[1]] > score[players[0]]:
        print(Colors.OKGREEN + f"🎉 {players[1]} wins the game!" + Colors.ENDC)
    else:
        print(Colors.WARNING + "🤝 The game is a draw!" + Colors.ENDC)
    input("Press Enter to return to Game Hub...")

# Game 3: Number Guess (2-4 players)
def game_number_guess(players):
    clear()
    print(Colors.OKGREEN + "🔢 Number Guess Game" + Colors.ENDC)
    secret = random.randint(1, 100)
    tries = 0
    max_tries = 10
    current = 0
    while tries < max_tries:
        player = players[current]
        guess = get_int_input(f"{player}, guess a number between 1 and 100: ", 1, 100)
        tries +=1
        if guess == secret:
            print(Colors.OKGREEN + f"🎉 {player} guessed it right in {tries} tries!" + Colors.ENDC)
            input("Press Enter to return to Game Hub...")
            return
        elif guess < secret:
            print("🔼 Too low!")
        else:
            print("🔽 Too high!")
        current = (current +1) % len(players)

    print(Colors.FAIL + f"Game over! The secret number was {secret}" + Colors.ENDC)
    input("Press Enter to return to Game Hub...")

# Game 4: Word Scramble (2-4 players)
def game_word_scramble(players):
    words = ["python", "terminal", "computer", "program", "developer", "multiplayer"]
    clear()
    print(Colors.OKGREEN + "🔤 Word Scramble" + Colors.ENDC)
    word = random.choice(words)
    scrambled = ''.join(random.sample(word, len(word)))
    print(f"Unscramble this word: {Colors.BOLD}{scrambled}{Colors.ENDC}")
    current = 0
    tries_per_player = 3
    tries = {p: tries_per_player for p in players}

    while True:
        player = players[current]
        print(f"{player}'s turn. Tries left: {tries[player]}")
        guess = input("Your guess: ").strip().lower()
        if guess == word:
            print(Colors.OKGREEN + f"🎉 {player} got it right! The word was '{word}'." + Colors.ENDC)
            input("Press Enter to return to Game Hub...")
            return
        else:
            tries[player] -=1
            print(Colors.WARNING + "Wrong guess." + Colors.ENDC)
            if tries[player] <= 0:
                print(Colors.FAIL + f"{player} is out of tries." + Colors.ENDC)
        current = (current +1) % len(players)
        if all(t <= 0 for t in tries.values()):
            print(Colors.FAIL + f"No one guessed it. The word was '{word}'." + Colors.ENDC)
            input("Press Enter to return to Game Hub...")
            return

# Game 5: Snake Duel (2 players)
def game_snake_duel(players):
    # Simplified placeholder snake game - each player tries to guess moves correctly
    clear()
    print(Colors.OKGREEN + "🐍 Snake Duel (Guess direction)" + Colors.ENDC)
    directions = ['up', 'down', 'left', 'right']
    score = {players[0]: 0, players[1]: 0}
    rounds = 5
    for r in range(1, rounds+1):
        print(f"Round {r}")
        for p in players:
            guess = input(f"{p}, guess snake move (up/down/left/right): ").lower()
            while guess not in directions:
                print(Colors.FAIL + "Invalid direction, try again." + Colors.ENDC)
                guess = input(f"{p}, guess snake move (up/down/left/right): ").lower()
            correct = random.choice(directions)
            print(f"Snake moved {correct}.")
            if guess == correct:
                print(Colors.OKGREEN + "Correct guess! +1 point." + Colors.ENDC)
                score[p] +=1
            else:
                print("Wrong guess.")
            time.sleep(1)
        print(f"Score after round {r}: {score}")
    if score[players[0]] > score[players[1]]:
        winner = players[0]
    elif score[players[1]] > score[players[0]]:
        winner = players[1]
    else:
        winner = None
    if winner:
        print(Colors.OKGREEN + f"🏆 {winner} wins Snake Duel!" + Colors.ENDC)
    else:
        print(Colors.WARNING + "🤝 Snake Duel is a draw!" + Colors.ENDC)
    input("Press Enter to return to Game Hub...")

def get_players(num):
    players = []
    for i in range(1, num+1):
        name = input(f"Enter name for Player {i}: ").strip()
        if not name:
            name = f"Player{i}"
        players.append(name)
    return players

def game_hub():
    while True:
        clear()
        print(Colors.HEADER + Colors.BOLD + "🎲 MULTIPLAYER GAME HUB 🎲" + Colors.ENDC)
        print("Select a game to play:")
        print("1. Tic Tac Toe (2 players)")
        print("2. Rock Paper Scissors (2 players)")
        print("3. Number Guess (2-4 players)")
        print("4. Word Scramble (2-4 players)")
        print("5. Snake Duel (2 players)")
        print("6. Quit")

        choice = get_int_input("Enter choice: ", 1, 6)

        if choice == 6:
            print(Colors.OKGREEN + "👋 Thanks for playing! Bye." + Colors.ENDC)
            break

        if choice == 1:
            players = get_players(2)
            game_tic_tac_toe(players)
        elif choice == 2:
            players = get_players(2)
            game_rps(players)
        elif choice == 3:
            num_p = get_int_input("Enter number of players (2-4): ", 2, 4)
            players = get_players(num_p)
            game_number_guess(players)
        elif choice == 4:
            num_p = get_int_input("Enter number of players (2-4): ", 2, 4)
            players = get_players(num_p)
            game_word_scramble(players)
        elif choice == 5:
            players = get_players(2)
            game_snake_duel(players)

if __name__ == "__main__":
    game_hub()
