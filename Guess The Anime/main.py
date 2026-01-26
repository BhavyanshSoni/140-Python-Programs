from random import choice
from time import sleep

class Anime: # Using Object-Oriented-Programming for this game.
    def __init__(self):
        def s(txt, delay = 0.04): # Slow Prints are here to make the programme more attractive.
            for char in txt:
                print(char, end = '', flush=True)
                sleep(delay)
            print()
        
        def welcome(): # This Screen Displays the welcome screen of the game.
            s("Welcome To Guess The Anime Game!")
            s("In This game you have to guess an Anime from the Animes given by you")
            s("Let's Get Started!")

        def taking_Animes(): # This Function take Animes from the user to guess by themselves.
            global Anime_names # Anime_names(list) is global to use it in the guess_Anime(Function).
            try:
                s("\nSo Now Let's Take the Animes.")
                no_of_Animes = int(input("Enter No. of Animes.>> "))
                Anime_names = []
                if no_of_Animes <= 1: # If the number of Animes is less than 1.
                    s("❌Number should be greater than 1")
                    exit()
                else:
                    for i in range(no_of_Animes): # For loop for taking the Animes and save them in the Anime_names(list).
                        name = input("\nAnime Name.>> ")
                        Anime_names.append(name.lower())
                    s("Name Of Animes Saved ✅!\n")

            except (ValueError,KeyboardInterrupt): # ValueError and KeyboardInterrupt are used here to prevent from stopping the programme
                s("Invalid Numbers!")
                exit()
        
        def guess_Anime(): # This function usses the Anime_names(from taking_Animes(Function)) to guess the Animes by the User.
            s("The Animes are: ")
            j = 0
            for i in Anime_names:
                j = j + 1
                s(f"{j}. {i}")

            s("\nNow Let's Guess the Anime.")
            guesses = 0
            while guesses < 10: # While Loop is used to run the guessing process 10 times.
                guesses = guesses + 1
                random_Anime = choice(Anime_names)
                user_Anime = input(">> ")
                if user_Anime.lower() == random_Anime:
                    s(f"Congratulations You Guessed The Anime {random_Anime} in {guesses} guesses.")
                    s("GoodBye...")
                    break
                else:
                    s("Wrong Anime\nTry Again\n")
        welcome()
        taking_Animes()
        guess_Anime()
        # Function Calls.
a = Anime()

