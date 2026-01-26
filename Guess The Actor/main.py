from random import choice
from time import sleep

class Actor: # Using Object-Oriented-Programming for this game.
    def __init__(self):
        def s(txt, delay = 0.04): # Slow Prints are here to make the programme more attractive.
            for char in txt:
                print(char, end = '', flush=True)
                sleep(delay)
            print()
        
        def welcome(): # This Screen Displays the welcome screen of the game.
            s("Welcome To Guess The Actor Game!")
            s("In This game you have to guess an actor from the actors given by you")
            s("Let's Get Started!")

        def taking_actors(): # This Function take actors from the user to guess by themselves.
            global actor_names # actor_names(list) is global to use it in the guess_actor(Function).
            try:
                s("\nSo Now Let's Take the Actors Hollywood/Bollywood")
                no_of_actors = int(input("Enter No. of actors.>> "))
                actor_names = []
                if no_of_actors <= 1: # If the number of actors is less than 1.
                    s("❌Number should be greater than 1")
                    exit()
                else:
                    for i in range(no_of_actors): # For loop for taking the actors and save them in the actor_names(list).
                        name = input("\nActor Name.>> ")
                        actor_names.append(name.lower())
                    s("Name Of Actors Saved ✅!\n")

            except (ValueError,KeyboardInterrupt): # ValueError and KeyboardInterrupt are used here to prevent from stopping the programme
                s("Invalid Numbers!")
                exit()
        
        def guess_actor(): # This function usses the actor_names(from taking_actors(Function)) to guess the actors by the User.
            s("The Actors are: ")
            j = 0
            for i in actor_names:
                j = j + 1
                s(f"{j}. {i}")

            s("\nNow Let's Guess the actor.")
            guesses = 0
            while guesses < 10: # While Loop is used to run the guessing process 10 times.
                guesses = guesses + 1
                random_actor = choice(actor_names)
                user_actor = input(">> ")
                if user_actor.lower() == random_actor:
                    s(f"Congratulations You Guessed The Actor {random_actor} in {guesses} guesses.")
                    s("GoodBye...")
                    break
                else:
                    s("Wrong Actor\nTry Again\n")
        welcome()
        taking_actors()
        guess_actor()
        # Function Calls.
a = Actor()

