import time
from PIL import Image
import pytesseract
from rich.console import Console
from rich.text import Text
import re

# Mapping of Python keywords to (color, emoji)
PYTHON_KEYWORDS = {
    'def': ('cyan', '🐍'),
    'class': ('magenta', '🐍'),
    'return': ('green', '🔙'),
    'if': ('yellow', '❓'),
    'elif': ('yellow', '❓'),
    'else': ('yellow', '❓'),
    'for': ('blue', '🔄'),
    'while': ('blue', '🔄'),
    'import': ('red', '📦'),
    'from': ('red', '📦'),
    'as': ('red', '📦'),
    'try': ('bright_cyan', '🛠️'),
    'except': ('bright_cyan', '⚠️'),
    'finally': ('bright_cyan', '✅'),
    'with': ('bright_green', '📂'),
    'pass': ('grey50', '⏭️'),
    'break': ('red', '⛔'),
    'continue': ('red', '🔁'),
    'in': ('bright_blue', '🔎'),
    'not': ('bright_red', '🚫'),
    'and': ('bright_green', '➕'),
    'or': ('bright_green', '➖'),
    'lambda': ('bright_magenta', '🔣'),
    'print': ('bright_yellow', '🖨️'),
}

console = Console()

# Regex to match Python keywords as whole words
KEYWORD_REGEX = re.compile(r'\b(' + '|'.join(re.escape(k) for k in PYTHON_KEYWORDS.keys()) + r')\b')

def highlight_code_line(line):
    """Return a rich.Text object with highlighted keywords and emojis."""
    text = Text()
    last_idx = 0
    for match in KEYWORD_REGEX.finditer(line):
        start, end = match.span()
        keyword = match.group(0)
        color, emoji = PYTHON_KEYWORDS[keyword]
        # Add text before the keyword
        text.append(line[last_idx:start])
        # Add the emoji and colored keyword
        text.append(f'{emoji} {keyword}', style=color)
        last_idx = end
    text.append(line[last_idx:])  # Add the rest of the line
    return text

def main():
    image_path = input("Enter the path to your screenshot image: ").strip()
    image = Image.open(image_path)
    code_text = pytesseract.image_to_string(image)

    # Print code smoothly with highlighting
    for line in code_text.splitlines():
        highlighted = highlight_code_line(line)
        console.print(highlighted)
        time.sleep(0.25)  # Pause for readability

if __name__ == '__main__':
    main()