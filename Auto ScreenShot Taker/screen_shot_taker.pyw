import pyautogui
import time
import os

save_dir = "E:\\Python Programmes\\Auto ScreenShot Taker\\screenshots"
interval = 60  # in seconds

# Create folder if not exists
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

print("📸 Screenshot service started...")

while True:
    timestamp = time.strftime("%Y_%m_%d-%H_%M_%S")
    file_path = os.path.join(save_dir, f"screenshot_{timestamp}.png")
    screenshot = pyautogui.screenshot()
    screenshot.save(file_path)
    time.sleep(interval)
