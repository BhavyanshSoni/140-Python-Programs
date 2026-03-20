import os
from time import sleep

def s(txt, d=0.03):
    for i in txt:
        print(i, end='', flush=True)
        sleep(d)
    print()

def create_file():
    if os.path.exists("C:\\Users\\gk\\3D Objects\\Python Programmes\\Pricer\\Info.txt"):
        pass
    else:
        with open("Info.txt","w") as f:
            f.write("")
        

def welcome():
    s("Welcome to 'Pricer' made by --> Bhavyansh Soni!") # Giving credit to the creator.
    # Instructions below:
    s("\nIn this Program you can enter a product and its current Price, It could be anything like, medicines, daily use materials.")
    s("For Example:- Gold 10g -> 2 Lakh($, Rs. etc...)") 
    s("\nLet's Get Started!") # Getting Started!
    
def main(): # The main function of the Program
    global item_and_price
    try:
        times = int(input("How Many Products do you wish to add:- "))
        
    except:
        s("\nInvalid Input! Try Something different...")
        return
    item_and_price = {}
    for i in range(times):
        s(f"\n\n----------Product {i+1}----------")
        item = input("\nEnter the Item's Name:- ")
        amount = input(f"\nEnter Amount of {item}:- ")
        price = input(f"\nEnter Price of {amount} {item}:- ")
        item_amount = f"{amount} {item}"
        item_and_price.update({item_amount:price})
    save()

def save():
    global save_file
    save_file = "Info.txt"
    s("\nSaving! in a File...")
    # Use append mode so new entries are added instead of overwriting the file
    with open(save_file, "a") as f:
        for i,j in zip(item_and_price.keys(),item_and_price.values()):
            f.write(f"=========================\n{i} --> {j}\n=========================\n")
    choosing_tasks()

def see_file():
    global save_file
    save_file = "Info.txt"
    with open(save_file) as f:
        prices = f.read()
    if "-->" in prices:
        s("\nTaking a look at the File...\n")
        with open(save_file) as f:
            content = f.read()
            s(f"{content}")
        choosing_tasks()
    else:
        s("\nSorry, But you haven't Provided any Data of your Products and its Prices Yet.")
        s("Provide some data...\n")
        main()


def choosing_tasks():
    try:
        print("\n|-----------------------------------------------|")
        s("|What do you Want to do:\t\t\t|")
        s("|1. Save Products with Prices.\t\t\t|")
        s("|2. Take a look on the Products and Prices File.|")
        s("|3. Exit\t\t\t\t\t|")
        print("|-----------------------------------------------|")
        choose = int(input('\n>> '))

        if choose == 1:
            main()
        elif choose == 2:
            see_file()
        elif choose == 3:
            s("Exiting GoodBye... Thanks for using this Program...")
            exit()
    except ValueError:
        s("Invalid Choice! Try Again...")
        return

create_file()
choosing_tasks()
