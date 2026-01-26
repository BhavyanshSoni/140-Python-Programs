import sys
import time
from termcolor import colored

def slow_print(text, delay=0.03, color=None):
    """Print text slowly with optional color."""
    for char in text:
        if color:
            sys.stdout.write(colored(char, color))
        else:
            sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def print_signature():
    """Print Bhavyansh Soni's signature."""
    signature = "\n" + "=" * 40 + "\n"
    signature += "Made by Bhavyansh Soni 😎🔥\n"
    signature += "=" * 40 + "\n"
    slow_print(signature, delay=0.01, color='cyan') 