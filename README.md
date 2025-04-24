---

# AI Fitness Tracker

An intelligent fitness tracker desktop application built using Python's Tkinter GUI toolkit and Scikit-learn. It allows users to register/login, calculate BMI, receive personalized workout recommendations, log daily workout data, predict calorie burn trends using Linear Regression, and get expert fitness advice.

---

## Features

- **User Registration & Login**  
  Securely stores user profiles including name, age, weight, height, and fitness goals.

- **BMI Calculator**  
  Automatically calculates and displays BMI upon login.

- **Workout Recommendations**  
  AI-driven recommendations tailored to your fitness goal (Weight Loss, Muscle Gain, Maintain).

- **Calorie Logging**  
  Log daily calories burned from your workouts.

- **Prediction Module**  
  Uses machine learning (Linear Regression) to predict future calorie burn.

- **Expert Advice System**  
  Gives health suggestions based on BMI.

- **Update Profile**  
  Update weight and height as progress is made.

---

## Tech Stack

- **Python 3.x**
- **Tkinter** (GUI)
- **Scikit-learn** (ML Model - Linear Regression)
- **NumPy** (Numerical computations)
- **JSON** (User data storage)
- **OS** and **datetime** (System utilities)

---

## Installation

1. **Clone the repository**  
   ```bash
   git clone https://github.com/saiimmani/ai-fitness-tracker.git
   cd ai-fitness-tracker
   ```

2. **Install dependencies**  
   Make sure Python 3 is installed, then run:
   ```bash
   pip install numpy scikit-learn
   ```

3. **Run the Application**  
   ```bash
   python main.py
   ```

---

## File Structure

```
ai-fitness-tracker/
├── main.py          # Main application file
├── db.json          # JSON database storing user data
├── README.md        # Project documentation
```

---

## How it Works

1. User logs in or registers.
2. The system calculates BMI and displays it.
3. Based on user goals and BMI, the app recommends a suitable workout.
4. User logs calories after a workout session.
5. A Linear Regression model trains on past calories burned to predict the next day's burn.
6. Expert advice is provided based on BMI classification.

---

## Future Enhancements

- Export user data as CSV or PDF.
- Add nutrition and diet tracking.
- Connect to wearable fitness devices.
- Cloud-based user storage for multi-device access.

---

## Author

**Sai Immani**  
GitHub: [saiimmani](https://github.com/saiimmani)  
LinkedIn: [Sai Immani](https://www.linkedin.com/in/sai-immani)  
B.Tech CSE | Passionate about AI & Fitness Tech

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
