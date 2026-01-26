import cv2
import numpy as np
import pyautogui
import datetime
import time

time_duration = 86400  # None means infinite duration
def screen_record(duration=time_duration):  # seconds
    screen_size = pyautogui.size()  # auto detect screen resolution
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # for mp4 format
    filename = f"Recording_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.mp4"
    fps = 20.0

    out = cv2.VideoWriter(filename, fourcc, fps, screen_size)

    print(f"[🎥] Recording started for {duration} seconds. Saving as {filename}")
    quit = input("Enter 'quit' to stop recording!: ")
    start_time = time.time()
    while time.time() - start_time < duration:
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        out.write(frame)
        if quit.lower() == "quit":
            out.release()
            print(f"[✅] Recording complete! File saved as: {filename}")
            break
        
if __name__ == "__main__":
    screen_record(duration=time_duration)  # adjust duration here
