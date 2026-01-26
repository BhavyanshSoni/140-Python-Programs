import pyttsx3

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

names = ["Rahul", "Rohit", "Javed", "Ritika", "John", "Sharukh Khan", "Deepika"]
for name in names:
    print(f"Shoutout to {name}")
    speak(f"Shoutout to {name}")
