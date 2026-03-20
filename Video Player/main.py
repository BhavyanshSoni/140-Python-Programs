import os
import random

files = os.listdir("C:\\Users\\gk\\Videos\\EDITS\\")
recent_videos = set()
while True:
    video_input = input("Press 'enter' to play next and 'q' to quit:")
    video = random.choice(files)
    if video_input == "":
        os.startfile(f"C:\\Users\\gk\\Videos\\EDITS\\{video}")
        recent_videos.add(video)
        files.remove(video)
    elif video_input.lower() == "q":
        break
    else:
        print(f"Invalid! Press 'enter' or 'q': ")
        print("\n"*50)
