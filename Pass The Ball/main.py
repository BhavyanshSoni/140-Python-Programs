from time import sleep
from random import choice

def s(txt, delay=0.04):
    for c in txt:
        print(c, end='', flush=True)
        sleep(delay)
    print()

def welcome():
    s("Welcome to Pass the Ball 🎱")
    s("In this you have to Pass the Ball until the song stops! 🛑")
    s("And when the song stops the player with the ball will be Eliminated! 🩸☠")
    s("Let's Get Started!\n")

def main():
    while True:
        try:
            no_of_player = int(input("Number of Players>> "))
            s("\n")
            players = []
            for i in range(no_of_player):
                player_name = input(f"Name of Player {i+1}>> ")
                players.append(player_name)
            s("\nPlayers Name Saved Successfully ✅\n")

            for i in range(len(players)-1):
                print("Song Playing", end='', flush=True)
                s("...", 1.5)
                eliminated_player = choice(players)
                players.remove(eliminated_player)
                s(f"Sorry, {eliminated_player} is Eliminated ☠")
                s("Booom 💣!\n")
                players.reverse()
            for i in players:
                s(f"And The Winner is {i} 👑")
                s("Congratulations Bhavya 👑\n")

        except ValueError:
            s("Invalid Number ❌\n")


welcome()
main()