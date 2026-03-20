import os
import random

files = os.listdir("C:\\Users\\gk\\Music\\MUSIC\\")
recent_music = set()
while True:
    video_input = input("Press 'enter' to play next and 'q' to quit:")
    music = random.choice(files)
    if video_input == "":
        os.startfile(f"C:\\Users\\gk\\Music\\MUSIC\\{music}")
        recent_music.add(music)
        files.remove(music)
    elif video_input.lower() == "q":
        break
    else:
        print(f"Invalid! Press 'enter' or 'q': ")
        print("\n"*50)
