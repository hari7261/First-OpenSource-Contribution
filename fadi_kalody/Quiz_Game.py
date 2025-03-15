import time
from colorama import Fore, init

# Initialize colorama for colored text
init(autoreset=True)

class QuizGame:
    def __init__(self):
        self.questions = [
            {
                "question": "What is the capital of France?",
                "options": ["A. London", "B. Paris", "C. Berlin", "D. Madrid"],
                "answer": "B"
            },
            {
                "question": "Which planet is known as the Red Planet?",
                "options": ["A. Venus", "B. Mars", "C. Jupiter", "D. Saturn"],
                "answer": "B"
            },
            {
                "question": "What is 2 + 2?",
                "options": ["A. 3", "B. 4", "C. 5", "D. 6"],
                "answer": "B"
            }
        ]
        self.score = 0
        self.total_questions = len(self.questions)

    def display_welcome(self):
        print(Fore.CYAN + "\n🌟 Welcome to the Python Quiz Game! 🌟")
        print(Fore.YELLOW + f"\nYou'll be presented with {self.total_questions} questions.")
        print("Enter the letter (A/B/C/D) of your answer. Type 'SKIP' to pass a question.\n")
        time.sleep(1)

    def run_quiz(self):
        for i, q in enumerate(self.questions, 1):
            print(Fore.MAGENTA + f"\nQuestion {i}: {q['question']}")
            for option in q['options']:
                print(Fore.WHITE + option)
            
            while True:
                user_answer = input(Fore.GREEN + "\nYour answer: ").strip().upper()
                
                if user_answer == "SKIP":
                    print(Fore.YELLOW + "Question skipped!")
                    break
                if user_answer in ["A", "B", "C", "D"]:
                    if user_answer == q['answer']:
                        self.score += 1
                        print(Fore.GREEN + "✅ Correct!")
                    else:
                        print(Fore.RED + f"❌ Incorrect! Correct answer was {q['answer']}")
                    break
                else:
                    print(Fore.RED + "Invalid input! Please enter A/B/C/D or 'SKIP'")
            
            print(Fore.BLUE + f"Current Score: {self.score}/{i}")
            time.sleep(1)

    def show_results(self):
        print(Fore.CYAN + "\n📊 Quiz Complete! 📊")
        print(Fore.YELLOW + f"\nFinal Score: {self.score}/{self.total_questions}")
        percentage = (self.score / self.total_questions) * 100
        print(Fore.YELLOW + f"Percentage: {percentage:.2f}%")
        
        if percentage >= 70:
            print(Fore.GREEN + "🎉 Excellent! You aced the quiz!")
        elif percentage >= 40:
            print(Fore.YELLOW + "👍 Good effort! Keep practicing!")
        else:
            print(Fore.RED + "💪 Keep learning! You'll do better next time!")

    def play_again(self):
        choice = input(Fore.WHITE + "\nPlay again? (Y/N): ").upper()
        return choice == "Y"

# Main Program
if __name__ == "__main__":
    while True:
        game = QuizGame()
        game.display_welcome()
        game.run_quiz()
        game.show_results()
        if not game.play_again():
            print(Fore.CYAN + "\nThanks for playing! 👋")
            break