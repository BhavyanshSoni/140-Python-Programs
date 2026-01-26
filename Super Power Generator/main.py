from time import sleep
from random import choice


def s(txt, delay=0.04):
    for c in txt:
        print(c, end='', flush=True)
        sleep(delay)
    print()

def main():
    s("Welcome To The SUPER HERO GENERATOR!")
    s("In this game you will be given a Super Power to fight an opponent!")
    s("Let's Get Started!\n")

    powers = [
        "Dark Magic", "Flight", "Heat Vision", "Speed", "Transformation-ANIMAL", "Incredible Strength", "Invisiblity", "Water Abilities", "Controlling Things from MIND", "Fire Ability", "Electric Power", "NOTHING!"
    ]
    opponents = [
        "Raven", "Superman", "Starfire", "Flash", "Beast Boy", "Hulk", "Agnes", "Aqua Man", "Professor X", "Dort", "Pugsley",
    ]
    try:
        name = input("\nYour Name>> ")
        no_of_rounds = int(input("Enter Number Of Rounds>> "))
        if no_of_rounds <= 1:
            s("Number of Rounds must be Greater than 1!")
        
        else:
            for i in range(no_of_rounds):
                s("|---------------------------------------|")
                s(f"|---------------ROUND {i+1}/{no_of_rounds}---------------|")
                s("|---------------------------------------|")
                user_power = choice(powers)
                opponent_win = choice(opponents)
                win_or_lose = choice(list(range(1,3)))
                print("Your Power is", end='', flush=True)
                s("...", 1.5)
                s(f"\n{user_power}")
                s("\nNow Let's Fight with the Opponent!")
                s(f"\n{name} V/S {opponent_win}")
                print("FIGHTING", end='', flush=True)
                s("...", 2)
                if win_or_lose == 1:
                    s(f"\nAnd the Winner 👑 is: {name}")
                else:
                    s(f"\nAnd the Winner 👑 is: {opponent_win}")

    except ValueError:
        s("Invalid Number Of Rounds!")

main()