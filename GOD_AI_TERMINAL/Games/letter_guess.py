import random

def start_game():
    print("\n-- Letter Guessing Game --")
    alphabets = [chr(i) for i in range(65, 91)]  # A-Z
    comp_choice = random.choice(alphabets)
    guesses = 0

    for i in range(10):
        guesses += 1
        user_input = input("Enter a letter (A-Z): ").upper()

        if user_input == comp_choice:
            print("************************************************")
            print(f"You guessed the letter in {guesses} tries! 🎉")
            print("************************************************")
            return 10
        else:
            print("❌ Wrong letter. Try again!")

    print(f"😢 You lost! The correct letter was: {comp_choice}")
    return 0
start_game()