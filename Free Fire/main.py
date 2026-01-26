from time import sleep
from random import choice, randint

def s(txt, delay=0.002):
    for char in txt:
        print(char, end='', flush=True)
        sleep(delay)
    print()

def search_guns():
    Guns = [
        "AK 47","G-18", "M18873", "Shot Gun", "Vector", "Plasma", "Healing Gun", "P-90", "MP-5", "Desert Eagle"
    ]
    gun = choice(Guns)
    s(f"You got -> {gun}")

def search_enemies():
    chance = randint(1,2)
    if chance == 1:
        s("Found an Enemy!")
        s("Let's Kill him!")
        kill_chance = randint(1,2)
        if kill_chance == 1:
            print("Killing", end='', flush=True)
            s("...",2)
            s("Enemy Killed!\n")
            s(f"\n\n\t{name} Killed a Player!")
        else:
            print("Killing", end='', flush=True)
            s("...",2)
            s("\nOh! You are Being Killed by the Enemy! Better Luck next Time!")
            exit()
    else:
        s("Safe! No Enemy Here Now!")

def hide_n_camp():
    s("\nLet's Hide and Camp to kill enemies Safely!")
    chance = randint(1,2)
    if chance == 1:
        s("Found Enemy kill him Sneakly!")
    else:
        s("No Enemies Now!")

def main():
    global name
    s("Welcome To Free Fire!")
    s("Here you can kill Enemies, Get Guns, and Win!")
    s("So, Let's Get Started!")
    name = input("\nName>> ")
    s(f"\n\tYour Name is>> {name}")
    s(f"\tWith Id>> {randint(100000, 999999)}")
    s("\n\nNow Let's Go to the Battle Ground")
    while True:
        s("\nWhat do you want to do?")
        s("1. Search For Guns!")
        s("2. Search For Enemies!")
        s("3. Hide and Camp!")
        ask = int(input("\n(1/3)>> "))
        if ask == 1:
            search_guns()
        elif ask == 2:
            search_enemies()
        elif ask == 3:
            hide_n_camp()
        else:
            s("Invalid! Choice!")
main()