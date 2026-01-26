from time import sleep
import random

def s(txt, delay = 0.05):
    for char in txt:
        print(char, end='', flush=True)
        sleep(delay)
    print()

def welcome():
    s("Welcome to the game!")
    s("5 ROUNDS")
    s("You Should Do A Challange where you Guess A Brainrot")
    s("If It will be correct you'll get a Point!")
    s("And If You Guess Wrong You'll Lose a Life")
    s("Get Ready 😎!")

def check_brainrot(brainrot,random_brainrot):
    if brainrot == random_brainrot:
        s("Correct Brainrot\nNice! ✅")
    else:
        s("Wrong Brainrot\n❌!")

def choose_brainrot():
    global brainrots
    brainrots = [
        "Tung Tung Sahur",
        "Brr Brr Patapim",
        "Chimpanzini Bananini",
        "Bomberdino Crocodilo",
        "Tra La Lero Tra La La"
    ]
    i = 0
    while i < 5:
        i += 1
        random_brainrot = random.choice(brainrots)
        s(random_brainrot)
        s("\n Guess The Brainrot: ")
        j = 0
        for rot in brainrots:
            j = j + 1
            s(f"{j}. {rot}!")
        try:
            action = int(input("(1-5)>> "))
            if action == 1:
                brainrot = "Tung Tung Sahur"
                s(f"You Chose '{brainrot}'")
                check_brainrot(brainrot,random_brainrot)
            
            elif action == 2:
                brainrot = "Brr Brr Patapim"
                s(f"You Chose '{brainrot}'")
                check_brainrot(brainrot,random_brainrot)
            
            elif action == 3:
                brainrot = "Chimpanzini Bananini"
                s(f"You Chose '{brainrot}'")
                check_brainrot(brainrot,random_brainrot)
            
            elif action == 4:
                brianrot = "Bomberdino Crocodilo"
                s(f"You Chose '{brainrot}'")
                check_brainrot(brainrot,random_brainrot)
            
            elif action == 5:
                brainrot = "Tra La Lero Tra La La"
                s(f"You Chose '{brainrot}'")
                check_brainrot(brainrot,random_brainrot)

            else:
                s("Invalid Brainrot!!")

        except ValueError as v:
            s("\nInvalid Brainrot!")

# welcome()
choose_brainrot()