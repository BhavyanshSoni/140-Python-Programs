# Modules Like (time and random) Are Imported Here.
from time import sleep # <-- time module Imported Here.
from random import choice # <-- random Module Imported Here.

def s(txt, delay=0.04): # <-- This is slow_print(Function), This is used to make the programme more attractive.
    for char in txt:
        print(char, end="", flush=True)
        sleep(delay)
    print()


def welcome(): # <-- This is Welcome(Function), This function displays the welcome screen of the game.
    s("Welcome To 'AI V/S Humans Guessing Duel!'\n")
    s("In This Game User will choose a number from 1 to 10 and the AI will guess the number in 3 TRIES!\n")
    s("If the AI Guesses the number in 3 TRIES then AI WINS else User Wins!\n")
    s("Let's Get Started!\n")


def take_number():
    global num # num is Global to use it in the guess_number(Function).
    s("User Choose a number from 1 to 10\n")
    try:
        num = int(input("Enter>> "))
        if num < 1 or num > 10:
            s("Invalid Input! Please Enter a number between 1 and 10")
            exit()
        else:
            s(f"So You Have Chosen: {num}\n")
    except ValueError:
        s("Invalid Input! Please Enter a valid number")
        exit()

def guess_number(): # <-- This is guess_number(Function), Used to let AI guess the number.
    s("AI Is Guessing the number...\n")
    for i in range(1, 4): # <-- for loop is used to run the guessing of AI '3' Times.
        guess = choice(range(1, 11))
        s(f"AI Guessed: {guess}")
        if guess == num:
            s("🎉 Congratulations, AI 🤖 Wins!")
            exit()  # exit() is used here to End the Programme cause AI WINS.
        else:
            s("Wrong Number... AI will Try Again!\n")

    s("🎉 Congratulations, User Wins!")  # This Line Displays User Wins when the loop is ended!



welcome()
take_number()
guess_number()
# Functions Are Called Here.