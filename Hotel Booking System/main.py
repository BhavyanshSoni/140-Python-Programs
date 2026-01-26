# Modules are  Called Here <--
import os
from time import sleep
from random import choice

# This is slow print function used to print text in a more attractive way.
def s(txt, delay=0.04): 
    for c in txt:
        print(c, end = '', flush=True)
        sleep(delay)
    print()

# This is Book Room(Function) used to let the user book a room in "BED AND BREAKFAST" HOTEL.
def book_room():
    s("You Chose to book a room.")
    name = input("(Name)>> ")
    room_no = choice(list(range(1,101)))
    os.makedirs(name)
    with open(f"{name}/{name}.txt", "w") as f:
        f.write(f"Your Room is {room_no} {name}.")
        s(f"Your Room is {room_no}. Here is your Room Key 🔑 {name}")

# This is checkout(Function) used to check out from the hotel. This function take input from user like name and their room no to checkout.
def checkout():
    try:
        s("So You want to check out!")
        name = input("Name>> ")
        co_room = int(input("Room Number>>  "))
        with open(f"{name}/{name}.txt") as f:
            con = f.read()

        if str(co_room) in con and name in con:
            s(f"Successfully✅ Checked Out...\nVisit Again {name}.")
            exit() # exit() is used so that the programme won't run after checking out.
        else:
            s(f"Sorry.\nInvalid Room No {co_room} and {name}")
    except ValueError: # try and except are used to prevent from ValueError.
        s("Invalid Room No.")

# This is menu(Function) or main(Funciton) of the Programme. This function displays the options user can do in the Programme like Book a room, Checkout or Exit!
def menu():
    while True: # While True is for printing the Menu Infinite Times.
        try:
            s("\nWelcome To Our Hotel 'BED AND BREAKFAST'\n")
            s("Do you want to?")
            s("1. Book a Room!")
            s("2. Checkout!")
            s("3. Exit!")

            ask = int(input("(1/3)>> "))
            if ask == 1:
                book_room()
            elif ask == 2:
                checkout()
            elif ask == 3:
                s("Good Bye...!")
                exit()
        except ValueError:
            s("Invalid Choice Try Again!")

menu() 

# ---------------------------------------------END-----------------------------------------------