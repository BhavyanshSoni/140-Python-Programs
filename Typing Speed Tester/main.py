import time
import random

sentences = [
    "Python is an amazing programming language.",
    "Typing fast takes practice and focus.",
    "OpenAI builds powerful AI models.",
    "Always test your code thoroughly.",
    "Creativity meets logic in programming."
]

sentence = random.choice(sentences)
print("\n🧪 Typing Speed Test")
print("\nType the following:\n")
print("➤", sentence)
input("\nPress Enter when ready...")

start = time.time()
typed = input("\nStart typing:\n➤ ")
end = time.time()

time_taken = end - start
words = len(sentence.split())
wpm = (words / time_taken) * 60

# Accuracy calculation
correct = sum(1 for a, b in zip(sentence, typed) if a == b)
accuracy = (correct / len(sentence)) * 100

print(f"\n⏱ Time Taken: {round(time_taken, 2)}s")
print(f"⌨️ Speed: {round(wpm, 2)} WPM")
print(f"✅ Accuracy: {round(accuracy, 2)}%")
