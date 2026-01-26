from time import sleep
from random import choice

# Slow print is used to make the programme attractive: TIP.
def s(txt, delay=0.04):
    for char in txt:
        print(char, end='', flush=True)
        sleep(delay)
    print()

# This is the Welcome(Function) of the game.This prints the welcome screen of the game.
def welcome():
    s("Welcome To The Football ⚽ Penalty Shootout!")
    s("In this game you have to shoot a Penalty!")
    s("Be carefull because the Goal 🥅 Keeper 🧤 is Tough!")
    s("Let's Get Started!\n")

# I have used classes for more clarity and for seperating the Striker's(Function) and GoalKeeper's(Function).
class Striker:
    def __init__(self):
            global user_direction
            s("\nNow Tell me the direction you want to hit ⚽ in! ")
            s_direction = input("Left(L), Right(R), Center(C)>> ")
            if s_direction.lower() == "l":
                user_direction = "Left"
            elif s_direction.lower() == "r":
                user_direction = "Right"
            elif s_direction.lower() == "c":
                user_direction = "Center"
            else:
                s("Invalid Direction\nTry Again")
                exit()

        
class GoalKeeper:
    def __init__(self):
        global g_direction
        directions = [ # This is Directions list to let the Goal Keeper decides its directions to save
            "Left",
            "Right",
            "Center"
        ]
        g_direction = choice(directions)


welcome() # <-- Here welcome(Function) is called.
score = 0
for i in range(1, 6): # There will be 5 Rounds that's the reason i have used for loop!
    s("----------------------------")
    s(f"--------ROUND {i}/5-----------")
    s("----------------------------")
    a = Striker()
    b = GoalKeeper()
    print("Shootin", end='', flush=True)
    s("g...", delay=1)
    if user_direction == g_direction:
        s("Its a Saaaaave!\n")
    else:
        s("YEAH YOU DID ITS A GOAAAAAAAL ⚽\n")
        score += 1
s(f"You Scored {score}/5 Goals ⚽") # Printing the score of the user that how many goals He/She hit.
with open("score.txt", "w") as f: # Writing the Score of user in score.txt for saving it.
    f.write(f"You Scored {score}/5 Goals")
# ----------------------------------------END-------------------------------------------