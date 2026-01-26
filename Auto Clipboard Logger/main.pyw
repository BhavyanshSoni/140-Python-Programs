import pyperclip
import time
import os

file_path = "E:\\Python Programmes\\Auto Clipboard Logger\\clipboard_history.txt"
prev_text = ""

def save_to_file(text):
    with open(file_path, "a", encoding="utf-8") as f:
        timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]")
        spaced_text = " ".join(list(text.replace("\n", "⏎")))
        f.write(f"{timestamp} {spaced_text}\n")

print("📋 Clipboard logger started. Running in background...")

while True:
    try:
        current_text = pyperclip.paste()
        if current_text != prev_text and current_text.strip() != "":
            save_to_file(current_text)
            prev_text = current_text
        time.sleep(1)  # Check every 1 second
    except KeyboardInterrupt:
        break
