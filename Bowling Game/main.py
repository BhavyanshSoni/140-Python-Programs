from time import sleep
from random import choice

# Used slow print for making the programme better. 
def s(txt,delay=0.04):
    for char in txt:
        print(char,end='',flush=True)
        sleep(delay)
    print()
# This is the welcome(Function) of the game.This prints the welcome screen of the game
def welcome():
    s("Welcome to the Bowling game 🎳!")
    s("In this you have to Bowl and should down the PINS!")
    s("There will be 3 Rounds!")
    s("Let's Get started!\n")

# This is the main(Function) of the game.In this Function random_pins are selected and then the user bowl and Knock Down Bowls Randomly().
def main():
    score = 0 # Score is used to save that how many bowls the user knocked down in a Strike.
    for i in range(1,4):
        random_pins = choice(list(range(1,11)))
        s("\n--------------------")
        s(f"--------ROUND{i}/3--------")
        s("--------------------")
        print("Bowling", end='',flush=True)
        s("...", delay=1)
        s("You Rolled the Bowl...🎱🎳")
        s(f"Knocked Down... {random_pins} Balls.")
        score += random_pins
        with open("score.txt", "w") as f: # Saving the score to keep the record of the recent Match.
            f.write(f"You Knocked Down... {random_pins} Bowls 🎳")
    s(f"You Score is {score}/30.")

welcome()
main()
# <-- Functions are called here.

# --------------------------------END---------------------------