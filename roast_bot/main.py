import random

def slow_print(t, d=0.04):
    for i in t:
        print(i, end='', flush=True)


ROASTS = [
    "Hey {}, you're so slow, Internet Explorer feels bad for you! 🐌",
    "{} is so clumsy, they tripped over a wireless network! 🌐",
    "I heard {} tried to catch fog... they mist! ☁️",
    "{}'s room is so messy, their WiFi signal gets lost in it! 📶",
    "Hey {}, you're like a broken pencil... pointless! ✏️",
    "{} is so indecisive, they took 20 minutes to pick a Netflix show... and still didn't watch anything! 📺",
    "I bet {}'s password is 'password123'... and they still forget it! 🔑",
    "{} is so lazy, their spirit animal is a sloth on vacation! 🦥",
    "Hey {}, you use Internet Explorer as your main browser, don't you? 🌍",
    "{} is so predictable, even their random number generator returns 1! 🎲",
    "{} types so slow, autocorrect gives up! ⌨️",
    "I heard {} puts their phone in airplane mode to send a pigeon mail! ✈️",
    "{} is so old school, they still have a MySpace account! 👴",
    "Hey {}, your selfies are so bad, even your phone's front camera feels sorry! 📱"
]

def generate_roast(name):
    """Generate a random roast with the given name."""
    return random.choice(ROASTS).format(name)

def main():
    slow_print("🔥 Welcome to the Personal Roast Bot! 🔥",)
    slow_print("Get ready for some light-hearted roasts!",)
    slow_print("Type 'quit' to exit",)
    
    while True:
        name = input("\nWho should I roast? ")
        if name.lower() == 'quit':
            break
            
        slow_print("\nPreparing a spicy roast... 🌶️")
        slow_print("3... 2... 1...",d=0.5)
        slow_print(generate_roast(name),)
    

if __name__ == "__main__":
    main() 