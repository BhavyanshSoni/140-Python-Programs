from time import sleep # <- Time module is used to support slow printing in this programme.
from random import choice # <- Random Module is used to choose an emoji(randomly).

# This is the slow print function named as 's'.
def s(txt, delay=0.04):
    for c in txt:
        print(c, end='', flush=True)
        sleep(delay)
    print()

# This is the main(Function) of the Progarmme.
def main():
    s("Welcome To The Dream Emoji Predictor!")
    s("In this you can enter your dream and the Programme will display a Emoji Randomly")
    s("Let's Get Started!")
    s("\nType 'End' in the dream to exit!") # This lines mean that if there is just 'End' in the Dream the Programme will be finished.
    emojis = [       # This is the EMOJIS list.
        "| 😀 |",
        "| 😮 |",
        "| 😡 |",
        "| 😎 |",
        "| 😂 |",
        "| 🤐 |",
        "| 😛 |",
        "| 😴 |",
        "| 🤔 |",
        "| 😆 |",
        "| 🤣 |",
        "| 😜 |",
        "| 🤑 |",
        "| 😱 |",
        "| 😭 |",
        "| 🤢 |",
        "| 😶 |"
    ]
    while True: # While loop is used to run the programme infinite times.
        dream = input("Enter Your Dream>> \n")
        if dream.lower() == "end": # This is the condition which checks if the dream contains end if yes the programme will end else the programme will preditct a random emoji from the EMOJIS(list).
            s("Thanks for using the Programme. GoodBye...")
            break
        else:
            print("Predicting Emoji", end='',flush=True)
            s("...", 0.9)
            random_emoji = choice(emojis)
            s(f"Predicted Emoji: {random_emoji}\n")
            
main() # <- The main(Function) is called here.




# ------------------------------------------------------------------END-----------------------------------------------------------------------------------------------