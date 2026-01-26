from time import sleep
from random import choice

def s(txt, delay=0.03):
    for char in txt:
        print(char, end='', flush=True)
        sleep(delay)
    print()

def main():
    s("Welcome To Knowledge Checker!")
    s("In this you can enter a name and then the programme will guess his/her knowledge in PERCENTAGE(%)!")
    s("Let's Get Started!\n")
    while True:
        name = input("Name>> ")
        percent = choice(list(range(1,101)))
        print('Calculatiing Knowledge', end='', flush=True)
        s("...",1.5)
        s(f"Name -> {name}\nKnowledge Percentage(%) -> {percent}")
        again = input("Want to Calculate Again(Y/N)>> ")
        if again.lower() == "y":
            s("\n")
        elif again.lower() == "n":
            s("Thanks for using this Programme... GoodByee...")
            break
        else:
            s("Invalid Choice\nTry Again!")
            break


main()