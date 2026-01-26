import random

def start_game():
    print("\n-- Number Guessing Game --")
    comp_num = random.randint(1, 100)
    guesses = 0

    for i in range(10):
        try:
            num = int(input("Enter a number (1-100): "))
            guesses += 1

            if num == comp_num:
                print("*****************************************************")
                print(f"🎉 You guessed the number in {guesses} tries!")
                print("*****************************************************")
                return 10
            elif num > comp_num:
                print("🔻 Lower number please!")
            else:
                print("🔺 Higher number please!")
        except ValueError:
            print("❌ Invalid input. Please enter a number.")

    print(f"😢 You lost! The correct number was: {comp_num}")
    return 0

start_game()