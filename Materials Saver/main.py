from calendar import month
from time import sleep, strftime

def s(txt, delay=0.04):
    for char in txt:
        print(char, end= '', flush=True)
        sleep(delay)
    print()

def welcome_screen():
    s("Welcome To Materials List Saver!")
    s("Made By Bhavyansh Soni!")
    s("Here You Can Save Your Daily Materials List!")
    s("Let's Get Started!")

def save():
    year = strftime("%Y-")
    month = strftime("%m-")
    date = strftime("%d")
    file_name = year+month+date
    materials = input("(Materials)>> ")
    with open(f"{file_name}.txt", "w") as f:
        f.write(materials)

    
def menu():
    while True:
        s("Do You Want To: ")
        s("1. Save List!")
        s("2. Exit!")
        try:
            action = int(input("(1-2)>> "))
            if action == 1:
                save()
            elif action == 2:
                s("Exiting... GoodBye...")
                break
        except ValueError as v:
            s("Invalid ❌")


welcome_screen()
menu()