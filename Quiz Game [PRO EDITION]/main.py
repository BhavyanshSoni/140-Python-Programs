from time import sleep, strftime
import random

def s(txt, delay=0.04):
    for char in txt:
        print(char, end='', flush=True)
        sleep(delay)
    print()

numbers = list(range(1, 100))
operators = ["+", "-", "*",]

def add_score(con):
    year = strftime("%y")
    mon = strftime("%m")
    day = strftime("%d")
    try:
        with open("E:\\Python Programmes\\Quiz Game [PRO EDITION]\\score.txt", "w") as f:
            f.write(f"{year}-{mon}-{day}>> Your Xp is {con}")
        s("Score saved successfully!")
    except PermissionError:
        s("Could not save score to file (permission denied)")
    except Exception as e:
        s(f"Error saving score: {e}")

def main():
        s("Welcome to the QUIZ GAME!")
        s("In This You have to answer 10 Maths questions and you will get +10 XP per question")
        s("Let's Get Started!\n")
        xp = 0
        i = 0
        while i < 3:
            try:
                i += 1
                num1 = random.choice(numbers)
                num2 = random.choice(numbers)
                operator = random.choice(operators)
                question = f"{num1} {operator} {num2}"
                answer = eval(question)
                s(f"Question {i}: {question}")
                s("Answer>> ")
                user_answer = int(input())
                if user_answer == answer:
                    s("Correct!")
                    s("Added 10 XP")
                    xp += 10
                else:
                    s("Incorrect!")
            except ValueError as v:
                s("Invalid")
        s(f"Your XP is {xp}")
        add_score(xp)

main()
