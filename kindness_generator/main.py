import random
from utils import slow_print, print_signature

ACTS_OF_KINDNESS = [
    "Send a thank you message to someone who helped you recently 💌",
    "Hold the door open for someone 🚪",
    "Give a genuine compliment to a stranger 🌟",
    "Share your snack with a friend or colleague 🍪",
    "Help someone carry their groceries 🛍️",
    "Leave a positive review for a small business 💝",
    "Pick up some litter in your neighborhood 🌍",
    "Let someone go ahead of you in line 🧍",
    "Share an umbrella with someone when it's raining ☔",
    "Write a note of appreciation to a family member ✉️",
    "Donate unused items to charity 🎁",
    "Water a neighbor's plants 🌱",
    "Share a motivational quote with someone feeling down 💭",
    "Buy coffee for the person behind you in line ☕",
    "Help a lost tourist with directions 🗺️",
    "Leave coins in a vending machine for the next person 💰",
    "Send a friend a funny meme to brighten their day 😊",
    "Give up your seat on public transport 💺",
    "Help someone take a photo at a tourist spot 📸",
    "Share your knowledge by teaching someone a skill 📚"
]

def get_random_act():
    """Get a random act of kindness."""
    return random.choice(ACTS_OF_KINDNESS)

def main():
    slow_print("💖 Welcome to Daily Random Act of Kindness! 💖", color='green')
    slow_print("Get inspired to spread kindness!", color='yellow')
    slow_print("Type 'quit' to exit", color='yellow')
    
    while True:
        user_input = input("\nPress Enter for a kind act suggestion (or 'quit' to exit): ")
        if user_input.lower() == 'quit':
            break
            
        slow_print("\nHere's your kind act for today:", color='cyan')
        slow_print(get_random_act(), color='magenta')
        slow_print("\nMake someone smile today! 😊", color='yellow')
    
    print_signature()

if __name__ == "__main__":
    main() 