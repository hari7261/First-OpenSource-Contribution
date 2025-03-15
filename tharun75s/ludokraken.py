import tkinter as tk
import random

# Create the game window
root = tk.Tk()
root.title("Ludo Game")

# Dimensions of the board
BOARD_SIZE = 15  # 15x15 grid for simplicity

# Colors for player tokens
PLAYER_COLORS = ['red', 'blue']

# Token positions for each player
player_positions = [0, 0]  # Two players, both starting at position 0
current_player = 0  # Track whose turn it is (0: Player 1, 1: Player 2)

# Create the game board
canvas = tk.Canvas(root, width=600, height=600, bg="white")
canvas.grid(row=0, column=0)

# Dice roll button
def roll_dice():
    global current_player

    # Roll the dice (1-6)
    dice_value = random.randint(1, 6)
    dice_label.config(text=f"Dice: {dice_value}")
    
    # Move the current player's token based on the dice value
    player_positions[current_player] += dice_value
    
    # Update the player's token position
    update_token_positions()
    
    # Check for winning condition
    if player_positions[current_player] >= BOARD_SIZE * BOARD_SIZE:
        winner = f"Player {current_player + 1} wins!"
        canvas.create_text(300, 300, text=winner, font=('Arial', 24), fill="green")
        return
    
    # Switch players
    current_player = 1 - current_player

# Draw the board grid
def draw_board():
    grid_size = 40  # Size of each cell
    for i in range(0, BOARD_SIZE):
        for j in range(0, BOARD_SIZE):
            x1, y1 = i * grid_size, j * grid_size
            x2, y2 = (i + 1) * grid_size, (j + 1) * grid_size
            canvas.create_rectangle(x1, y1, x2, y2, outline="black", width=2)
            
    # Draw the home zones for each player (in the corners)
    canvas.create_rectangle(0, 0, 3*grid_size, 3*grid_size, fill="red", outline="black")
    canvas.create_rectangle(BOARD_SIZE-3, 0, BOARD_SIZE-1, 3*grid_size, fill="blue", outline="black")
    canvas.create_rectangle(0, BOARD_SIZE-3, 3*grid_size, BOARD_SIZE-1, fill="green", outline="black")
    canvas.create_rectangle(BOARD_SIZE-3, BOARD_SIZE-3, BOARD_SIZE-1, BOARD_SIZE-1, fill="yellow", outline="black")

# Draw the tokens
def update_token_positions():
    global player_positions
    grid_size = 40
    
    # Clear previous token positions
    canvas.delete("tokens")
    
    # Draw the tokens for both players
    for i in range(2):
        x = (player_positions[i] % BOARD_SIZE) * grid_size + grid_size // 2
        y = (player_positions[i] // BOARD_SIZE) * grid_size + grid_size // 2
        canvas.create_oval(x-10, y-10, x+10, y+10, fill=PLAYER_COLORS[i], tags="tokens")

# Initialize the board and dice
def initialize_game():
    draw_board()
    update_token_positions()
    
    roll_button = tk.Button(root, text="Roll Dice", command=roll_dice)
    roll_button.grid(row=1, column=0, pady=20)
    
    global dice_label
    dice_label = tk.Label(root, text="Dice: ", font=('Arial', 14))
    dice_label.grid(row=2, column=0)

# Run the game initialization
initialize_game()

# Run the Tkinter event loop
root.mainloop()
