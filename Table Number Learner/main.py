from time import sleep
from turtle import right

def s(txt, delay=0.04):
    for char in txt:
        print(char, end='', flush=True)
        sleep(delay)
    print()

def welcome_screen():
    s("Welcome To The Table Learner!")
    s("Here You Can Learn Number Tables!")
    s("So You Won't Forget them!")
    s("Let's Get Started!")

def practice_table():
    s("\nYou Chose To Practice Tables!")
    s("Enter which Table You Want To Practice!")
    tables = []
    no_table = int(input("(Which Table To Practice)>> "))
    right_table = True
    for i in range(1,11):
        table = int(input(f"({no_table} X {i})?>> "))
        tables.append(table)
    
    for a,n in zip(tables,range(1,11)):
        if no_table*n == a:
            right_table = True
        else:
            right_table = False
    if right_table == True:
        s("Correct Table!")
    else:
        s("Incorrect Table!")
            

def learn_tables():
    s("\nYou Chose To Learn Tables!")
    s("Enter Which Table You Want To Learn!")
    try:
        table = int(input(">> "))
        for i in range(1,11):
            s(f"{table} X {i} = {table*i}", delay=0.08)
        s("Thanks For Using This Programme!")
    except ValueError as v:
        s("Invalid Number ❌")

def menu():
    s("\nDo you want to:")
    s("1. Practice Tables!")
    s("2. Learn Tables!")
    s("3. Exit!\n")
    try:
        action = int(input("(1-3)>> "))
        if action == 1:
            practice_table()
        elif action == 2:
            learn_tables()
        else:
            s("Exiting... GoodBye...")
            exit()
    except ValueError as v:
        s("Invalid! ❌\nPlease enter a valid number")


welcome_screen()
menu()