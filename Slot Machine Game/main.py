import random
import time

def slot_machine():
    symbols = ["🍒", "🍋", "🍉", "⭐", "7️⃣", "🍇"]
    print("🎰 Welcome to the Slot Machine! Type 'spin' to play or 'quit' to exit.\n")

    while True:
        user_input = input("Enter command: ").lower()
        if user_input == 'quit':
            print("Thanks for playing! Good luck next time 🍀")
            break
        elif user_input == 'spin':
            print("Spinning...", end="", flush=True)
            for _ in range(3):
                print(".", end="", flush=True)
                time.sleep(0.5)
            print()

            result = [random.choice(symbols) for _ in range(3)]
            print(" | ".join(result))

            if result[0] == result[1] == result[2]:
                print("🎉 Jackpot! You won! 🎉\n")
            else:
                print("Try again!\n")
        else:
            print("Invalid command. Type 'spin' or 'quit'.\n")

if __name__ == "__main__":
    slot_machine()
