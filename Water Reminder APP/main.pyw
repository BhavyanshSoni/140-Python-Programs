import time
from plyer import notification
import pyttsx3

engine = pyttsx3.init()
INTERVEL = 27

def speak(text):
    engine.say(text)
    engine.runAndWait()

def notify_message():
    while True:
        speak("Bhavyansh Time To Drink WATER")
        notification.notify(
            title = "Yoo Bhavyansh Bro 😎.",
            message = "DRINK 🥤 WATER 🌊 AND STAY 😄 HYDRATED!",
            timeout = 5
        )
        time.sleep(INTERVEL)

notify_message()