from time import sleep
from os import makedirs

def s(txt, delay=0.01):
    for c in txt:
        print(c, end='', flush=True)
        sleep(delay)
    print()

class habbit_saver:
    def welcome(self):
        s("Welcome To Good Bad Habbits!")
        s("In this you can enter someone's Good and Bad Habbits!")
        s("Let's Get Started!\n")

    def main(self):
        name = input("\nName of the Person>> ")
        no_of_habbits = int(input("Enter Number of Habbits to save>> "))
        s(f"\nFirst Enter {no_of_habbits} Good Habbit(s) of {name}")
        gh_s = []
        for i in range(no_of_habbits):
            g_h = input(f"\nHabbit {i+1}>> ")
            gh_s.append(g_h)
        
        s(f"\nNow Enter {no_of_habbits} Bad Habbit(s) of {name}")
        bh_s = []
        for i in range(no_of_habbits):
            b_h = input(f"\nHabbit {i+1}>> ")
            bh_s.append(b_h)
        
        person = makedirs(f"{name}")
        s(f"\n{name}'s Habbits:")
        j = 0
        s("\nGood Habbit(s)")
        for i in gh_s:
            j += 1
            s(f"{j}. {i}")
            with open(f"{name}\\Good_Habbits.txt", "a") as f:
                f.write(f"{j}. {i}\n")

        s("\nBad Habbit(s)")
        k = 0
        for habbits in bh_s:
            k += 1
            s(f"{k}. {habbits}")
            with open(f"{name}\\Bad_Habbits.txt", "a") as f:
                f.write(f"{k}. {habbits}\n")


a = habbit_saver()
a.welcome()
a.main()

again = input("\nWant to Save Again(Y/N)>> ")
if again.lower() == "y":
    a.main()
else:
    s("GoodByee... Thanks for Using this Programme")
    exit()
