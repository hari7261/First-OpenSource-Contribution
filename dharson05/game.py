import random

def number_guessing_game():
    print("🎮 Welcome to the Number Guessing Game! 🎯")
    number = random.randint(1, 100)  # Computer selects a random number
    attempts = 0

    while True:
        try:
            guess = int(input("Enter your guess (1-100): "))
            attempts += 1

            if guess < number:
                print("Too low! Try again. ⬆️")
            elif guess > number:
                print("Too high! Try again. ⬇️")
            else:
                print(f"🎉 Congratulations! You guessed the number in {attempts} attempts! 🏆")
                break
        except ValueError:
            print("Invalid input! Please enter a number.")

# Start the game
number_guessing_game()
