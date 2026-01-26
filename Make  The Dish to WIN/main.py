from time import sleep
from random import choice

def s(txt, delay=0.04):
    for c in txt:
        print(c, end='', flush=True)
        sleep(delay)
    print()

def main():
    s("Welcome To Make The Dish and WIN!")
    s("In this game you have to make a dish and I will rate the DISH!")
    s("You have to make 3 DISHES!")
    s("Let's Get Started!\n")
    for i in range(3):
        rate = choice(list(range(1,11)))
        print(f"MAKING DISH {i+1}", end='', flush=True)
        s("...", 1)
        s("|------------------------------------------|", 0)
        s(f"| Dish {i+1} -->  {rate}/10                         |", 0)
        s("|------------------------------------------|\n", 0)
        with open("rates.txt", "a") as f:
            f.write(f"\nDish {i+1}. -->  {rate}/10\n")
main()
