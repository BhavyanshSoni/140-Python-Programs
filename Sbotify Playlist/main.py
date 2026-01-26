from time import sleep

def s(txt, delay=0.04):
    for char in txt:
        print(char, end='', flush=True)
        sleep(delay)
    print()

def welcome():
    s("Welcome To Sbotify Playlist Maker!")
    s("Here you can make your own playlist with Music Names!")
    s("Let's Get Started!")

def make_playlist():
    try:
        name = input("\nPlaylist Name>> ")
        no_of_songs = int(input("How many songs you want to add>> "))
        songs = []
        for i in range(no_of_songs):
            name_of_song = input(f"Song {i+1} Name>> ")
            songs.append(name_of_song)
        
        j = 0
        for i in songs:
            j += 1
            with open(f"{name}.txt", "a") as f:
                f.write(f"Song {j}. {i}\n")
        
        s(f"Created Playlist: {name}")

    except ValueError:
        s("Invalid Number of Songs ❌")
def main():
    while True:
        s("\nWhat do you want to do?")
        s("1. Make Playlist!")
        s("2. Exit!")
        ask = int(input("(1/2)>> "))
        if ask == 1:
            make_playlist()
        elif ask == 2:
            s("Thanks For Using Sbotify 🎵! GoodBye..!")
            break
        else:
            s("Invalid Choice Number!Try Again ❌")


welcome()
main()