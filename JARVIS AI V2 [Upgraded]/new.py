import speech_recognition as sr

print("Available microphones:")
for i, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"{i}: {name}")

r = sr.Recognizer()
with sr.Microphone() as source:
    print("🎧 Say something...")
    audio = r.listen(source)
    print("Got it, recognizing...")

try:
    text = r.recognize_google(audio)
    print("You said:", text)
except Exception as e:
    print("Error:", e)
