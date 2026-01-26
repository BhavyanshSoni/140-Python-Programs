from random import choice
from time import sleep

# Defining Classes to Keep the player's seperately.
class Player1:
    def __init__(self):
        # Using Slow Print To make the programme more attractive.
        def s(txt, delay= 0.04):
            for char in txt:
                print(char, end = '', flush=True)
                sleep(delay)
            print()
        
        # Using Function 'WELCOME' to print the welcome screen.
        def welcome():
            """This Function Displays The Welcome Screen of the GAME!"""
            s("Welcome To Dice 🎲 Battle ⚔")
            s("In this game two players will roll dice\nThe winner will be chosen with the outcomes of the sum of player's turn!")
            s("There'll be 3 Rounds ⭕\n")
        
        # Taking name of the first player.
        def take_name():
            """This Function Take the name of the Player"""
            global name
            s("The Name Of First Player 🎲")
            name = input(">>: ")

        # This Function Roll Dice.
        def roll():
            """This funtion roll the dice and displays a random number from the numbers(list)."""
            global outcomes
            s("\nNow Let's Roll the Dice 🎲")
            numbers = [1, 2, 3, 4, 5, 6] # The numbers(list) contains the numbers on the dice.
            outcomes = []
            for i in range(3): # Using For Loop to run this function 3 times.
                dice = choice(numbers) # random.choice is used here to take a random number from the numbers(list).
                print("\nRolling Dic", end = '')
                s("e...", delay=0.5)
                s(f"The Dice Rolled And The Number is : {dice}")
                outcomes.append(dice) # Appending dice to outcomes so that at the end we can sum to compare.

        def sum_of_outcomes():
            """This Function Displays the sum of outcomes to compare from the other player."""
            global answer
            s(f"\nNow Let's Check the outcomes of Player : {name}.")
            print("Addin", end = '')
            s("g...", delay=0.5)
            answer = sum(outcomes) # The Answer contains the sum of the outcomes.
            s(f"The Sum of Outcomes of {name} is : {answer}.")


        welcome() # Welcome Function Call.
        take_name() # take_name function call.
        roll() # Roll Function Call.
        sum_of_outcomes()
        # Function Calls.

class Player2():
    def __init__(self):
        # Using Slow Print To make the programme more attractive.
        def s(txt, delay= 0.04):
            for char in txt:
                print(char, end = '', flush=True)
                sleep(delay)
            print()
        
        # Taking name of the second player.
        def take_name():
            """This Function Take the name of the Player"""
            global name
            s("The Name Of Second Player 🎲")
            name = input(">>: ")

        # This Function Roll Dice.
        def roll():
            """This funtion roll the dice and displays a random number from the numbers(list)."""
            global outcomes
            s("\nNow Let's Roll the Dice 🎲")
            numbers = [1, 2, 3, 4, 5, 6] # The numbers(list) contains the numbers on the dice.
            outcomes = []
            for i in range(3): # Using For Loop to run this function 3 times.
                dice = choice(numbers) # random.choice is used here to take a random number from the numbers(list).
                print("\nRolling Dic", end = '')
                s("e...", delay=0.5)
                s(f"The Dice Rolled And The Number is : {dice}")
                outcomes.append(dice) # Appending dice to outcomes so that at the end we can sum to compare.

        def sum_of_outcomes():
            """This Function Displays the sum of outcomes to compare from the other player."""
            global answer2
            s(f"\nNow Let's Check the outcomes of Player : {name}.")
            print("Addin", end = '')
            s("g...", delay=0.5)
            answer2 = sum(outcomes) # The Answer contains the sum of the outcomes.
            s(f"The Sum of Outcomes of {name} is : {answer2}.")

        take_name() # take_name function call.
        roll() # Roll Function Call.
        sum_of_outcomes()
        # Function Calls.

a = Player1() # 'a' is the object of the Player1() Class.
b = Player2() # 'b' is the object of the Player2() Class.

def check(): # Now Let's Compare The Outcomes of the Player 1 and PLayer 2
    """This Function Check the outcomes of the players to choose a winner 👑"""
    print("\nLet's Compare the Outcomes.")
    print(f"1st Player's Outcomes sum: {answer}")
    print(f"2nd Player's Outcomes sum: {answer2}")
    if answer == answer2:
        print("Tie 🤝🏻!")
    elif answer > answer2:
        print("Player 1 Won! 👑")
    else:
        print("Player 2 Won 👑")

check()