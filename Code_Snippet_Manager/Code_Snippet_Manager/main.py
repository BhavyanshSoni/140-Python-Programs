import json
import os
import time
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

SNIPPET_FILE = 'snippets.json'

CATEGORY_EMOJIS = {
    'python': '🐍',
    'javascript': '🟨',
    'sql': '🗄️',
    'html': '🌐',
    'css': '🎨',
    'bash': '💻',
    'c++': '💠',
    'java': '☕',
    'other': '📦'
}

# Load or initialize snippets
if os.path.exists(SNIPPET_FILE):
    with open(SNIPPET_FILE, 'r', encoding='utf-8') as f:
        snippets = json.load(f)
else:
    snippets = []

def save_snippets():
    with open(SNIPPET_FILE, 'w', encoding='utf-8') as f:
        json.dump(snippets, f, indent=2, ensure_ascii=False)

def pause():
    time.sleep(1)

def print_menu():
    print(Fore.CYAN + Style.BRIGHT + '\n=== Code Snippet Manager ===')
    print(Fore.YELLOW + '[1] Add Snippet')
    print(Fore.GREEN + '[2] View All Snippets')
    print(Fore.MAGENTA + '[3] Search by Tag')
    print(Fore.RED + '[4] Delete Snippet')
    print(Fore.WHITE + '[5] Exit')

def add_snippet():
    print(Fore.YELLOW + Style.BRIGHT + '\n--- Add New Snippet ---')
    title = input(Fore.WHITE + 'Title: ')
    print(Fore.WHITE + 'Available tags: ' + ', '.join([f"{v} {k}" for k, v in CATEGORY_EMOJIS.items()]))
    tag = input(Fore.WHITE + 'Tag: ').strip().lower()
    if tag not in CATEGORY_EMOJIS:
        tag = 'other'
    print(Fore.WHITE + 'Enter your code (end with a single line containing only "END"):')
    code_lines = []
    while True:
        line = input()
        if line.strip() == 'END':
            break
        code_lines.append(line)
    code = '\n'.join(code_lines)
    snippets.append({'title': title, 'tag': tag, 'code': code})
    save_snippets()
    print(Fore.GREEN + 'Snippet added successfully!')
    pause()

def view_snippets():
    if not snippets:
        print(Fore.RED + Style.BRIGHT + '\nNo snippets found! Please add some snippets first.')
        return
    print(Fore.GREEN + Style.BRIGHT + f'\nTotal Snippets: {len(snippets)}')
    for idx, snip in enumerate(snippets, 1):
        emoji = CATEGORY_EMOJIS.get(snip.get('tag', 'other').lower(), CATEGORY_EMOJIS['other'])
        print(Fore.YELLOW + f"[{idx}] {emoji} {snip['title']} ({snip['tag']})")
        print(Fore.WHITE + snip['code'])
        print(Fore.CYAN + '-'*40)
    pause()

def search_snippets():
    if not snippets:
        print(Fore.RED + Style.BRIGHT + '\nNo snippets to search!')
        return
    view_snippets()  # Show all snippets before searching
    tag = input(Fore.MAGENTA + 'Enter tag to search: ').strip().lower()
    found = [s for s in snippets if s.get('tag', 'other').lower() == tag]
    if not found:
        print(Fore.RED + f'No snippets found for tag "{tag}".')
    else:
        print(Fore.GREEN + f'\nSnippets for tag "{tag}":')
        for idx, snip in enumerate(found, 1):
            emoji = CATEGORY_EMOJIS.get(snip.get('tag', 'other').lower(), CATEGORY_EMOJIS['other'])
            print(Fore.YELLOW + f"[{idx}] {emoji} {snip['title']} ({snip['tag']})")
            print(Fore.WHITE + snip['code'])
            print(Fore.CYAN + '-'*40)
    pause()

def delete_snippet():
    if not snippets:
        print(Fore.RED + Style.BRIGHT + '\nNo snippets to delete!')
        return
    view_snippets()  # Show all snippets before deleting
    try:
        idx = int(input(Fore.RED + 'Enter the number of the snippet to delete: '))
        if 1 <= idx <= len(snippets):
            removed = snippets.pop(idx - 1)
            save_snippets()
            print(Fore.GREEN + f'Snippet "{removed["title"]}" deleted!')
        else:
            print(Fore.RED + 'Invalid number!')
    except ValueError:
        print(Fore.RED + 'Please enter a valid number!')
    pause()

def main():
    while True:
        print_menu()
        choice = input(Fore.BLUE + 'Choose an option: ')
        if choice == '1':
            add_snippet()
        elif choice == '2':
            view_snippets()
        elif choice == '3':
            search_snippets()
        elif choice == '4':
            delete_snippet()
        elif choice == '5':
            print(Fore.CYAN + 'Goodbye!')
            break
        else:
            print(Fore.RED + 'Invalid choice!')
        pause()

if __name__ == '__main__':
    main() 