import os
import random
import string
import time
import sys
from datetime import datetime

def slow_print(text, delay=0.03):
    """Print text with a slow, dramatic effect"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def slow_input(prompt, delay=0.03):
    """Print prompt slowly and get input"""
    slow_print(prompt, delay)
    return input()

def generate_alternate_content(original_content):
    """Generate alternate content by shuffling letters within words"""
    lines = original_content.split('\n')
    alternate_lines = []
    
    for line in lines:
        if line.strip():  # Skip empty lines
            words = line.split()
            shuffled_words = []
            
            for word in words:
                if len(word) > 2:  # Only shuffle words with more than 2 characters
                    # Keep first and last letter in place, shuffle the middle
                    if len(word) > 3:
                        first_letter = word[0]
                        last_letter = word[-1]
                        middle_letters = list(word[1:-1])
                        random.shuffle(middle_letters)
                        shuffled_word = first_letter + ''.join(middle_letters) + last_letter
                    else:
                        # For 3-letter words, just shuffle the middle letter
                        shuffled_word = word[0] + word[2] + word[1]
                else:
                    shuffled_word = word
                
                shuffled_words.append(shuffled_word)
            
            alternate_lines.append(' '.join(shuffled_words))
        else:
            alternate_lines.append(line)
    
    return '\n'.join(alternate_lines)

def save_file():
    """Allow user to save a file"""
    slow_print("\n" + "="*50, 0.01)
    slow_print("SAVE FILE", 0.05)
    slow_print("="*50, 0.01)
    
    filename = slow_input("Enter filename to save (without extension): ", 0.02).strip()
    if not filename:
        filename = f"file_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    filename = filename + ".txt"
    
    slow_print(f"\nEnter your content (press Enter twice to finish):", 0.02)
    slow_print("-" * 30, 0.01)
    
    lines = []
    while True:
        line = input()
        if line == "" and lines and lines[-1] == "":
            break
        lines.append(line)
    
    content = '\n'.join(lines[:-1])  # Remove the last empty line
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        slow_print(f"\n✅ File saved successfully: {filename}", 0.02)
        return filename, content
    except Exception as e:
        slow_print(f"\n❌ Error saving file: {e}", 0.02)
        return None, None

def create_alternate_file(original_filename, original_content):
    """Create an alternate version of the file"""
    slow_print("\n" + "="*50, 0.01)
    slow_print("CREATE ALTERNATE FILE", 0.05)
    slow_print("="*50, 0.01)
    
    slow_print("Generating alternate dimension content...", 0.03)
    time.sleep(1)
    
    # Generate alternate filename
    name, ext = os.path.splitext(original_filename)
    alternate_filename = f"{name}_alternate{ext}"
    
    # Generate alternate content
    alternate_content = generate_alternate_content(original_content)
    
    try:
        with open(alternate_filename, 'w', encoding='utf-8') as f:
            f.write(alternate_content)
        slow_print(f"✅ Alternate file created: {alternate_filename}", 0.02)
        
        # Show preview
        slow_print(f"\n📄 PREVIEW OF ALTERNATE FILE:", 0.03)
        slow_print("-" * 40, 0.01)
        slow_print(alternate_content, 0.01)
        slow_print("-" * 40, 0.01)
        
        return alternate_filename
    except Exception as e:
        slow_print(f"❌ Error creating alternate file: {e}", 0.02)
        return None

def view_files():
    """View all saved files"""
    slow_print("\n" + "="*50, 0.01)
    slow_print("SAVED FILES", 0.05)
    slow_print("="*50, 0.01)
    
    txt_files = [f for f in os.listdir('.') if f.endswith('.txt')]
    
    if not txt_files:
        slow_print("No .txt files found in current directory.", 0.02)
        return
    
    for i, filename in enumerate(txt_files, 1):
        slow_print(f"{i}. {filename}", 0.02)
    
    try:
        choice = slow_input(f"\nEnter file number to view (1-{len(txt_files)}): ", 0.02).strip()
        if choice.isdigit() and 1 <= int(choice) <= len(txt_files):
            filename = txt_files[int(choice) - 1]
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            slow_print(f"\n📄 CONTENT OF {filename}:", 0.03)
            slow_print("-" * 40, 0.01)
            slow_print(content, 0.01)
            slow_print("-" * 40, 0.01)
        else:
            slow_print("Invalid choice.", 0.02)
    except Exception as e:
        slow_print(f"Error reading file: {e}", 0.02)

def main():
    """Main program loop"""
    slow_print("🌌 ALTERNATE DIMENSION FILE GENERATOR", 0.05)
    slow_print("="*50, 0.01)
    slow_print("Create files and generate alternate versions!", 0.03)
    time.sleep(0.5)
    
    while True:
        slow_print("\n" + "="*50, 0.01)
        slow_print("MAIN MENU", 0.05)
        slow_print("="*50, 0.01)
        slow_print("1. Save a new file", 0.02)
        slow_print("2. Create alternate file", 0.02)
        slow_print("3. View saved files", 0.02)
        slow_print("4. Exit", 0.02)
        
        choice = slow_input("\nEnter your choice (1-4): ", 0.02).strip()
        
        if choice == '1':
            filename, content = save_file()
            if filename and content:
                slow_print(f"\n💡 Tip: Use option 2 to create an alternate version of '{filename}'", 0.02)
        
        elif choice == '2':
            txt_files = [f for f in os.listdir('.') if f.endswith('.txt')]
            if not txt_files:
                slow_print("\n❌ No .txt files found. Please save a file first (option 1).", 0.02)
                continue
            
            slow_print(f"\nAvailable files:", 0.02)
            for i, f in enumerate(txt_files, 1):
                slow_print(f"{i}. {f}", 0.02)
            
            try:
                file_choice = slow_input(f"\nEnter file number to create alternate (1-{len(txt_files)}): ", 0.02).strip()
                if file_choice.isdigit() and 1 <= int(file_choice) <= len(txt_files):
                    selected_file = txt_files[int(file_choice) - 1]
                    with open(selected_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    create_alternate_file(selected_file, content)
                else:
                    slow_print("Invalid choice.", 0.02)
            except Exception as e:
                slow_print(f"Error: {e}", 0.02)
        
        elif choice == '3':
            view_files()
        
        elif choice == '4':
            slow_print("\n👋 Goodbye! Thanks for using Alternate Dimension File Generator!", 0.03)
            time.sleep(1)
            break
        
        else:
            slow_print("❌ Invalid choice. Please enter 1-4.", 0.02)

if __name__ == "__main__":
    main() 