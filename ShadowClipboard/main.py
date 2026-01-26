import pyperclip
import time
from rich.console import Console
from rich.panel import Panel
from rich import print as rprint
import threading
import queue
from datetime import datetime

# Initialize Rich console for fancy output
console = Console()

# Create a queue for clipboard history
clipboard_history = queue.Queue(maxsize=10)

def type_print(text, delay=0.03):
    """Print text with a cool typing effect"""
    for char in text:
        console.print(char, end='', style='bold cyan')
        time.sleep(delay)
    print()

def monitor_clipboard():
    """Silently monitor clipboard changes in the background"""
    last_value = ''
    while True:
        try:
            current_value = pyperclip.paste()
            if current_value != last_value:
                timestamp = datetime.now().strftime("%H:%M:%S")
                if clipboard_history.full():
                    clipboard_history.get()  # Remove oldest item if full
                clipboard_history.put((timestamp, current_value))
                last_value = current_value
            time.sleep(0.5)
        except:
            time.sleep(1)  # Wait if clipboard is busy

def display_history():
    """Display clipboard history with cyberpunk styling"""
    console.clear()
    type_print("🕶️  [ShadowClipboard] - Stealth Clipboard Monitor", delay=0.05)
    print()
    
    items = list(clipboard_history.queue)
    if not items:
        console.print(Panel("No clipboard activity detected yet...", 
                          style="dim cyan",
                          title="Shadow Log"))
        return

    for timestamp, content in items:
        panel = Panel(
            f"[bold cyan]{content}[/]",
            title=f"[red]{timestamp}[/]",
            style="bold white on black"
        )
        console.print(panel)
        time.sleep(0.2)  # Dramatic pause between panels

def main():
    """Main program loop with cyberpunk-themed UI"""
    # Start clipboard monitor in background
    monitor_thread = threading.Thread(target=monitor_clipboard, daemon=True)
    monitor_thread.start()

    console.clear()
    type_print("🕶️  Welcome to ShadowClipboard", delay=0.05)
    type_print("    Silently monitoring your clipboard...", delay=0.03)
    print()

    try:
        while True:
            display_history()
            time.sleep(3)  # Update every 3 seconds
            console.clear()
    except KeyboardInterrupt:
        type_print("\n💨 Fading into the shadows...", delay=0.05)

if __name__ == "__main__":
    main() 