# Ultimate Multi-Clipboard Manager 📋

A powerful clipboard enhancer for power users: store multiple copied items, quickly recall them with a shortcut, and never lose your important snippets again.

## ✨ Features

- Save up to 9 different clipboard items
- Quick access with hotkeys:
  - `Ctrl+C+[1-9]` to save to a specific slot
  - `Ctrl+V+[1-9]` to paste from a specific slot
- Persistent storage: all clips are saved to a text file
- System tray icon with status and notifications
- Runs silently in the background
- Automatic timestamp logging of saved clips

## 🚀 Installation

1. Make sure you have Python 3.6+ installed
2. Install the required packages:
```bash
pip install -r requirements.txt
```

## 💻 Usage

1. Run the program:
```bash
pythonw main.pyw
```
or double-click `main.pyw` in Windows Explorer

2. The program will run silently in the background with a system tray icon

3. To save a clip:
   - Copy any text (Ctrl+C)
   - Press the number (1-9) while still holding Ctrl+C
   - You'll see a notification confirming the save

4. To paste a clip:
   - Press Ctrl+V+[1-9] where [1-9] is the slot number
   - The text will be pasted at your cursor position

5. All clips are automatically saved to `clips.txt` with timestamps

6. To exit:
   - Right-click the system tray icon
   - Select "Exit"

## 📝 Notes

- The program needs to run with admin privileges to capture global hotkeys
- Clips are preserved between sessions
- System tray notifications show when clips are saved
- Full clip history is maintained in `clips.txt`
- The .pyw extension makes the program run without showing a console window

## 🛠️ Requirements

- Python 3.6+
- keyboard
- pyperclip
- pystray
- Pillow 