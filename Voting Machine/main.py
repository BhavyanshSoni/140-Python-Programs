from time import sleep
from random import choice

def s(txt, delay=0.04): # This is slow_print(Function).Used to print a text slowly .
    for char in txt:
        print(char, end='', flush=True)
        sleep(delay)
    print()


# This is Welcome(Function). To print the welcome screen of the PROGRAMME.
def welcome():
    s("Welcome To Voting Machine!")
    s("In this you have to select 3 candidates and Vote one of them!")
    s("Let's Get Started!\n")

# This is the main(Function) of the Programme. This Programme select 3 candidates and give them random votes!
def main():
    # Try and except is used to prevent from the KeyboardInterrupt that can happen.
    try:
        candidates = {}
        for i in range(3):
            name = input(f"Name of Candidate {i+1}>> ")
            candidates.update({name:choice(list(range(1,101)))})
        j = 0
        s(f"The Candidates are")
        for i in candidates:
            j = j + 1
            s(f"{j}. {i} - {candidates[i]} Votes")
        

    except KeyboardInterrupt:
        s("Invalid Number!")

welcome()
main()
# <-- Here Functions are Called.