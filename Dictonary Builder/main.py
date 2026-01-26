from time import sleep

import ast

try:
    with open("dictonary.txt") as f:
        content = f.read().strip()
        if content:
            words_and_meanings = ast.literal_eval(content)
        else:
            words_and_meanings = {}
            
except FileNotFoundError:
    words_and_meanings = {}

print("Welcome To!")
sleep(0.9)
print("The Dictonary 📔 Builder 🔨!")
sleep(0.9)
print("Here You Can Make ⛏  Your Own Dictonary 📔!")
sleep(0.9)
print("So, Let's 😀  Make a Dictonary 📔\n\n")
sleep(0.9)


def add():
    sleep(0.9)
    try:
        word = input("Enter Word To Add (e.g., water): ")
        meaning = input(f"Enter Meaning of word {word}: ")
        words_and_meanings.update({word.lower(): meaning})
        with open("dictonary.txt", "w") as f:
            f.write(str(words_and_meanings))
        sleep(0.9)
        print(f"Added Word {word} with meaning {meaning}\n")
        sleep(0.9)
    except (ValueError, KeyboardInterrupt):
        print("🚨 Invalid!")
        sleep(0.9)
        print("❌ Try Again!\n")
        sleep(0.9)
    

def delete():
    sleep(0.9)
    if len(words_and_meanings) == 0:
        print("The Dictonary is Empty Now!")
        sleep(0.9)
        print("You Should First Add + Words\n")
        sleep(0.9)
    else:
        try:
            for i in words_and_meanings.keys():
                print(f"{i}")
                sleep(0.3)
            word = input("Enter Word To Delete (e.g., water): ")
            if word.lower() in words_and_meanings.keys():
                words_and_meanings.pop(word.lower())
                with open("dictonary.txt", "w") as f:
                    f.write(str(words_and_meanings))
                sleep(0.9)
                print(f"Deleted {word} From The Dictonary!\n")
                sleep(0.9)
            else:
                print(f"Word {word} Not Found In The Dictonary!\n")
                sleep(0.9)
        except (KeyboardInterrupt, KeyError):
            print("🚨 Invalid!")
            sleep(0.9)
            print("❌ Try Again!\n")
            sleep(0.9)
            
def get_meaning():
    """Get the meaning of a word from the dictionary."""
    """If the dictionary is empty, prompt the user to add words first."""
    global words_and_meanings
    print("Getting Meaning Of Word...")
    sleep(0.9)
    if len(words_and_meanings) == 0:
        print("The Dictonary is Empty Now!")
        sleep(0.9)
        print("You Should First Add + Words\n")
        sleep(0.9)
    else:
        try:
            print("Available words:")
            for i in words_and_meanings.keys():
                print(f"{i}")
                sleep(0.3)
            word = input("Enter Word To Get Meaning (e.g., water): ")
            if word.lower() in words_and_meanings.keys():
                print(f"The Meaning Of {word} is {words_and_meanings[word.lower()]}")
                sleep(0.9)
            else:
                print(f"Word {word} Not Found In The Dictonary!\n")
                sleep(0.9)
        except (KeyboardInterrupt, KeyError):
            print("🚨 Invalid!")
            sleep(0.9)
            print("❌ Try Again!\n")
            sleep(0.9)
    sleep(0.9)

while True:
    try:
        print("What Do You Want To Do?")
        sleep(0.9)
        print("1. Add Word")
        sleep(0.9)
        print("2. Delete Word")
        sleep(0.9)
        print("3. Get Meaning Of Word")
        sleep(0.9)
        print("4. See The Dictonary")
        sleep(0.9)
        print("5. Exit\n")
        print("Enter 1-5 To Select Action\n")

        action = int(input("Enter Action: "))
        if action == 1:
            add()
        elif action == 2:
            delete()
        elif action == 3:
            get_meaning()
        elif action == 4:
            if len(words_and_meanings) == 0:
                print("The Dictonary is Empty Now!")
                sleep(0.9)
                print("You Should First Add + Words\n")
                sleep(0.9)
                continue
        
            else:
                print("Loading... The Dictonary...")
                print("The Dictonary 📔 Contains:\n")
                sleep(0.9)
                for word, meaning in words_and_meanings.items():
                    print(f"{word}: {meaning}")
                    sleep(0.3)
                print("\n")
                sleep(0.9)
                
        elif action == 5:
            print("Exiting The Dictonary Builder! 👋")
            sleep(0.9)
            break
        else:
            raise ValueError("Invalid Action")
        

    except ValueError as v:
        print("🚨 Invalid Action!\n\n")
        sleep(0.9)
    
