import os
import time
import hashlib
from collections import defaultdict
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# 🔥 Configure Default Folder and Delay
FOLDERS = ["E:/Python Programmes"]  # 🟢 Change folder path here
DELAY = 2  # seconds

# Emojis for event types
EMOJIS = {
    'created': '🟢',
    'modified': '🟡',
    'deleted': '🔴',
}

# Colors for event types
COLORS = {
    'created': Fore.GREEN,
    'modified': Fore.YELLOW,
    'deleted': Fore.RED,
}

def hash_file(path):
    """Return a hash of the file contents, or None if not a file."""
    try:
        with open(path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception:
        return None

def scan_folder(folder):
    """Return a dict of {filepath: (mtime, hash)} for all files in folder recursively."""
    state = {}
    for root, _, files in os.walk(folder):
        for name in files:
            path = os.path.join(root, name)
            try:
                mtime = os.path.getmtime(path)
                file_hash = hash_file(path)
                state[path] = (mtime, file_hash)
            except Exception:
                continue
    return state

def print_event(event_type, path):
    emoji = EMOJIS[event_type]
    color = COLORS[event_type]
    print(f"{color}{emoji} {event_type.upper():<9} {Style.RESET_ALL}{path}")

def main(folders, delay=2):
    prev_state = defaultdict(dict)
    # Initial scan
    for folder in folders:
        if not os.path.isdir(folder):
            print(Fore.RED + f"❌ Folder not found: {folder}")
            continue
        prev_state[folder] = scan_folder(folder)

    print(Fore.CYAN + Style.BRIGHT + f"\n🔍 Tracking changes in: {', '.join(folders)} (every {delay}s)\n")

    while True:
        time.sleep(delay)
        for folder in folders:
            curr_state = scan_folder(folder)
            prev_files = prev_state[folder]
            curr_files = curr_state

            # Detect created and modified files
            for path in curr_files:
                if path not in prev_files:
                    print_event('created', path)
                elif curr_files[path][1] != prev_files.get(path, (None, None))[1]:
                    print_event('modified', path)

            # Detect deleted files
            for path in prev_files:
                if path not in curr_files:
                    print_event('deleted', path)

            prev_state[folder] = curr_files

if __name__ == "__main__":
    print(Fore.CYAN + Style.BRIGHT + "\n🗂️  File Change Tracker (Auto Mode) 🚀\n")
    main(FOLDERS, DELAY)
