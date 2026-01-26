# <-- Here Modules Like(time and random) are Imported.
from time import sleep
from random import choice

# I used Object-Oriented-Programming(OOPs) to make the programme easy.
class Railway_Ticket:
    def __init__(self):
        # This is Slow Print(Function). This Function make the programme more attractive.
        def s(txt, delay=0.04):
            for c in txt:
                print(c, end = '', flush=True)
                sleep(delay)
            print()
        
        # This is book_ticket(Function). Used to let the user book the ticket. This Programme take inputs(Like, number of passangers, name of passangers) to use them in the TICKET 🎫.
        def book_ticket():
            # Try And Except is used to prevent the ValueError from the no_of_passangers(Variable[Input]).
            try: 
                s("\nLet's Book the Ticket!")
                seats = [] # This is seats list for storing the seats of Passangers.
                passangers = [] # This List stores the name of passangers.
                no_of_passangers = int(input("No. of Passangers>> "))
                for i in range(no_of_passangers):
                    passanger_name = input(f"Passanger {i+1} Name>> ")
                    passangers.append(passanger_name)
                s("Successfully ✅ Saved Names!\n")

                for i in range(no_of_passangers):
                    random_seat = choice(list(range(1,101)))
                    seats.append(random_seat)

                location_from = input("Location(From)>> ") # This input take location(From).
                location_to = input("Location(To)>> ") # This input take location(To).
                s("--------------------------------------")
                s("---------------Ticket 🎫--------------")
                s("--------------------------------------")
                s(f"Location: From ({location_from}) To ({location_to})")
                j = 0
                s("Passangers:\n")
                for i in passangers:
                    j += 1
                    s(f"{j}. {i}")
                
                s("Seats:")
                for i in seats:
                    s(f"{i}")

            except ValueError:
                s("Invalid No. of Passangers.")
        
        # This is the main(Function) of the Programme.
        def main():
            while True:
                s("\nWelcome To The Railway Booking Ticket Are!")
                s("Let's Get Started!\n")
                s("What do you want to do?")
                s("1. Book Ticket!")
                s("2. Exit!\n")
                try:
                    choice_no = int(input("(1/2)>> "))
                    if choice_no == 1:
                        book_ticket()
                    elif choice_no == 2:
                        s("GoodBye...Thanks For Visiting")
                        break # If the choice is 2 the loop will break and the programme would be ended.
                    else:
                        s("Invalid Choice Number! Try Again!")
                except ValueError:
                    s("Invalid Choice Try Again!")

        main()
a = Railway_Ticket() # <-- 'a' is the Object(Obj) of the Class(Railway_Ticket).
