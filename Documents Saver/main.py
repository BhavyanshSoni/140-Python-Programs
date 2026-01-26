from time import sleep
import os

def s(txt, delay=0.03):
    for char in txt:
        print(char, end = '', flush=True)
        sleep(delay)
    print()

def welcome_screen():
    s("Welcome To Documents Saver!")
    s("Here You Can Save Your Documents!")
    s("Let's Get Started!")

def save():
    s("\nLet's Save The Document!")
    name = input("Name Of Document: ")
    content = input("What To Save: \n")
    with open(f"{name}.txt", "w") as f:
        s("Saving...", 0.1)
        f.write(content)
    s("Saved ✅!")

def delete():
    docs = os.listdir("E:\\Python Programmes\\Documents Saver")
    contents = {}
    for i in docs:
        if ".txt" in i:
            with open(f"{i}.txt") as f:
                content = f.read()
                contents.update({i:content})
    j = 0
    for i in contents.keys():
        j = j + 1
        s(f"{j}. {contents[i]}")
    

def edit():
    pass

def menu():
    while True:
        s("\nDo you want to: ")
        s("1. Save Document ✅")
        s("2. Delete Document ❌")
        s("3. Edit Document ✨")
        s("4. Exit 🔚")
        try:
            action = int(input("(1-4)>> "))
            if action == 1:
                save()
            elif action == 2:
                delete()
            elif action == 3:
                edit()
            elif action == 4:
                s("Exiting... GoodBye...", 0.07)
                break
        except ValueError as v:
            s("Invalid ❌\nPlease Try Again ❌")


welcome_screen()
menu()