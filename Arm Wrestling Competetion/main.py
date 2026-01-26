from time import sleep
from random import choice

def s(txt, delay=0.04):
    for char in txt:
        print(char, end='', flush=True)
        sleep(delay)
    print()

# This is compete(Function). This Function let the user do Arm Wrestling with the competetor and win or lose(Randomly).
def compete():
    s("\nLet's Compete in the GAME!")
    s("READY  GET  SET  GO!")
    s("\nFIGHT!")
    results = ["Win","Lose"]
    print("FIGHTINGGGG 😡", end = '', flush=True)
    s("...", delay=1.5)
    random_w_o_l = choice(results)
    if random_w_o_l == "Win": # This if condition specifies that what to print if the random_w_o_l chooses WIN or LOSE.
        s("Congratulations you Won! 👑")
        sleep(3) # Sleep is used to wait 3 seconds and then displays the Menu.
    else:
        s("Sorry, You Lost! 😥")

def main():
    while True: # Using while True to print the menu Infiinte Times.
        try:
            s("\nWelcome to the Arm 💪 Wrestling Competetion!")
            s("In this game you have to fight with the other competetor")
            s("Let's Get Started!\n")
            s("what do you want to do?")
            s("1. Compete in Arm Wrestling Competetion!")
            s("2. Exit!\n")
            ask = int(input("(1/2)>> "))
            if ask == 1:
                compete()
            elif ask == 2:
                s("Good Bye!!!")
                break
            else:
                print("Invalid🚨 Input Try Again ❌")
        except ValueError:
            s("Invalid Choice!")

main() # <-- Main(Function) is called here.