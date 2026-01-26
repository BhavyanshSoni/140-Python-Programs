from random import choice
from time import sleep, strftime

def s(txt, delay = 0.04):
    for char in txt:
        print(char, end='', flush=True)
        sleep(delay)
    print()

def welcome():
    s("Welcome to the game!")
    s("In this game you will be able to solve the questions and Answer Who Am I?")
    s("Let's Get Started!")

questions_and_answers = {
    "I have keys but no doors. What am I?": "keyboard",
    "The more you take from me, the bigger I get. What am I?": "hole",
    "I am full of holes, but I still hold water. What am I?": "sponge",
    "I have hands but I cannot clap. What am I?": "clock",
    "I go up but never come down. What am I?": "age",
    "The more you use me, the sharper I get. What am I?": "brain",
    "I run but I never walk. What am I?": "river",
    "I have a face but no eyes, nose, or mouth. What am I?": "clock",
    "You can break me without touching me. What am I?": "promise",
    "I can fly without wings. What am I?": "time"
}

def add_to_file(con):
    year = strftime("%y")
    mon = strftime("%m")
    day = strftime("%d")
    with open("score.txt", "w") as f:
        f.write(f"{year}-{mon}-{day} You Guessed The Answer in: {con} Round(s)")

def game():
    s("\nNow Answer The Question!\n")
    rounds = 0
    while rounds<5:
        rounds += 1
        s(f"-------------Round {rounds}/5-------------")
        random_ques = choice(list(questions_and_answers.keys()))

        s(random_ques)
        answer = input("Answer>> ")
        if answer.lower() == questions_and_answers[random_ques]:
            s("Correct Answer!")
            add_to_file(rounds)
            break
        else:
            s("Wrong Answer\n")
welcome()
game()