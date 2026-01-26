
import json
import os
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
import joblib

DATA_FILE = "lifelens_data.json"
MODEL_FILE = "lifelens_model.joblib"

class LifeLens:
    def __init__(self):
        self.data = self.load_data()
        self.model, self.vectorizer = self.load_or_train_model()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        else:
            return {"habits": [], "moods": [], "advice_history": []}

    def save_data(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.data, f, indent=4)

    def log_habit(self):
        habit = input("Aaj ka habit batao (e.g. Exercise, Reading): ").strip().lower()
        status = input("Kya habit complete kiya? (yes/no): ").strip().lower()
        date = str(datetime.today().date())
        self.data["habits"].append({"habit": habit, "status": status, "date": date})
        self.save_data()
        print("✅ Habit record ho gaya.")

    def log_mood(self):
        mood = input("Aaj apna mood batao (e.g. Happy, Stressed, Tired): ").strip().lower()
        date = str(datetime.today().date())
        self.data["moods"].append({"mood": mood, "date": date})
        self.save_data()
        print("✅ Mood record ho gaya.")

    def prepare_training_data(self):
        # Prepare sample training data with advice labels
        texts = [
            "I am stressed and tired",
            "I feel happy and energetic",
            "I am anxious and tired",
            "I am excited and joyful",
            "Feeling low and tired",
            "I completed my exercises today",
            "I did not finish my tasks",
            "I feel calm and relaxed"
        ]
        labels = [
            "Take rest and meditate",
            "Keep up the good work",
            "Try relaxation techniques",
            "Maintain your positive energy",
            "Rest more and avoid stress",
            "Great job on exercise",
            "Try to complete your tasks",
            "Good job staying calm"
        ]
        return texts, labels

    def load_or_train_model(self):
        if os.path.exists(MODEL_FILE):
            model_data = joblib.load(MODEL_FILE)
            print("📚 Model loaded from disk.")
            return model_data["model"], model_data["vectorizer"]
        else:
            print("⚙️ Training advice model...")
            texts, labels = self.prepare_training_data()
            vectorizer = TfidfVectorizer()
            X = vectorizer.fit_transform(texts)
            model = KNeighborsClassifier(n_neighbors=3)
            model.fit(X, labels)
            joblib.dump({"model": model, "vectorizer": vectorizer}, MODEL_FILE)
            print("🎯 Model trained and saved.")
            return model, vectorizer

    def get_advice(self):
        if not self.data["moods"]:
            print("⚠️ Pehle mood log karo tab advice milegi.")
            return
        last_mood = self.data["moods"][-1]["mood"]
        habits_today = [h for h in self.data["habits"] if h["date"] == str(datetime.today().date())]
        completed_count = len([h for h in habits_today if h["status"] == "yes"])
        total_count = len(habits_today)

        input_text = f"I am {last_mood}"
        if total_count > 0 and completed_count < total_count:
            input_text += " and I did not finish all my tasks"
        elif total_count > 0 and completed_count == total_count:
            input_text += " and I completed my exercises today"

        vect = self.vectorizer.transform([input_text])
        advice = self.model.predict(vect)[0]

        print("\n🤖 LifeLens Advice:")
        print(advice)

        self.data["advice_history"].append({"date": str(datetime.today().date()), "advice": advice})
        self.save_data()

    def run(self):
        while True:
            # LifeLens header comment
            print("""
# --- LifeLens - Advanced Personal Life Coach ---
1. Log Habit
2. Log Mood
3. Take Advice 
4. Exit
""")
            choice = input("Choose: ").strip()
            if choice == "1":
                self.log_habit()
            elif choice == "2":
                self.log_mood()
            elif choice == "3":
                self.get_advice()
            elif choice == "4":
                print("👋 LifeLens Closed. Stay awesome!")
                break
            else:
                print("⚠️ Invalid choice, try again.")

if __name__ == "__main__":
    lens = LifeLens()
    lens.run()
