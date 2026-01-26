from time import * # Modules are imported here like:- Time
from random import choice # Random
from colorama import Fore # Colorama

def s(txt, delay=0.02): # This is a slow print(Function) which is used to make the program more attractive.
    for c in txt: # This for loop makes every letter as 'c' in the text(txt)
        print(c, end='', flush=True) # And then print c with end='', flush=True
        sleep(delay)# And sleep(delay=0.02) seconds to print every leter(c) in o.o2 seconds
    print() # This line prints a blank line when the txt is completed!

def main(): # This is the main function of the game.

    # This is the welcome text of the game and instructions.
    s("Welcome to Red Light - Green Light")
    s("Here on Green Light press (m) to move and on Red Light press (s) to stop!")
    s("You Must Move or Stop in 3 seconds! otherwise you'll be eliminated!")
    s("There will be 5 Rounds!")
    s("Let's Get Started!")

    for i in range(5): # Declaring 5 Rounds of the game using a for loop which runs when 1 round of a game is completed.
        s("________________________________________")
        s(f"_______________ROUND: {i+1}/5_______________")
        s("________________________________________\n")
        
        lights = ["Red Light", "Green Light"] # This list contains the "Red Light" and "Green light"
        light = choice(lights) # This Variable chooses a light from the lights(List)

        if light == "Red Light": # This print "Red light" in red color when red light is chose by the light variable.
            s(Fore.RED+"Red Light 🚨")
        elif light == "Green Light": # This print "Green Light" in green color when green light is chose by the light variable.
            s(Fore.GREEN+"Green Light ✅")

        # This variable plays a vital role in calculating the time taken by the user in giving an input.
        start_time = time()
        m_s = input("\n(m) or (s)>> ") # This is the input where user tells the computer if they want to stop(s) or move(m).

        end_time = time()
        time_taken = end_time - start_time

        if time_taken <= 3:
            if light == "Red Light" and m_s.lower() == "s":
                s("\n\tPhew, You Stopped!")
            elif light == "Red Light" and m_s.lower() == "m":
                s("\n\tOh No, You Moved on Red Light 🚨")
            elif light == "Green Light" and m_s.lower() == "m":
                s("\n\tGosh, You Moved on the right time!")
            elif light == "Green Light" and m_s.lower() == "s":
                s("\n\tWrong Timing, You Stopped on Green Light!")
            else:
                s(Fore.MAGENTA + "\n\nWRONG KEY!")
        elif time_taken > 3:
            s("\n\nEliminated! You Pressed the Key in more than 3 seconds!")

main()