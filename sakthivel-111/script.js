const board = document.querySelectorAll('.cell');
const message = document.getElementById('message');
const restartBtn = document.getElementById('restart-btn');
let currentPlayer = 'X';
let gameState = ['', '', '', '', '', '', '', '', '']; // Empty board
let gameActive = true;

// Win conditions
const winConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
];

// Handle cell click
function handleCellClick(index) {
    if (gameState[index] !== '' || !gameActive) return; // Ignore if cell is already filled or game is over
    gameState[index] = currentPlayer;
    board[index].textContent = currentPlayer;

    // Check for win
    if (checkWinner()) {
        message.textContent = `${currentPlayer} wins!`;
        gameActive = false;
        return;
    }

    // Check for draw
    if (gameState.every(cell => cell !== '')) {
        message.textContent = "It's a draw!";
        gameActive = false;
        return;
    }

    // Switch player
    currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
    message.textContent = `Player ${currentPlayer}'s turn`;
}

// Check for a winner
function checkWinner() {
    return winConditions.some(condition => {
        const [a, b, c] = condition;
        return gameState[a] && gameState[a] === gameState[b] && gameState[a] === gameState[c];
    });
}

// Restart the game
function restartGame() {
    gameState = ['', '', '', '', '', '', '', '', ''];
    gameActive = true;
    currentPlayer = 'X';
    message.textContent = "Player X's turn";

    board.forEach(cell => {
        cell.textContent = '';
    });
}

// Add event listeners to each cell
board.forEach(cell => {
    cell.addEventListener('click', () => {
        handleCellClick(cell.dataset.index);
    });
});

// Restart button event listener
restartBtn.addEventListener('click', restartGame);

// Initial message
message.textContent = "Player X's turn";
