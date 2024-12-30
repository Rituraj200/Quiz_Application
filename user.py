import tkinter as tk
from tkinter import ttk
import json
import os

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Application")
        self.root.geometry("800x600")

        self.users_scores = self.load_scores()
        self.current_user = None

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

        self.global_timer = 300  # 5 minutes in seconds
        self.global_timer_job = None

        self.login_screen()

    def load_scores(self):
        """Load the user scores from a file"""
        if os.path.exists("user_scores.json"):
            with open("user_scores.json", "r") as file:
                users_scores = json.load(file)
                for user, data in users_scores.items():
                    if "quiz_history" not in data:
                        data["quiz_history"] = []
                    if "quiz_attempts" not in data:
                        data["quiz_attempts"] = 0
                    if "max_scores" not in data:
                        data["max_scores"] = {"Python": 0, "DSA": 0, "DBMS": 0}  # Store scores for each quiz topic
                return users_scores
        return {}

    def save_scores(self):
        """Save the updated user scores to a file"""
        with open("user_scores.json", "w") as file:
            json.dump(self.users_scores, file, indent=4)

    def load_questions(self):
        """Load questions from the local file"""
        with open('questions.json', 'r') as file:
            return json.load(file)

    def login_screen(self):
        """Display the login screen with separate panels for Admin and User"""
        self.clear_screen()

        tk.Label(self.root, text="Login", font=("Arial", 30, "bold")).pack(pady=20)

        login_frame = ttk.Frame(self.root)
        login_frame.pack(pady=30)

        # User Login Panel
        user_frame = ttk.Frame(login_frame)
        user_frame.grid(row=0, column=0, padx=50)
        tk.Label(user_frame, text="User Login", font=("Arial", 20, "bold")).pack(pady=10)

        tk.Label(user_frame, text="Username:", font=("Arial", 15)).pack()
        self.user_username_entry = tk.Entry(user_frame, font=("Arial", 15))
        self.user_username_entry.pack(pady=10)

        tk.Label(user_frame, text="Password:", font=("Arial", 15)).pack()
        self.user_password_entry = tk.Entry(user_frame, font=("Arial", 15), show="*")
        self.user_password_entry.pack(pady=10)

        tk.Button(user_frame, text="Login", font=("Arial", 15), command=self.user_login).pack(pady=10)

        # Registration Button
        tk.Button(self.root, text="New User? Register Here", font=("Arial", 15), command=self.register).pack(pady=10)

    def clear_screen(self):
        """Clear the screen"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def user_login(self):
        """Handle user login"""
        username = self.user_username_entry.get()
        password = self.user_password_entry.get()
        user_data = self.users_scores.get(username)

        if username and password:
            if user_data and user_data.get("password") == password:
                self.current_user = username
                if self.users_scores[username]["quiz_attempts"] >= 1:
                    tk.Label(self.root, text="You have already attempted the quiz.", font=("Arial", 15), fg="red").pack(pady=10)
                else:
                    self.quiz_screen()
            else:
                tk.Label(self.root, text="Invalid username or password!", font=("Arial", 15), fg="red").pack(pady=10)
        else:
            tk.Label(self.root, text="Username and password are required!", font=("Arial", 15), fg="red").pack(pady=10)

    def register(self):
        """Handle user registration"""
        username = self.user_username_entry.get()
        password = self.user_password_entry.get()

        if username:
            if username not in self.users_scores:
                self.users_scores[username] = {
                    "password": password,
                    "quiz_history": [],
                    "quiz_attempts": 0,
                    "max_scores": {"Python": 0, "DSA": 0, "DBMS": 0},  # Store scores for each quiz topic
                }
                self.save_scores()
                tk.Label(self.root, text="Registration successful! Please login.", font=("Arial", 15), fg="green").pack(pady=10)
            else:
                tk.Label(self.root, text="Username already exists!", font=("Arial", 15), fg="red").pack(pady=10)
        else:
            tk.Label(self.root, text="Username cannot be empty!", font=("Arial", 15), fg="red").pack(pady=10)

    def quiz_screen(self):
        """Display the quiz screen where the user can select a topic"""
        self.clear_screen()

        tk.Label(self.root, text="Select Quiz Topic", font=("Arial", 30, "bold")).pack(pady=20)

        topic_frame = ttk.Frame(self.root)
        topic_frame.pack(pady=30)

        # Topic Buttons (Python, DSA, DBMS)
        topics = ["Python", "DSA", "DBMS"]
        for topic in topics:
            tk.Button(
                topic_frame,
                text=topic,
                font=("Arial", 20),
                command=lambda t=topic: self.start_quiz(t)
            ).pack(pady=10)

    def start_quiz(self, topic):
        """Start the quiz by loading questions from the file"""
        questions_data = self.load_questions()
        if topic in questions_data:
            self.questions = questions_data[topic]
            for question in self.questions:
                question["topic"] = topic  # Add the topic to each question
            self.start_quiz_screen()

    def start_quiz_screen(self):
        """Start the quiz with the loaded questions"""
        self.clear_screen()

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

        self.frames = []
        self.timer_labels = {}
        self.score = 0
        self.current_question = 0
        self.incorrect_answers = []

        self.create_frames()

        self.start_global_timer()

    def create_frames(self):
        """Create frames for each question"""
        for index, q in enumerate(self.questions):
            frame = ttk.Frame(self.notebook)
            self.frames.append(frame)
            self.notebook.add(frame, text=f"Q{index + 1}")
            self.add_question(frame, q, index)

    def add_question(self, frame, question_data, index):
        """Add question and options to a frame"""
        tk.Label(
            frame,
            text=question_data["question"],
            font=("Arial", 20, "bold"),
            wraplength=800,
        ).pack(pady=20)

        for option in question_data["options"]:
            tk.Button(
                frame,
                text=option,
                font=("Arial", 15),
                bg="light blue",
                command=lambda opt=option, idx=index: self.check_answer(opt, question_data["answer"], idx),
            ).pack(pady=10)

        timer_label = tk.Label(
            frame, text="Time Left: 5:00", font=("Arial", 15, "bold"), fg="red"
        )
        timer_label.pack(pady=10)
        self.timer_labels[frame] = timer_label

        tk.Button(
            frame,
            text="Skip Question",
            font=("Arial", 15),
            bg="yellow",
            command=self.skip_question
        ).pack(pady=20)

        # Exit Quiz Button
        tk.Button(
            frame,
            text="Exit Quiz",
            font=("Arial", 15),
            bg="red",
            command=self.exit_quiz
        ).pack(pady=10)

    def check_answer(self, selected, correct, index):
        """Check if the answer is correct"""
        frame = self.frames[index]
        if selected == correct:
            tk.Label(
                frame,
                text="Correct!",
                font=("Arial", 20, "bold"),
                bg="green",
                fg="yellow",
            ).pack(pady=20)
            self.score += 1
        else:
            tk.Label(
                frame,
                text="Incorrect!",
                font=("Arial", 20, "bold"),
                bg="red",
                fg="yellow",
            ).pack(pady=20)
            self.incorrect_answers.append({
                "question": self.questions[index]["question"],
                "selected": selected,
                "correct": correct
            })
        self.show_next_question(index)

    def skip_question(self):
        """Skip current question and show next one"""
        self.show_next_question(self.current_question)

    def show_next_question(self, current_index):
        """Show next question in the quiz"""
        if current_index < len(self.questions) - 1:
            self.notebook.select(self.frames[current_index + 1])
            self.current_question = current_index + 1
        else:
            self.show_results()

    def start_global_timer(self):
        """Start the global timer for the entire quiz"""
        self.global_timer_job = self.root.after(1000, self.update_global_timer)

    def update_global_timer(self):
        """Update the global timer every second"""
        minutes = self.global_timer // 60
        seconds = self.global_timer % 60
        timer_text = f"Time Left: {minutes:02d}:{seconds:02d}"

        for frame, timer_label in self.timer_labels.items():
            timer_label.config(text=timer_text)

        if self.global_timer > 0:
            self.global_timer -= 1
            self.global_timer_job = self.root.after(1000, self.update_global_timer)
        else:
            self.show_results()

    def show_results(self):
        """Show quiz results after completion"""
        self.clear_screen()
        tk.Label(
            self.root,
            text=f"Quiz Completed!\nYour Score: {self.score}/{len(self.questions)}",
            font=("Arial", 25, "bold"),
        ).pack(pady=20)

        topic = self.questions[0]["topic"]  # Get the topic from the first question
        if self.score > self.users_scores[self.current_user]["max_scores"][topic]:
            self.users_scores[self.current_user]["max_scores"][topic] = self.score
            self.save_scores()

        self.users_scores[self.current_user]["quiz_attempts"] += 1
        self.save_scores()

        # Buttons for Reviewing Incorrect Answers and Viewing Leaderboard
        tk.Button(self.root, text="Review Incorrect Answers", font=("Arial", 15), command=self.review_incorrect_answers).pack(pady=10)
        tk.Button(self.root, text="Leaderboard", font=("Arial", 15), command=lambda: self.show_leaderboard(topic)).pack(pady=10)

        # Exit Button
        tk.Button(self.root, text="Exit Quiz", font=("Arial", 15), command=self.exit_quiz).pack(pady=20)

    def review_incorrect_answers(self):
        """Display the incorrect answers in a scrollable frame"""
        review_window = tk.Toplevel(self.root)
        review_window.title("Review Incorrect Answers")

        canvas = tk.Canvas(review_window)
        scrollbar = ttk.Scrollbar(review_window, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        review_frame = ttk.Frame(canvas)

        canvas.create_window((0, 0), window=review_frame, anchor="nw")
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Column-wise layout for incorrect answers with centered alignment
        for incorrect in self.incorrect_answers:
            frame = ttk.Frame(review_frame)
            frame.pack(pady=10, fill="x", anchor="center")
            
            tk.Label(frame, text=f"Q: {incorrect['question']}", font=("Arial", 15), fg="black").pack(pady=5)
            tk.Label(frame, text=f"Your Answer: {incorrect['selected']}", font=("Arial", 15), fg="red").pack(pady=5)
            tk.Label(frame, text=f"Correct Answer: {incorrect['correct']}", font=("Arial", 15), fg="blue").pack(pady=5)

        review_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def show_leaderboard(self, topic):
        """Display the leaderboard for a specific topic"""
        leaderboard_window = tk.Toplevel(self.root)
        leaderboard_window.title(f"{topic} Leaderboard")

        canvas = tk.Canvas(leaderboard_window)
        scrollbar = ttk.Scrollbar(leaderboard_window, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        leaderboard_frame = ttk.Frame(canvas)

        canvas.create_window((0, 0), window=leaderboard_frame, anchor="nw")
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Filter users based on the topic and sort by max score
        sorted_users = sorted(
            [(user, data["max_scores"].get(topic, 0)) for user, data in self.users_scores.items() if data["max_scores"].get(topic, 0) > 0],
            key=lambda x: x[1], reverse=True
        )

        row = 0  # To track the row for grid placement
        for idx, (user, score) in enumerate(sorted_users, start=1):
            frame = ttk.Frame(leaderboard_frame)
            frame.grid(row=row, pady=10, sticky="w", padx=10, columnspan=2)  # Grid for the frame

            # Display ranking number and score directly
            tk.Label(frame, text=f"{idx}. {user}: {score}", font=("Arial", 15), fg="black").grid(row=0, column=0, sticky="w", padx=10)

            row += 1

        leaderboard_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def exit_quiz(self):
        """Exit the quiz and return to login screen"""
        self.clear_screen()
        self.login_screen()

# Create the main window
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
