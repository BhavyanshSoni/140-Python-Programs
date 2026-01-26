# This Programme is made by Bhavyansh Soni.
from time import sleep # sleep(Function) is imported from time to support attractive slow print(Function).
from random import randint # This Module is imported to generate a random number from 1 to 100.

def s(txt, delay=0.04): # This is the slow print(Function).
    for char in txt:
        print(char, end='', flush=True)
        sleep(delay)
    print()

def welcome(): # This Function displays the Welcome screen of the game.
    s("Welcome To Another AI V/S Humans Game!")
    s("In this game a random number will be generated, after that the Ai and user both have to guess the number!")
    s("Let's Get Started!\n")

# This is the main(Function) of the game
def main():
    while True: # Using while True to run the games as many times as the user want.
        random_number = randint(1,100) # This is random_number varaiable to generate a random number.
        user_number = int(input("\nGuess The Number>> ")) # This is here to take input from user.
        ai_number = randint(1,100) # This variable is used to let the (AI) guess a random number.
        s(f"\nYou Guessed: {user_number}\nAi Guessed: {ai_number}\n")
        # This is the if-elif-else ladder.
        if user_number == random_number:
            s(f"User Guessed The Correct Number✅ : {random_number}\n")
        elif ai_number == random_number:
            s(f"Ai Guessed The Correct Number✅ : {random_number}\n")
        else:
            s("You Both are WRONG ❌!\n")
        again = input("Want to Play Again (Y/N): ")
        if again.lower() == "n": # Asking if the user want to play again or not.
            s("GoodBye...Thanks For Playing...")
            break # Breaking the loop to exit()

welcome()
main()
# END.