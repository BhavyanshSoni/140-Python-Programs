import os
import sys
import time
from PIL import Image
import pytesseract
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def print_animated(text, color=Fore.CYAN, delay=0.05):
    for char in text:
        print(color + char, end='', flush=True)
        time.sleep(delay)
    print(Style.RESET_ALL)

def print_banner():
    print(Fore.YELLOW + '🖼️  ' + Style.BRIGHT + 'Smart Screenshot to Text OCR Tool' + '  📝')
    print(Fore.MAGENTA + '---------------------------------------------' + Style.RESET_ALL)

def get_image_path():
    print(Fore.GREEN + '📂 Please enter the path to your screenshot image:')
    path = input(Fore.CYAN + '>> ')
    if not os.path.isfile(path):
        print(Fore.RED + '❌ File not found. Please check the path and try again.')
        sys.exit(1)
    return path

def show_progress():
    stages = [
        (Fore.YELLOW + '🔍 Analyzing image', 0.5),
        (Fore.YELLOW + '🔎 Extracting text', 0.5),
        (Fore.YELLOW + '📝 Finalizing', 0.5)
    ]
    for stage, t in stages:
        print(stage + '...', end='\r', flush=True)
        time.sleep(t)
    print(' ' * 30, end='\r')  # Clear line

def highlight_text(text):
    # Highlight keywords and numbers for demo
    words = text.split()
    highlighted = []
    for word in words:
        if word.isdigit():
            highlighted.append(Fore.CYAN + word + Style.RESET_ALL)
        elif word.isupper() and len(word) > 2:
            highlighted.append(Fore.GREEN + word + Style.RESET_ALL)
        else:
            highlighted.append(Fore.WHITE + word + Style.RESET_ALL)
    return ' '.join(highlighted)

def main():
    print_banner()
    img_path = get_image_path()
    show_progress()
    try:
        img = Image.open(img_path)
    except Exception as e:
        print(Fore.RED + f'❌ Error opening image: {e}')
        sys.exit(1)
    print_animated('🤖 Running OCR...', Fore.YELLOW)
    try:
        text = pytesseract.image_to_string(img)
    except Exception as e:
        print(Fore.RED + f'❌ OCR failed: {e}')
        sys.exit(1)
    print_animated('✅ Text extraction complete!', Fore.GREEN)
    print(Fore.MAGENTA + '\n--- Recognized Text ---\n' + Style.RESET_ALL)
    print(highlight_text(text))
    print(Fore.MAGENTA + '\n----------------------' + Style.RESET_ALL)
    print(Fore.YELLOW + '💾 Would you like to save the text to a file? (y/n)')
    if input(Fore.CYAN + '>> ').strip().lower() == 'y':
        out_path = os.path.splitext(img_path)[0] + '_ocr.txt'
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(Fore.GREEN + f'✅ Text saved to {out_path}')
    print(Fore.BLUE + '👋 Thank you for using Smart Screenshot to Text!')

if __name__ == '__main__':
    main()


