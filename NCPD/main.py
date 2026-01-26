from time import sleep
from random import choice
from os import makedirs, path

def s(txt, delay=0.04):
    for char in txt:
        print(char, end='', flush=True)
        sleep(delay)
    print()

def solve_crimes():
    global crimes_solved
    s_o_n = ["Solved", "Not Solved", "Solved", "Not Solved", "Solved", "Not Solved"]
    crimes_solved = 0
    s("\nLet's Solve Crimes!")
    print("\nSOLVING CRIME", end='', flush=True)
    s("...", 1)
    if choice(s_o_n) == "Not Solved":
        s("Sorry, The Case is too hard for you!\nYou don't have to potential to solve it!\n")
    else:
        s("Congratulations! Now the Criminal is in the JAIL ")
        crimes_solved += 1
        with open(f"{name}\\Crimes Solved.txt", "w") as f:
            f.write(f"{crimes_solved}")
        with open(f"{name}\\Crimes Solved.txt") as f:
            crimes_solved = int(f.read())

def get_promoted():
    global rank
    s(f"Let's Give Promotion to you Officer!")
    ranks = {
        "inspector":10, "sub inspector":15, "incharge":20, "dgp":25, "ips":30, "ras":40
    }
    j =0
    s("Posts:")
    for i in ranks:
        j +=1
        s(f"{j}. {i.capitalize()}")

    which_rank = input("In which rank you would like to be promoted>> ")
    file_path = f"E:\\Python Programmes\\NCPD\\{name}\\"
    if path.exists(file_path):
        s("\nInfo Saved")
    else:
        makedirs(f"{name}")
    if which_rank.lower() in ranks and crimes_solved == ranks[which_rank.lower()]:
        s(f"You Are Promoted to the {which_rank} Rank!")
        with open(f"{name}\\Ranks.txt", "w") as f:
            f.write(f"{which_rank}")
    else:
        s("Invalid Rank or Not Enough Crimes Solved Yet!")
        
    
def main():
    global name
    name = input("Your Name>> ")
    s(f"\nWelcome Officer 👮🏻‍♂️/👮🏻‍♀️ {name}")
    s("In this Program you can Solve Crimes and Get Promoted!")
    s("Let's Get Started!")
    while True:
        s("\nWhat do you want to do?")
        s("1. Solve Crimes!")
        s("2. Get Promoted!")
        s("3. See Info about You!")
        s("4. Exit!")
        ask = int(input("\n(1/4)>> "))
        if ask == 1:
            solve_crimes()
        elif ask == 2:
            get_promoted()
        elif ask == 3:
            with open(f"{name}\\Ranks.txt") as f:
                rank = f.read()
            s(f"Name -> {name}")
            s(f"Rank -> {rank}")
            
main()