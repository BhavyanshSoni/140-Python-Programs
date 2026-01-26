import random
from utils import slow_print, print_signature

# Alien language components
PREFIXES = ['zx', 'kl', 'vr', 'th', 'qz', 'nx', 'yx']
MIDDLES = ['oo', 'aa', 'ee', 'ii', 'ux', 'ax']
SUFFIXES = ['or', 'ax', 'ix', 'ux', 'oz', 'ax']
PUNCTUATION = ['!?', '...', '?!', '!!', '~', '??']

def generate_alien_word():
    """Generate a random alien word."""
    word = (
        random.choice(PREFIXES) +
        random.choice(MIDDLES) +
        random.choice(SUFFIXES)
    )
    return word.capitalize()

def generate_alien_sentence(word_count=4):
    """Generate an alien sentence with given word count."""
    words = [generate_alien_word() for _ in range(word_count)]
    return ' '.join(words) + random.choice(PUNCTUATION)

def main():
    slow_print("👽 Welcome to the Alien Language Generator! 👽", color='green')
    slow_print("Generate random alien words and sentences.", color='yellow')
    slow_print("Type 'quit' to exit", color='yellow')
    
    while True:
        choice = input("\nGenerate (w)ord or (s)entence? ").lower()
        if choice == 'quit':
            break
            
        if choice == 'w':
            word = generate_alien_word()
            slow_print(f"\n🛸 Alien word: {word}", color='cyan')
        elif choice == 's':
            sentence = generate_alien_sentence()
            slow_print(f"\n🛸 Alien sentence: {sentence}", color='magenta')
        else:
            slow_print("\nPlease choose 'w' for word or 's' for sentence!", color='red')
    
    print_signature()

if __name__ == "__main__":
    main() 