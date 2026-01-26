import sys
import time
from colorama import init, Fore, Back, Style

# Initialize colorama
init(autoreset=True)

# Key to drum mapping: key: (drum name, emoji)
DRUMS = {
    'q': ("Kick", "🥁"),
    'w': ("Snare", "🥁"),
    'e': ("Hi-Hat", "✨"),
    'a': ("Tom", "🪘"),
    's': ("Clap", "👏"),
    'd': ("Cymbal", "🔔"),
}

def get_key():
    if sys.platform == "win32":
        import msvcrt
        return msvcrt.getch().decode('utf-8').lower()
    else:
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch.lower()

def print_drum_kit(active_key=None):
    print("\nTerminal Drum Kit! Press keys to play. Press 'ESC' to quit.\n")
    for key, (name, emoji) in DRUMS.items():
        if key == active_key:
            print(f"{Back.YELLOW}{Fore.BLACK} [{key.upper()}] {name} {emoji} {Style.RESET_ALL}", end='  ')
        else:
            print(f"[{key.upper()}] {name} {emoji}", end='  ')
    print("\n")

def main():
    print_drum_kit()
    while True:
        key = get_key()
        if key == '\x1b':  # ESC to quit
            print("\nExiting Drum Kit. Bye!")
            break
        if key in DRUMS:
            # Highlight the key and show emoji
            print_drum_kit(active_key=key)
            name, emoji = DRUMS[key]
            print(f"{Fore.GREEN}You played: {name} {emoji}{Style.RESET_ALL}")
            time.sleep(0.15)  # Short delay for rhythm
            print_drum_kit()  # Reset display

if __name__ == "__main__":
    main() 