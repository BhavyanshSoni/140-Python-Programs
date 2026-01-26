from time import sleep # <-- Time module is imported to support the Slow Print(Function).
from random import randint # <-- Random module is imported to randomly choose the hits.

# This is the Slow Print(Function).
def s(txt, delay=0.04):
    for char in txt:
        print(char, end='', flush=True)
        sleep(delay)
    print()

# This is the welcome(Function).Used to print the welcome screen of the game.
def welcome():
    s("Welcome to the Cricket Hitter 🏏 Game!")
    s("You have to hit and score as high as you can!")
    s("Let's Get Started!")

# This is the main(Function) of the game.
def main():
    score = 0
    random_hit = randint(1,8) # Using numbers to select Hits Randomly.
    for i in range(6): # For loop is used to Iterate this function 6 times(Like a Over).
        s("\n|--------------------------------------|")
        s(f"|--------------BALL: {i+1}/6---------------|")
        s("|--------------------------------------|\n")
        print("Hitting", end='', flush=True)
        s("...", 0.9)
        if random_hit == 1 or random_hit == 2: # This shows that if the random number is 1 or 2 then its a Six.
            s("Hurray! Its a Six")
            score += 6
        elif random_hit == 3 or random_hit == 4:
            s("Well Done, Its a Four")
            score += 4
        elif random_hit == 5 or random_hit == 6:
            s("Nice, Its a Single Run")
            score += 1
        elif random_hit == 7 or random_hit == 8: 
            s("Wow You got 2 RUNS!")
            score += 2
    with open("Score.txt", "w") as f: # Saving the score in the Score.txt File to keep the record of the recent Match/Game.
        f.write(f"Your Runs are: {score}/36!")
        s(f"Your Runs are: {score}/36!")
        s("GoodBye... Thanks for Playing")

welcome()
main()
# <-- Functions are called here.

# ------------------------------------------------END--------------------------------------------