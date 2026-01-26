import keyboard
import pyperclip
import json
import os
from datetime import datetime
import sys
from threading import Thread
import time
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw

class ClipboardManager:
    def __init__(self):
        self.clips = ["" for _ in range(9)]  # Initialize 9 empty clips
        self.save_file = "clips.txt"
        self.load_clips()
        self.running = True
        
        # Create a simple icon for the system tray
        self.create_icon()
        
    def create_icon(self):
        """Create a system tray icon"""
        # Create a simple square icon
        image = Image.new('RGB', (64, 64), color='white')
        dc = ImageDraw.Draw(image)
        dc.rectangle([16, 16, 48, 48], fill='black')
        
        # Create the menu
        menu = Menu(
            MenuItem("Running...", self.dummy),
            MenuItem("Exit", self.stop_application)
        )
        
        # Create the icon with a shorter name
        self.icon = Icon(
            "Clipboard",  # Shortened name
            image,
            "Multi-Clipboard",  # Shortened tooltip
            menu
        )
        
    def dummy(self):
        """Dummy function for status menu item"""
        pass
        
    def setup_hotkeys(self):
        """Setup all hotkeys"""
        try:
            # Setup hotkeys for saving clips (Ctrl+C+number)
            for i in range(9):
                keyboard.add_hotkey(f'ctrl+c+{i+1}', lambda x=i: self.save_clip(x))
                
            # Setup hotkeys for pasting clips (Ctrl+V+number)
            for i in range(9):
                keyboard.add_hotkey(f'ctrl+v+{i+1}', lambda x=i: self.paste_clip(x))
        except Exception as e:
            self.show_notification("Error", f"Failed to setup hotkeys: {e}")
            
    def show_notification(self, title, message):
        """Show a system tray notification with truncated message"""
        try:
            # Truncate message if too long
            if len(message) > 50:
                message = message[:47] + "..."
            self.icon.notify(title, message)
        except Exception:
            # If notification fails, just continue silently
            pass
            
    def save_clip(self, index):
        """Save current clipboard content to specified index"""
        try:
            current_clip = pyperclip.paste()
            if current_clip:  # Only save if there's actual content
                self.clips[index] = current_clip
                self.save_to_file()
                preview = current_clip[:30] + "..." if len(current_clip) > 30 else current_clip
                self.show_notification(f"Slot {index + 1}", f"Saved: {preview}")
        except Exception as e:
            self.show_notification("Error", f"Failed to save: {str(e)[:50]}")
            
    def paste_clip(self, index):
        """Paste content from specified index to clipboard"""
        try:
            if self.clips[index]:
                pyperclip.copy(self.clips[index])
                keyboard.write(self.clips[index])
        except Exception as e:
            self.show_notification("Error", f"Failed to paste: {str(e)[:50]}")
            
    def save_to_file(self):
        """Save all clips to file with timestamps"""
        try:
            with open(self.save_file, 'a', encoding='utf-8') as f:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"\n=== Clips saved at {timestamp} ===\n")
                for i, clip in enumerate(self.clips, 1):
                    if clip:
                        f.write(f"Clip {i}: {clip}\n")
        except Exception as e:
            self.show_notification("Error", f"Failed to save file: {str(e)[:50]}")
            
    def load_clips(self):
        """Load clips from file if it exists"""
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    # Get the last saved clips
                    clips_section = []
                    for line in reversed(lines):
                        if line.startswith("==="):
                            break
                        if line.startswith("Clip "):
                            clips_section.append(line)
                    
                    # Parse clips
                    for clip_line in reversed(clips_section):
                        try:
                            index = int(clip_line[5]) - 1
                            content = clip_line[8:].strip()
                            self.clips[index] = content
                        except:
                            continue
        except Exception as e:
            self.show_notification("Error", f"Failed to load clips: {str(e)[:50]}")
    
    def stop_application(self):
        """Stop the application gracefully"""
        try:
            self.running = False
            self.icon.stop()
        finally:
            sys.exit(0)
        
    def run(self):
        """Run the application"""
        try:
            # Setup hotkeys in a separate thread
            hotkey_thread = Thread(target=self.setup_hotkeys)
            hotkey_thread.daemon = True
            hotkey_thread.start()
            
            # Show startup notification
            self.show_notification(
                "Clipboard Manager",
                "Running... Use Ctrl+C+[1-9] to save, Ctrl+V+[1-9] to paste"
            )
            
            # Run the system tray icon
            self.icon.run()
            
        except Exception as e:
            self.show_notification("Error", str(e)[:50])
            sys.exit(1)

def main():
    try:
        if not os.path.exists("clips.txt"):
            # Create empty clips file
            with open("clips.txt", "w", encoding='utf-8') as f:
                f.write("=== Ultimate Multi-Clipboard Manager ===\n")
        
        app = ClipboardManager()
        app.run()
    except Exception as e:
        print(f"Failed to start: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 