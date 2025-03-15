let books = [];
const bookListContainer = document.getElementById("bookList");

function renderBooks() {
  // Clear current list
  bookListContainer.innerHTML = "";

  // Render updated list
  books.forEach((book, index) => {
    const bookDiv = document.createElement("div");
    bookDiv.classList.add("book-item");

    // Book Name
    const bookName = document.createElement("span");
    bookName.textContent = book;
    bookDiv.appendChild(bookName);

    // Update button
    const updateButton = document.createElement("button");
    updateButton.textContent = "Update";
    updateButton.onclick = () => updateBook(index);
    bookDiv.appendChild(updateButton);

    // Delete button
    const deleteButton = document.createElement("button");
    deleteButton.textContent = "Delete";
    deleteButton.classList.add("delete");
    deleteButton.onclick = () => confirmDeleteBook(index);
    bookDiv.appendChild(deleteButton);

    // Append book to list
    bookListContainer.appendChild(bookDiv);
  });
}

function saveBook() {
  const bookNameInput = document.getElementById("bookName");
  const bookName = bookNameInput.value.trim();
  
  if (bookName) {
    books.push(bookName); // Save book name
    bookNameInput.value = ""; // Clear input field
    renderBooks(); // Re-render book list
  } else {
    alert("Please enter a valid book name.");
  }
}

function updateBook(index) {
  // Show pop-up message
  alert("It may take a few seconds to update.");

  const newBookName = prompt("Enter the new book name:", books[index]);
  if (newBookName !== null && newBookName.trim() !== "") {
    books[index] = newBookName.trim(); // Update book name

    // Simulate a delay before rendering the updated list (you can adjust this)
    setTimeout(() => {
      renderBooks(); // Re-render book list after "update"
      alert("Book updated successfully!");
    }, 2000); // 2-second delay for demonstration
  }
}

function confirmDeleteBook(index) {
  const isConfirmed = confirm("Are you sure you want to delete this book?");
  if (isConfirmed) {
    deleteBook(index);
  }
}

function deleteBook(index) {
  books.splice(index, 1); // Remove book from the array
  renderBooks(); // Re-render book list
}

// Initial render
renderBooks();
