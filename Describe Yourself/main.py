from time import sleep as sl

def s(txt,delay=0.035):
    for i in txt:
        print(i, end='',flush=True)
        sl(delay)
    print()

def main():
    s("Welcome to Describe Yourself --> Made By [Bhavyansh Soni]")
    s("Here you have to enter your name and the programme will describe a word of all of the alphabets of your name.")
    s("Let's Get Started!\n")
    words_and_aplhas = {
        "A": " mazing",
        "B": " rave",
        "C": " ool",
        "D": " aring",
        "E": " agered",
        "F": " antastic",
        "G": " angster",
        "H": " erioc",
        "I": " nvinicible",
        "J": " oker",
        "K": " ing",
        "L": " ucky",
        "M": " allecious",
        "N": " ice",
        "O": " rdinary",
        "P": " ebble",
        "Q": " ueen",
        "R": " oaster",
        "S": " uperstar",
        "T": " opper",
        "U": " nderstander",
        "V": " enerable",
        "W": " aver",
        "X": " treme",
        "Y": " are",
        "Z": " ebra"
    }
    name = input("Enter your Name:- ")
    for i in name:
        if i.upper() in words_and_aplhas.keys():
                s(f"{i.upper()}{words_and_aplhas[i.upper()]}")
        else:
            s("Invalid Name ❌")
            exit()

main()

