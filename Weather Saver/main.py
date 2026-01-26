from time import sleep


def s(txt, delay = 0.04):
    for char in txt:
        print(char, end = '', flush=True)
        sleep(delay)
    print()

def save():
    s("\nLet's Save Weather For")
def Menu():
    s("Welcome To Weather Saver ☁ ")
    s("Here You Can Save Daily Weathers !")
    s("Let's Get Started!")    