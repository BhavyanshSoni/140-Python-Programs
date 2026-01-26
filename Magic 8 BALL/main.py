import random

def magic_8_ball():
    print("🎱 Welcome to Magic 8-Ball! Ask your question (or type 'quit' to exit):\n")

    answers = [
        "It is certain.",
        "Without a doubt.",
        "You may rely on it.",
        "Ask again later.",
        "Cannot predict now.",
        "Don't count on it.",
        "My reply is no.",
        "Very doubtful.",
        "Yes, definitely!",
        "Better not tell you now.",
        "Signs point to yes.",
        "Outlook not so good."
    ]

    while True:
        question = input("Your question: ")
        if question.lower() in ['quit', 'exit', 'bye']:
            print("Goodbye! May luck be with you 🍀")
            break

        if question.strip() == "":
            print("Please ask a question!")
            continue

        response = random.choice(answers)
        print("Magic 8-Ball says:", response, "\n")

if __name__ == "__main__":
    magic_8_ball()
