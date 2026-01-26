from time import sleep

import ast

try:
    with open("formula.txt") as f:
        content = f.read().strip()
        if content:
            name_and_formulas = ast.literal_eval(content)
        else:
            name_and_formulas = {}
except FileNotFoundError:
    name_and_formulas = {}

print("Welcome To!")
sleep(0.9)
print("The Formula Saver 📔!")
sleep(0.9)
print("Here You Can Add + Formulas 📔!")
sleep(0.9)
print("So, Let's 😀  Add Some Formulas 📔\n\n")
sleep(0.9)


def add():
    sleep(0.9)
    try:
        formula = input("Enter Formula To Add (e.g., water): ")
        formula_meaning = input(f"Enter Meaning of formula {formula}: ")
        name_and_formulas.update({formula.lower(): formula_meaning})
        with open("formula.txt", "w") as f:
            f.write(str(name_and_formulas))
        sleep(0.9)
        print(f"Added Formula {formula} with Answer {formula_meaning}\n")
        sleep(0.9)
    except (ValueError, KeyboardInterrupt):
        print("🚨 Invalid!")
        sleep(0.9)
        print("❌ Try Again!\n")
        sleep(0.9)
    

def delete():
    sleep(0.9)
    if len(name_and_formulas) == 0:
        print("The Formula File is Empty Now!")
        sleep(0.9)
        print("You Should First Add + Forumlas\n")
        sleep(0.9)
    else:
        try:
            for i in name_and_formulas.keys():
                print(f"{i}")
                sleep(0.3)
            formula = input("Enter Formula To Delete (e.g., water): ")
            if formula.lower() in name_and_formulas.keys():
                name_and_formulas.pop(formula.lower())
                with open("formula.txt", "w") as f:
                    f.write(str(name_and_formulas))
                sleep(0.9)
                print(f"Deleted {formula} From The Formula File!\n")
                sleep(0.9)
            else:
                print(f"Formula {formula} Not Found In The Formula File!\n")
                sleep(0.9)
        except (KeyboardInterrupt, KeyError):
            print("🚨 Invalid!")
            sleep(0.9)
            print("❌ Try Again!\n")
            sleep(0.9)
            
def get_meaning():
    """Get the formula_meaning of a formula from the Formula File."""
    """If the Formula File is empty, prompt the user to add Formulas first."""
    global name_and_formulas
    print("Getting Meaning Of Formula...")
    sleep(0.9)
    if len(name_and_formulas) == 0:
        print("The Formula File is Empty Now!")
        sleep(0.9)
        print("You Should First Add + Forumlas\n")
        sleep(0.9)
    else:
        try:
            print("Available Formulas:")
            for i in name_and_formulas.keys():
                print(f"{i}")
                sleep(0.3)
            formula = input("Enter Name of the Formula (e.g., H2O): ")
            if formula.lower() in name_and_formulas.keys():
                print(f"The Meaning Of {formula} is {name_and_formulas[formula.lower()]}")
                sleep(0.9)
            else:
                print(f"Formula {formula} Not Found In The Formula File!\n")
                sleep(0.9)
        except (KeyboardInterrupt, KeyError):
            print("🚨 Invalid!")
            sleep(0.9)
            print("❌ Try Again!\n")
            sleep(0.9)
    sleep(0.9)

while True:
    try:
        print("What Do You Want To Do?")
        sleep(0.9)
        print("1. Add Formula")
        sleep(0.9)
        print("2. Delete Formula")
        sleep(0.9)
        print("3. See Formula")
        sleep(0.9)
        print("4. See The Formula File")
        sleep(0.9)
        print("5. Exit\n")
        print("Enter 1-5 To Select Action\n")

        action = int(input("Enter Action: "))
        if action == 1:
            add()
        elif action == 2:
            delete()
        elif action == 3:
            get_meaning()
        elif action == 4:
            if len(name_and_formulas) == 0:
                print("The Formula File is Empty Now!")
                sleep(0.9)
                print("You Should First Add + Forumlas\n")
                sleep(0.9)
                continue
        
            else:
                print("Loading... The Formula File...")
                print("The Formula File 📔 Contains:\n")
                sleep(0.9)
                for formula, formula_meaning in name_and_formulas.items():
                    print(f"{formula}: {formula_meaning}")
                    sleep(0.3)
                print("\n")
                sleep(0.9)
                
        elif action == 5:
            print("Exiting The Formula Saver! 👋")
            sleep(0.9)
            break
        else:
            raise ValueError("Invalid Action")
        

    except ValueError as v:
        print("🚨 Invalid Action!\n\n")
        sleep(0.9)
    
