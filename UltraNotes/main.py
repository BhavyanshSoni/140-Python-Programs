
import time
import sys

# 🚀 By Bhavyansh Soni | Enhanced by GOD

colors = ["\033[91m", "\033[92m", "\033[93m", "\033[94m", "\033[95m", "\033[96m"]
reset = "\033[0m"
text = "🌟 Welcome to this GOD LEVEL PROJECT! 🌟"

for i, char in enumerate(text):
    sys.stdout.write(colors[i % len(colors)] + char + reset)
    sys.stdout.flush()
    time.sleep(0.05)

print("\n✨ Add your code below! ✨")
