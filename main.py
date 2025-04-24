import tkinter as tk
from tkinter import messagebox
from sklearn.linear_model import LinearRegression
import numpy as np
import datetime
import json
import os

# -----------------------------
# Data Storage Functions
# -----------------------------
USER_DB_FILE = "db.json"

def load_users():
    if os.path.exists(USER_DB_FILE):
        with open(USER_DB_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_DB_FILE, "w") as f:
        json.dump(users, f, indent=4)

# -----------------------------
# Core Classes
# -----------------------------

class User:
    def __init__(self, name, age, weight, height, goal, history=None):
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height
        self.goal = goal
        self.history = history or []  # (date, calories)

    def bmi(self):
        return round(self.weight / ((self.height / 100) ** 2), 2)

    def log_progress(self, calories):
        today = datetime.date.today().isoformat()
        self.history.append((today, calories))

    def update_weight_height(self, weight, height):
        self.weight = weight
        self.height = height

    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "weight": self.weight,
            "height": self.height,
            "goal": self.goal,
            "history": self.history
        }


class WorkoutRecommender:
    def __init__(self, user):
        self.user = user

    def recommend(self):
        goal = self.user.goal.lower()
        bmi = self.user.bmi()

        workouts = {
            "weight_loss": [("Walk", 200), ("Jog", 300), ("HIIT", 400)],
            "muscle_gain": [("Pushups", 150), ("Weight Lifting", 250), ("Pullups", 200)],
            "maintain": [("Yoga", 100), ("Cycling", 150), ("Light Cardio", 120)]
        }

        if goal == "weight loss" and bmi >= 25:
            plan = "weight_loss"
        elif goal == "muscle gain":
            plan = "muscle_gain"
        else:
            plan = "maintain"

        return max(workouts[plan], key=lambda x: x[1])


class FitnessPredictor:
    def __init__(self, user):
        self.user = user
        self.model = LinearRegression()

    def train(self):
        if len(self.user.history) < 2:
            return None
        X = np.array([i for i in range(len(self.user.history))]).reshape(-1, 1)
        y = np.array([cal for (_, cal) in self.user.history])
        self.model.fit(X, y)
        return self.model

    def predict_next(self):
        if self.train():
            next_day = np.array([[len(self.user.history)]])
            return round(self.model.predict(next_day)[0], 2)
        return None


def expert_system_advice(user):
    bmi = user.bmi()
    if bmi >= 30:
        return "Advice: Start with walking and diet control."
    elif bmi >= 25:
        return "Advice: Mix cardio and strength training."
    elif bmi >= 18.5:
        return "Advice: Maintain current routine."
    else:
        return "Advice: Underweight. Consult a doctor."


# -----------------------------
# GUI App
# -----------------------------

class FitnessApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Fitness Tracker 🏋️")
        self.users = load_users()
        self.username = None
        self.user = None

        self.login_screen()

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login_screen(self):
        self.clear()
        tk.Label(self.root, text="Login or Sign Up", font=("Arial", 14)).pack(pady=10)

        self.username_entry = tk.Entry(self.root)
        self.entry("Username", self.username_entry)

        tk.Button(self.root, text="Continue", command=self.check_user, bg="#2196F3", fg="white").pack(pady=10)

    def entry(self, label, var):
        tk.Label(self.root, text=label).pack()
        var.pack()

    def check_user(self):
        username = self.username_entry.get()
        self.username = username

        if username in self.users:
            data = self.users[username]
            self.user = User(
                data["name"], data["age"], data["weight"], data["height"], data["goal"], data["history"]
            )
            self.show_main_screen()
        else:
            self.register_screen()

    def register_screen(self):
        self.clear()
        tk.Label(self.root, text="New User Registration", font=("Arial", 14)).pack(pady=10)

        self.name = tk.Entry(self.root); self.entry("Name", self.name)
        self.age = tk.Entry(self.root); self.entry("Age", self.age)
        self.weight = tk.Entry(self.root); self.entry("Weight (kg)", self.weight)
        self.height = tk.Entry(self.root); self.entry("Height (cm)", self.height)
        self.goal = tk.Entry(self.root); self.entry("Goal (Weight Loss / Muscle Gain / Maintain)", self.goal)

        tk.Button(self.root, text="Register", command=self.register_user, bg="#4CAF50", fg="white").pack(pady=10)

    def register_user(self):
        try:
            self.user = User(
                self.name.get(),
                int(self.age.get()),
                float(self.weight.get()),
                float(self.height.get()),
                self.goal.get()
            )
            self.users[self.username] = self.user.to_dict()
            save_users(self.users)
            self.show_main_screen()
        except:
            messagebox.showerror("Error", "Please enter valid data.")

    def show_main_screen(self):
        self.clear()
        tk.Label(self.root, text=f"Welcome {self.user.name}! 🎉", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text=f"BMI: {self.user.bmi()}").pack(pady=5)

        tk.Button(self.root, text="🏃 Recommend Workout", command=self.recommend_workout, width=25).pack(pady=5)
        tk.Button(self.root, text="📊 Log Calories Burned", command=self.log_calories, width=25).pack(pady=5)
        tk.Button(self.root, text="🔮 Predict Tomorrow's Calories", command=self.predict_calories, width=25).pack(pady=5)
        tk.Button(self.root, text="🧠 Get Expert Advice", command=self.get_advice, width=25).pack(pady=5)
        tk.Button(self.root, text="⚙️ Update Weight/Height", command=self.update_weight_height, width=25).pack(pady=5)
        tk.Button(self.root, text="🚪 Logout", command=self.login_screen, width=25).pack(pady=10)

    def recommend_workout(self):
        rec = WorkoutRecommender(self.user).recommend()
        messagebox.showinfo("Workout Recommendation", f"Recommended: {rec[0]} 🔥\nCalories: {rec[1]}")

    def log_calories(self):
        def save():
            try:
                cal = float(entry.get())
                self.user.log_progress(cal)
                self.users[self.username] = self.user.to_dict()
                save_users(self.users)
                top.destroy()
                messagebox.showinfo("Logged", "Calories logged successfully!")
            except:
                messagebox.showerror("Error", "Invalid number")

        top = tk.Toplevel(self.root)
        top.title("Log Workout")
        tk.Label(top, text="Enter Calories Burned:").pack(pady=5)
        entry = tk.Entry(top)
        entry.pack(pady=5)
        tk.Button(top, text="Log", command=save).pack(pady=5)

    def predict_calories(self):
        pred = FitnessPredictor(self.user).predict_next()
        if pred:
            messagebox.showinfo("Prediction", f"Estimated Burn Tomorrow: {pred} kcal")
        else:
            messagebox.showinfo("Prediction", "Not enough data for prediction.")

    def get_advice(self):
        advice = expert_system_advice(self.user)
        messagebox.showinfo("Expert Advice", advice)

    def update_weight_height(self):
        def save():
            try:
                new_weight = float(weight_entry.get())
                new_height = float(height_entry.get())
                self.user.update_weight_height(new_weight, new_height)
                self.users[self.username] = self.user.to_dict()
                save_users(self.users)
                top.destroy()
                messagebox.showinfo("Updated", "Weight and height updated successfully!")
            except:
                messagebox.showerror("Error", "Invalid input")

        top = tk.Toplevel(self.root)
        top.title("Update Weight and Height")
        tk.Label(top, text="Enter New Weight (kg):").pack(pady=5)
        weight_entry = tk.Entry(top)
        weight_entry.pack(pady=5)
        tk.Label(top, text="Enter New Height (cm):").pack(pady=5)
        height_entry = tk.Entry(top)
        height_entry.pack(pady=5)
        tk.Button(top, text="Update", command=save).pack(pady=10)


# -----------------------------
# Run App
# -----------------------------

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x550")
    app = FitnessApp(root)
    root.mainloop()