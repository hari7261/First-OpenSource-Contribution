import tkinter as tk
from tkinter import messagebox
import random

# Sample questions for the quiz (You can add more questions)
questions = [
    {
        "question": "What is the capital of France?",
        "options": ["Berlin", "Madrid", "Paris", "Rome"],
        "answer": "Paris"
    },
    {
        "question": "What is the largest planet in our solar system?",
        "options": ["Earth", "Jupiter", "Mars", "Saturn"],
        "answer": "Jupiter"
    },
    {
        "question": "What is 5 + 7?",
        "options": ["11", "12", "13", "14"],
        "answer": "12"
    },
    {
        "question": "What is the chemical symbol for water?",
        "options": ["O2", "H2O", "CO2", "NaCl"],
        "answer": "H2O"
    },
    {
        "question": "Who wrote 'Harry Potter'?",
        "options": ["J.R.R. Tolkien", "George R.R. Martin", "J.K. Rowling", "Mark Twain"],
        "answer": "J.K. Rowling"
    }
]

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Educational Quiz App")
        self.root.geometry("400x400")
        
        # Initialize quiz variables
        self.score = 0
        self.current_question = 0
        self.selected_option = tk.StringVar()
        
        # Label to display the question
        self.question_label = tk.Label(root, text="", font=("Arial", 16), wraplength=350)
        self.question_label.pack(pady=20)

        # Radio buttons for options
        self.options_frame = tk.Frame(root)
        self.options_frame.pack()

        self.option_buttons = []
        for i in range(4):
            button = tk.Radiobutton(self.options_frame, text="", variable=self.selected_option, value="", font=("Arial", 14))
            button.pack(anchor='w')
            self.option_buttons.append(button)

        # Next button to go to the next question
        self.next_button = tk.Button(root, text="Next", command=self.check_answer, font=("Arial", 14))
        self.next_button.pack(pady=20)

        # Start the quiz
        self.show_question()

    def show_question(self):
        # Get the current question and options
        question_data = questions[self.current_question]
        self.question_label.config(text=question_data["question"])
        
        for i, option in enumerate(question_data["options"]):
            self.option_buttons[i].config(text=option, value=option)
        
        self.selected_option.set(None)  # Reset the selected option

    def check_answer(self):
        # Check if an option is selected
        if not self.selected_option.get():
            messagebox.showwarning("No Selection", "Please select an answer!")
            return
        
        # Get the current question and check the selected answer
        question_data = questions[self.current_question]
        if self.selected_option.get() == question_data["answer"]:
            self.score += 1
        
        # Move to the next question or end the quiz
        self.current_question += 1
        if self.current_question < len(questions):
            self.show_question()
        else:
            self.end_quiz()

    def end_quiz(self):
        # Show the final score when the quiz ends
        messagebox.showinfo("Quiz Over", f"Your final score is: {self.score}/{len(questions)}")
        self.root.quit()

# Main function to run the app
def main():
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
