import time
import pyttsx3
from datetime import datetime, timedelta
from colorama import init, Fore

init(autoreset=True)

# Initialize pyttsx3
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# Hindi voice setting (may vary by system)
for voice in engine.getProperty('voices'):
    if 'hindi' in voice.name.lower() or 'hi' in voice.id.lower():
        engine.setProperty('voice', voice.id)
        break

def say(text):
    engine.say(text)
    engine.runAndWait()

def slow_print(text, color=Fore.GREEN):
    for char in text:
        print(color + char, end='', flush=True)
        time.sleep(0.02)
    print()

def main():
    print(Fore.CYAN + "\n=== 🔔 Smart School Bell System ===\n")
    start_time_str = input("Enter assembly start time (HH:MM): ")
    end_time_str = input("Enter school end time (HH:MM): ")

    # Convert to datetime
    today = datetime.today()
    start_time = datetime.strptime(start_time_str, "%H:%M").replace(year=today.year, month=today.month, day=today.day)
    end_time = datetime.strptime(end_time_str, "%H:%M").replace(year=today.year, month=today.month, day=today.day)

    total_periods = 9  # 8 + last 0 period
    period_duration = (end_time - start_time) / total_periods

    period_names = ['First ', 'Second ', 'Third ', 'Fourth ',
                    'Fifth ', 'Sixth ', 'Seventh ', 'Eighth ', 'Zero']

    current_time = start_time

    for i in range(total_periods):
        now = datetime.now()
        wait_seconds = (current_time - now).total_seconds()
        if wait_seconds > 0:
            time.sleep(wait_seconds)

        # Hindi voice announce
        say(f"{period_names[i]}, Period")

        current_time += period_duration


if __name__ == "__main__":
    main()