import os
def welcome_screen():
    print("Welcome To MINI GAME HUB  ---> Made By Bhavyansh Soni")
    print("In This MINI GAME HUB You Can Play: ")
    print("1. Flappy Bird 🐤")
    print("2. Letter 🔤 Guessing 🤔 Game 🎮")
    print("3. Ludo 🎲")
    print("4. Number 🔢 Guessing 🤔 Game🎮")
    print("5. Rock 🥌 Paper 📜 Scissors ✂")
    print("6. Snake 🐍 and Ladders ⛓")
    print("7. Word 🔠 Guessing 🤔 Game 🎮")

games = {
    "flappy bird":"Games/flappy_bird.py", 
    "letter guessing game":"Games/letter_guess.py", 
    "ludo":"Games/Ludo.py", 
    "number guessing game":"Games/number_guess.py", 
    "rock paper scissors":"Games/rps.py", 
    "snake and ladders":"Games/snake_and_ladders.py", 
    "word guessing game":"Games/word_guess.py"
}


while True:
    welcome_screen()
    game = input("Enter Name Of Game You Want To Play: ")
    if game.lower() in games:
        print(f"Opening {game}")
        os.system(f"python {games[game.lower()]}")
    
    elif game.lower() == "quit":
        print("Exiting... GoodBye... 👋🏻")
        break
    else:
        print("Invalid Game Name!\nTry Again!")
