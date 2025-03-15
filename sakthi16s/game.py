import random

# Function to get the user's choice
def get_user_choice():
    while True:
        choice = input("Enter 'rock', 'paper', or 'scissors': ").lower()
        if choice in ['rock', 'paper', 'scissors']:
            return choice
        else:
            print("Invalid input. Please enter 'rock', 'paper', or 'scissors'.")

# Function to get the computer's choice
def get_computer_choice():
    return random.choice(['rock', 'paper', 'scissors'])

# Function to determine the winner
def determine_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        return "It's a tie!"
    elif (user_choice == 'rock' and computer_choice == 'scissors') or \
         (user_choice == 'scissors' and computer_choice == 'paper') or \
         (user_choice == 'paper' and computer_choice == 'rock'):
        return "You win!"
    else:
        return "You lose!"

# Main function to play the game
def play_game():
    print("Welcome to Rock, Paper, Scissors!")
    
    while True:
        user_choice = get_user_choice()  # Get user input
        computer_choice = get_computer_choice()  # Get computer's random choice

        print(f"\nYou chose {user_choice}.")
        print(f"The computer chose {computer_choice}.\n")
        
        # Determine and display the winner
        result = determine_winner(user_choice, computer_choice)
        print(result)
        
        # Ask the user if they want to play again
        play_again = input("\nDo you want to play again? (yes/no): ").lower()
        if play_again != 'yes':
            print("Thanks for playing! Goodbye.")
            break

# Run the game
if __name__ == "__main__":
    play_game()
