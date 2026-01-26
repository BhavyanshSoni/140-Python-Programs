from time import sleep # Time module is imported to use the slow_print(Function).
from random import choice # Random Module is imported to choose heads or tails(Randomly).

# This is the slow_print(Function) to print the text slowly and make the programme attractive.
def s(txt, delay=0.04):
    for char in txt:
        print(char, end='', flush=True)
        sleep(delay)
    print()

# This is the welcome(Function).Used to display the welcome screen of the Programme.
def welcome():
    s("Welcome To the Coin Flip Master!")
    s("In this game 2 Players will Flip a Coin!")
    s("Let's Get Started!\n")

# At last this is the main(Function) of the Programme which take inputs like names of players and their choices.
def main():
    name_1 = input("Name of Ist Player>> ")
    name_2 = input("Name of IInd Player>> ")
    choices = ["heads", "tails"]
    player_1_choice = input("What's Your Call?(heads/tails) ")
    random_choice = choice(choices)
    if player_1_choice.lower() == "heads" and random_choice == "heads":
        s(f"The Winner is {name_1}.")
    else:
        s(f"The Winner is {name_2}.")

welcome() 
main()
# <-- Here Functions are called.
        
# ----------------------------END----------------------------