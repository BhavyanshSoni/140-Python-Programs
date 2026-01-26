from time import sleep
from random import choice, randint
from colorama import Fore

def s(txt, delay=0.04):
    for chr in txt:
        print(Fore.MAGENTA + chr, end='', flush=True)
        sleep(delay)
    print()

def welcome():
    s("Welcome To Take N Fight!")
    s("In this game you will be given a random character and after that you have to fight a Random Character!")
    s("Let's Get Started!\n")

def main():
    characters = [
        "Goku", "Vegeta", "Piccolo", "Kokushibo", "Akaza", "Douma", "Tanjiro", "Master Roshi", "Black Goku", "Trunks", "Gohan", "Sukuna", "Levi", "Zenitsu", "Inosuke", "Nezuko", "Genya", "Gyomei", "Sanemi", "Rengoku", "Muichiro", "Obanai", "Mitsuri", "Broly", "Vegito", "Gogeta", "Bardock" 
    ]
    try:
        no_of_rounds = int(input("Enter Number of Rounds>> "))
        if no_of_rounds < 1:
            s("Invalid Enter Number Greater than 0!")
        else:

            user_score = 0 
            comp_score = 0 
            user_cha = choice(characters)
            print("You are", end='', flush=True)
            s("...", 1.4)
            s(f"{user_cha}")
            comp_cha = choice(characters)
            s(f"\nYour Opponent is {comp_cha}")

            for i in range(no_of_rounds):
                s("\n------------------------------------------------------", 0)
                s(f"--------------------ROUND {i+1}/{no_of_rounds}-------------------------", 0)
                s("------------------------------------------------------", 0)
                s(f"\nUser Score: {user_score}")
                s(f"Computer Score: {comp_score}")
                s("\n\nReady\nGet\nSet\nFIGHT 💀!")
                print("FIGHTIN",end='',flush=True)
                s("G...", 1.5)
                s("\n")
                num = randint(1,2)
                if num == 1:
                    winner = user_cha
                    s(f"And The Winner 👑 is: {winner}")
                    user_score += 1
                else:
                    winner = comp_cha
                    s(f"And The Winner 👑 is: {winner}")
                    comp_score += 1
            if user_score > comp_score:
                s(f"THE CHAMPION 🥇 🏆 is: {winner}")
                s(f"{winner} Won {user_score} ROUNDS")

            elif user_score < comp_score:
                s(f"THE CHAMPION 🥇 🏆 is: {winner}")
                s(f"{winner} Won {comp_score} ROUNDS")
            else:
                s("TIE! 🤝🏻")
                
    except ValueError:
        s("Invalid ❌ Number of Rounds!!!")


welcome()
main()
    