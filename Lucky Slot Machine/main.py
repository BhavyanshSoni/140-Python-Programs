from time import sleep
from random import choice

def s(txt, delay=0.04):
    for c in txt:
        print(c, end='', flush=True)
        sleep(delay)
    print()

def welcome():
    s("Welcome To The Lucky Slot(Casino)🎰")
    s("In this game you have to spin 5 Times and Hope to get the JACKPOT!")
    s("Let's Get Started!\n")

def main():
    slots = list(range(1,11))
    for i in range(5):
        s("Let's SPIN 💫")
        print("Spining", end='',flush=True)
        s("...", 0.7)
        em_1 = choice(slots)
        em_2 = choice(slots)
        em_3 = choice(slots)
        s(f"You Got: {em_1}  {em_2}  {em_3}")
        if em_1 == em_2 and em_1 == em_3:
            s("CONGRATULATIONS... ITS A JACKPOT!")
        else:
            s("Better Luck Next Time 👋🏻!\n")
    
welcome()
main()
