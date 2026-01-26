from time import sleep,time # This is the modules section of the programme.
from random import *

def s(txt, d=0.035): # This is a slow print function used to print the text slower and attractive.
    for i in txt: # This for loop gives the value of variable(i) in the parameter(txt)
        print(i, end='', flush=True) # Then the variable(i) is printed without any new line and with flush=True
        sleep(d)
    print()

def main():
    s("Welcome to Tell the Number with Alphabets. => Made by Bhavyansh Soni!")
    s("How to Play?")
    s("(I) The Game will show you an alphabet!")
    s("(II) Then you should tell the number of the alphabet. Eg(A-1, H-8)")
    s("(III) You'll Will be given 10 Tries to guess the number of the alphabet in just 5 seconds!")
    s("So, Let's Get Started!\n")
    ids_of_alphabets = {
        "A" : 1, "B" : 2, "C" : 3, "D" : 4, "E" : 5, "F" : 6, "G" : 7, "H" : 8, "I" : 9, "J" : 10, "K" : 11, "L" : 12, "M" : 13, "N" : 14, "O" : 15, "P" : 16, "Q" : 17, "R" : 18, "S" : 19, "T" : 20, "U" : 21, "V" : 22, "W" : 23, "X" : 24, "Y" : 25, "Z" : 26
    }
    alphabets = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    random_alphabet = choice(alphabets)
    s(f"\nThe Alphabet is... {random_alphabet}")
    i = 0
    while i<10:
        i += 1
        try:
            start = time()
            alpha_num = int(input("(Enter Number)>> "))
            end = time()
            time_taken = end-start
            if time_taken <= 5:
                
                if alpha_num == ids_of_alphabets[random_alphabet]:
                    s("Congratulations you guessed the Number of Alphabet in...!")
                    if i > 1:
                        s(f"{i} Guesses")
                        s("Good Bye...Thanks For Playing")
                        break
                    if i == 1:
                        s(f"{i} Guess")
                        s("Good Bye...Thanks For Playing")
                        break
                elif alpha_num < ids_of_alphabets[random_alphabet]:
                    s("Enter a Higher Number Please!")
                elif alpha_num > ids_of_alphabets[random_alphabet]:
                    s("Enter a Lower Numebr Please!")
            else:
                s("Sorry, You must give the answer under 15 seconds")

        except ValueError:
            s("Invalid Number of Alphabet ❌!")
            s("Try Again")
main()