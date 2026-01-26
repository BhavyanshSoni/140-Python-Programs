# Folder-based structure:
# ULTIMATE STUDY ASSISTANT/
#   Class 6/
#     maths.json, science.json, ...
#   Class 7/
#     maths.json, science.json, ...
#   ...

import os
import json
import time
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CLASSES = [f"Class {i}" for i in range(6, 13)]
SUBJECTS = ["computer.json", "hindi.json", "maths.json", "science.json", "english.json"]


def select_class():
    print("\nWelcome to the ULTIMATE STUDY ASSISTANT!")
    print("Please select your class:")
    for idx, c in enumerate(CLASSES, 1):
        print(f"{idx}. {c}")
    while True:
        choice = input("Enter the number for your class: ")
        if choice.isdigit() and 1 <= int(choice) <= len(CLASSES):
            return CLASSES[int(choice)-1]
        else:
            print("Invalid choice. Please enter a valid number.")
            time.sleep(1)

def main_menu():
    print("\nWhat would you like to do?")
    print("1. Solve Problems")
    print("2. Take Exam")
    print("3. Exit")
    while True:
        choice = input("Enter your choice (1-3): ")
        if choice in ['1', '2', '3']:
            return choice
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
            time.sleep(1)

def list_subjects(class_folder):
    path = os.path.join(BASE_DIR, class_folder)
    files = [f for f in os.listdir(path) if f.endswith('.json')]
    if not files:
        print("No subject files found for this class. Please check your folders.")
        time.sleep(1.5)
        return []
    return files

def select_subject_file(class_folder):
    files = list_subjects(class_folder)
    if not files:
        return None
    print(f"\nSelect a subject:")
    for idx, f in enumerate(files, 1):
        print(f"{idx}. {f.replace('.json','').capitalize()}")
    while True:
        choice = input("Enter the number for your subject: ")
        if choice.isdigit() and 1 <= int(choice) <= len(files):
            return files[int(choice)-1]
        else:
            print("Invalid choice. Please enter a valid number.")
            time.sleep(1)

def load_questions(class_folder, subject_file):
    path = os.path.join(BASE_DIR, class_folder, subject_file)
    if not os.path.exists(path):
        print(f"No questions found for {subject_file.replace('.json','').capitalize()} in {class_folder}.")
        time.sleep(1.5)
        return []
    with open(path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except Exception:
            print("Error reading questions file. Please check the file format.")
            return []

def solve_problems(class_folder):
    subject_file = select_subject_file(class_folder)
    if not subject_file:
        return
    questions = load_questions(class_folder, subject_file)
    if not questions:
        print("No questions found in this subject.")
        time.sleep(1.5)
        return
    random.shuffle(questions)
    for idx, prob in enumerate(questions, 1):
        print(f"\nQ{idx}: {prob['question']}")
        for opt in ['A', 'B', 'C', 'D']:
            print(f"   {opt}. {prob['options'].get(opt, '')}")
        ans = input("Your answer (A/B/C/D, or Q to quit): ").strip().upper()
        if ans == 'Q':
            print("Exiting practice mode.")
            break
        if ans == prob['correct']:
            print("Correct!")
        else:
            print(f"Wrong! Correct answer: {prob['correct']}")
            if prob.get('explanation'):
                print(f"Explanation: {prob['explanation']}")
        time.sleep(1)
    input("\nPractice session finished. Press Enter to return to the menu...")

def take_exam(class_folder):
    print(f"\nPreparing exam for {class_folder}...")
    subject_files = list_subjects(class_folder)
    if not subject_files:
        print("No subjects found for this class. Please check your folders.")
        time.sleep(1.5)
        return
    exam_questions = []
    for subject_file in subject_files:
        questions = load_questions(class_folder, subject_file)
        if not questions:
            continue
        selected = random.sample(questions, min(10, len(questions)))
        for q in selected:
            exam_questions.append((subject_file.replace('.json','').capitalize(), q))
    if not exam_questions:
        print("No questions available for exam. Please check your subject files.")
        time.sleep(1.5)
        return
    print(f"Exam has {len(exam_questions)} questions from {len(subject_files)} subjects. Total marks: 100.")
    time.sleep(2)
    score = 0
    marks_per_question = 100 / len(exam_questions)
    for idx, (subject, prob) in enumerate(exam_questions, 1):
        print(f"\nQ{idx} [{subject}]: {prob['question']}")
        for opt in ['A', 'B', 'C', 'D']:
            print(f"   {opt}. {prob['options'].get(opt, '')}")
        ans = input("Your answer (A/B/C/D): ").strip().upper()
        if ans == prob['correct']:
            print("Correct!")
            score += marks_per_question
        else:
            print(f"Wrong! Correct answer: {prob['correct']}")
            if prob.get('explanation'):
                print(f"Explanation: {prob['explanation']}")
        time.sleep(1)
    print(f"\nExam finished! Your score: {round(score,2)} / 100")
    input("Press Enter to return to the menu...")

def main():
    class_folder = select_class()
    while True:
        choice = main_menu()
        if choice == '1':
            solve_problems(class_folder)
        elif choice == '2':
            take_exam(class_folder)
        elif choice == '3':
            print("Thank you for using the ULTIMATE STUDY ASSISTANT. Goodbye!")
            time.sleep(1)
            return
        else:
            print("Invalid choice. Try again.")
            time.sleep(1)

if __name__ == "__main__":
    main() 