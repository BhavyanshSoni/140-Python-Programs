from time import sleep

def s(txt,d=0.04):
    for char in txt:
        print(char, end='',flush=True)
        sleep(d)
    print()

def main():
    s("Welcome To Nicknames Maker!")
    s("Here you can make nicknames of your Friends!")
    s("Let's Get Started!\n")
    
    no_of_names = int(input("How many Nicknames you want to make>> "))
    for i in range(no_of_names):
        real_name = input("Real Name of The Person>> ")
        nick_name = input("Nick Name>> ")
        s(f"\nTHE NICKNAME of {real_name} is now: {nick_name}\n")

        with open("Nick_names.txt", "a") as f:
            f.write(f"THE NICKNAME of {real_name} is: {nick_name}\n")
    s("Thanks for Using This Programme. Made By Bhavyansh Soni! GoodByee...")

main()