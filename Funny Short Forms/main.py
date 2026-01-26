from time import sleep
from random import randint

def s(txt, delay=0.004):
    for c in txt:
        print(c, end='', flush=True)
        sleep(delay)
    print()

def main():
    s("Welcome to Short Forms Saver!")
    s("Here you can save Funny short forms of words as you want!")
    s("Let's Get Started!")
    while True:
        word = input("\n\nWord>> ")
        shrt_frm = input("\nShort Form>> ")
        s(f"\n\n\tWord -> {word}")
        s(f"\tShort Form -> {shrt_frm}")
        with open("Short Forms.txt", "a") as f:
            f.write(f"Word -> {word}\nShort Form -> {shrt_frm}\n")
            
        again = input("\nWant to Save Again(Y/N)>> ")
        if again.lower() == "n":
            s("Thanks for using this Program. GoodBye...")
            break
        else:
            s("Thanks for using this Program Once Again!")

main()