# StudyMate AI - Phase 1 (GUI + Full Functionalities)
import tkinter as tk
from tkinter import messagebox, filedialog
import json
import os
import fitz  # PyMuPDF for PDF reading
import random

# Create necessary folders
if not os.path.exists("data"):
    os.makedirs("data")

# Sample Data Paths
doubt_data_file = "data/doubt_solver.json"
topic_data_file = "data/learn_topics.json"
quiz_data_file = "data/quiz_questions.json"
progress_file = "data/progress.json"

# Load or initialize data
def load_json(path, default):
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump(default, f)
    with open(path, "r") as f:
        return json.load(f)

doubt_data = load_json(doubt_data_file, {
    "What is photosynthesis?": "Photosynthesis is the process by which green plants make their food using sunlight.",
    "What is 2 + 2?": "2 + 2 = 4"
})

topic_data = load_json(topic_data_file, {
    "Science": {
        "Photosynthesis": "Photosynthesis is the process used by plants to convert light energy into chemical energy.",
        "Gravity": "Gravity is a force that pulls objects toward each other."
    },
    "Maths": {
        "Addition": "Addition is combining two or more numbers to get a total.",
        "Multiplication": "It is repeated addition."
    }
})

quiz_data = load_json(quiz_data_file, {
    "Science": [
        {"q": "What is the function of leaves?", "a": ["Photosynthesis", "Digestion", "Respiration"], "correct": "Photosynthesis"},
        {"q": "What planet is known as the red planet?", "a": ["Earth", "Mars", "Venus"], "correct": "Mars"}
    ],
    "Maths": [
        {"q": "What is 5 x 2?", "a": ["10", "7", "12"], "correct": "10"},
        {"q": "What is 9 - 3?", "a": ["6", "5", "7"], "correct": "6"}
    ]
})

progress = load_json(progress_file, {})

# Save progress
def save_progress():
    with open(progress_file, "w") as f:
        json.dump(progress, f)

# Main GUI
app = tk.Tk()
app.title("StudyMate AI")
app.geometry("500x500")


def doubt_solver():
    def solve():
        q = entry.get()
        answer = doubt_data.get(q.strip(), "Sorry, I don't know the answer to that question.")
        messagebox.showinfo("Answer", answer)

    win = tk.Toplevel(app)
    win.title("AI Doubt Solver")
    tk.Label(win, text="Enter your question:").pack()
    entry = tk.Entry(win, width=50)
    entry.pack(pady=5)
    tk.Button(win, text="Get Answer", command=solve).pack()


def learn_by_topic():
    def show_topics():
        subject = subject_var.get()
        topic_list.delete(0, tk.END)
        for topic in topic_data.get(subject, {}):
            topic_list.insert(tk.END, topic)

    def show_explanation(evt):
        subject = subject_var.get()
        topic = topic_list.get(topic_list.curselection())
        explanation = topic_data[subject][topic]
        messagebox.showinfo(topic, explanation)

    win = tk.Toplevel(app)
    win.title("Learn By Topic")

    subject_var = tk.StringVar(value="Science")
    tk.OptionMenu(win, subject_var, *topic_data.keys(), command=lambda x: show_topics()).pack()

    topic_list = tk.Listbox(win)
    topic_list.pack(pady=10)
    topic_list.bind("<<ListboxSelect>>", show_explanation)
    show_topics()


def practice_quiz():
    def next_question():
        nonlocal current_question
        if current_question >= len(questions):
            messagebox.showinfo("Quiz Over", f"Score: {score[0]} / {len(questions)}")
            progress[subject] = score[0]
            save_progress()
            win.destroy()
            return

        q_data = questions[current_question]
        question_lbl.config(text=q_data['q'])
        for i, opt in enumerate(q_data['a']):
            options[i].config(text=opt, command=lambda o=opt: check_answer(o))

    def check_answer(selected):
        nonlocal current_question
        if selected == questions[current_question]['correct']:
            score[0] += 1
        current_question += 1
        next_question()

    win = tk.Toplevel(app)
    win.title("Practice Quiz")
    subject = tk.simpledialog.askstring("Subject", "Enter Subject:")
    questions = quiz_data.get(subject, [])

    if not questions:
        messagebox.showerror("Error", "No quiz found for this subject.")
        return

    current_question = 0
    score = [0]

    question_lbl = tk.Label(win, text="", wraplength=400)
    question_lbl.pack(pady=10)
    options = [tk.Button(win) for _ in range(3)]
    for btn in options:
        btn.pack(pady=5, fill="x")

    next_question()


def view_progress():
    msg = ""
    for subj, sc in progress.items():
        msg += f"{subj}: {sc} correct answers\n"
    if not msg:
        msg = "No progress recorded yet."
    messagebox.showinfo("Progress", msg)


def extract_pdf_questions():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if not file_path:
        return

    text = ""
    doc = fitz.open(file_path)
    for page in doc:
        text += page.get_text()
    doc.close()

    found_answers = []
    for q in doubt_data:
        if q.lower() in text.lower():
            found_answers.append(f"Q: {q}\nA: {doubt_data[q]}\n")

    messagebox.showinfo("Extracted Answers", "\n\n".join(found_answers) or "No known questions found.")


def generate_timetable():
    subjects = list(quiz_data.keys())
    timetable = ""
    for i, subj in enumerate(subjects):
        timetable += f"Day {i+1}: Study {subj} for 1 hour\n"
    messagebox.showinfo("Study Timetable", timetable)

# Main Menu
btns = [
    ("AI Doubt Solver", doubt_solver),
    ("Learn By Topic", learn_by_topic),
    ("Practice Quiz", practice_quiz),
    ("Progress Tracker", view_progress),
    ("Upload PDF Questions", extract_pdf_questions),
    ("Study Time Table", generate_timetable)
]

for text, cmd in btns:
    tk.Button(app, text=text, command=cmd, width=30, height=2).pack(pady=5)

app.mainloop()