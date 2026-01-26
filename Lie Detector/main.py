from time import sleep
from random import choice

def s(txt,delay=0.04):
    for char in txt:
        print(char, end='',flush=True)
        sleep(delay)
    print()

def main():
    s("Welcome To The Lie ❌ Detector ✅!")
    s("Let's See How Honest are you")
    s("In this Programme you will enter somthing like (I got 100$ Today) and the Programme will detect if you are lying or not!")
    s("Let's Get Started!\n")
    choices = [
        "Truth", "Lie"
    ]
    try:
        no_of_detects = int(input("How Many Sentences you want to detect>> "))
        for i in range(no_of_detects):
            detect = choice(choices)
            content = input(">> ")
            print("Detecting",end='',flush=True)
            s("...",1)
            s("\n")
            s(f"It's a {detect}")
            with open(f"History.txt", "a") as f:
                f.write(f"{content}  --> {detect}\n")
        s("\nThanks For Using This Programme Made By Bhavyansh Soni! GoodByee...")
    except ValueError:
        s("Invalid Number")

main()