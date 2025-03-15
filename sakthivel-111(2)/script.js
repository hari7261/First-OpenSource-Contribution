const words = ["JAVASCRIPT", "HANGMAN", "COMPUTER", "DEVELOPER", "PROGRAMMING"];
let chosenWord = "";
let guessedLetters = [];
let wrongLetters = [];
let remainingAttempts = 6;

const wordDisplay = document.getElementById("word-display");
const wrongGuesses = document.getElementById("wrong-guesses");
const letterInput = document.getElementById("letter-input");
const guessButton = document.getElementById("guess-btn");
const message = document.getElementById("message");
const restartButton = document.getElementById("restart-btn");

function startNewGame() {
    // Reset all game variables
    chosenWord = words[Math.floor(Math.random() * words.length)];
    guessedLetters = [];
    wrongLetters = [];
    remainingAttempts = 6;

    // Update UI
    wordDisplay.textContent = "_ ".repeat(chosenWord.length);
    wrongGuesses.textContent = "Wrong guesses: ";
    letterInput.value = "";
    letterInput.disabled = false;
    guessButton.disabled = false;
    restartButton.classList.add("hidden");
    message.textContent = "Good luck!";
}

function updateWordDisplay() {
    wordDisplay.textContent = chosenWord
        .split("")
        .map(letter => (guessedLetters.includes(letter) ? letter : "_"))
        .join(" ");
}

function handleGuess() {
    const letter = letterInput.value.toUpperCase();
    if (letter && !guessedLetters.includes(letter) && !wrongLetters.includes(letter)) {
        if (chosenWord.includes(letter)) {
            guessedLetters.push(letter);
        } else {
            wrongLetters.push(letter);
            remainingAttempts--;
        }
    }
    letterInput.value = "";
    letterInput.focus();
    updateGame();
}

function updateGame() {
    updateWordDisplay();
    wrongGuesses.textContent = `Wrong guesses: ${wrongLetters.join(", ")}`;

    if (remainingAttempts === 0) {
        message.textContent = `Game over! The word was: ${chosenWord}.`;
        letterInput.disabled = true;
        guessButton.disabled = true;
        restartButton.classList.remove("hidden");
    } else if (!wordDisplay.textContent.includes("_")) {
        message.textContent = "Congratulations! You've guessed the word!";
        letterInput.disabled = true;
        guessButton.disabled = true;
        restartButton.classList.remove("hidden");
    } else {
        message.textContent = `Attempts remaining: ${remainingAttempts}`;
    }
}

guessButton.addEventListener("click", handleGuess);
restartButton.addEventListener("click", startNewGame);

// Start the game on page load
startNewGame();
