from time import sleep
from random import *
from colorama import Fore, init

init()

def s(txt, d=0.04):
    for i in txt:
        print(i, end='', flush=True)
        sleep(d)
    print()


def main():
    s(Fore.LIGHTBLUE_EX + "Welcome to Flip Us! -> Made by 'Bhavyansh Soni'")
    s(Fore.LIGHTCYAN_EX + "In this game you have to flip cards and match them you would be given chances.")
    s(Fore.LIGHTMAGENTA_EX + "And you must match 5 set of cards to win!")
    s(Fore.GREEN + "\nLet's Get Started!")
    
    while True:
        score = 0
        card1 = randint(1,2)
        card2 = randint(1,2)
        flip = input(Fore.LIGHTYELLOW_EX + "\nPress any key to Flip (Recommended -> Enter):- ")
        s(Fore.LIGHTCYAN_EX + "\n\tCard Flipped!")
        flip2 = input(Fore.LIGHTYELLOW_EX + "\n Press any key to Flip the second card:- ")
        s(Fore.CYAN + "\n\tSecond Card Flipped!\n")

        if (card1 == 1 and card2 == 1) or (card1 == 2 and card2 == 2):
            s(Fore.LIGHTGREEN_EX + "Hurray! you Matched 1 set of Cards!")
            score += 1
        else:
            s(Fore.RED + "Oops! That wasn't the Card You were looking for!")

        if score == 5:
            s(Fore.GREEN + "Congratulations! You Won! ✨")
        
main()
            
