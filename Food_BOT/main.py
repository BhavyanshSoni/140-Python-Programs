from time import sleep

def s(txt, delay=0.04):
    for c in txt:
        print(c, end='', flush=True)
        sleep(delay)
    print()

def main():
    s("Welcome to the Food Bot!")
    s("Here the BOT will cook a dish for you and you will decide if it is Tasty or Not!")
    s("Let's Get Started!\n")
    try:
        no_of_dishes = int(input("Enter How many Dishes the bot should cook for you>> "))
        for i in range()
    except ValueError:
        s("Invalid Number Of DISHES!")