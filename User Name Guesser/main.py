from time import sleep
from random import choice

def s(txt, delay=0.04):
    for c in txt:
        print(c, end='', flush=True)
        sleep(delay)
    print()

def main():
    s("Welcome To User Name Guesser!")
    s("In this you will enter 3 Names!")
    s("And I'll Guess what's your Name!")
    s("Let's Get Started!")
    names = []
    for i in range(3):
        name = input(f"\nName {i+1}>> ")
        names.append(name)
    
    print("\nYour Name is", end='', flush=True)
    s("...", 1.5)
    user_name = choice(names)
    s(f"{user_name}")
    y_or_n = input("Correct(Y) or Wrong(N)>> ")
    if y_or_n.lower() == "y":
        s(f"So your Name is {user_name}")
        s("\n\nThanks for Using this Programme... GoodByee...")
        exit()
    elif y_or_n.lower() == "n":
        s(f"Oh! So {user_name} is not your Name!")
        s("Sorry!")
        exit()
    else:
        s("Invalid! Choice!")
        exit()

main()