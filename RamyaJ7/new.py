import random

# Generate a random number between 1 and 100
number_to_guess = random.randint(1, 100)

# Ask the user to guess
guess = int(input("Guess the number between 1 and 100: "))

# Check if the guess is correct
while guess != number_to_guess:
    if guess < number_to_guess:
        print("Too low! Try again.")
    else:
        print("Too high! Try again.")
    guess = int(input("Guess the number again: "))

print("Congratulations! You guessed the right number!")
