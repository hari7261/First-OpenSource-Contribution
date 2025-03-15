import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Create tables
cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    author TEXT,
                    year INTEGER,
                    available INTEGER)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS borrowed (
                    user_id INTEGER,
                    book_id INTEGER,
                    FOREIGN KEY(user_id) REFERENCES users(id),
                    FOREIGN KEY(book_id) REFERENCES books(id))''')

conn.commit()

# Function to add a book
def add_book():
    title = input("Enter book title: ")
    author = input("Enter author name: ")
    year = input("Enter publication year: ")

    cursor.execute("INSERT INTO books (title, author, year, available) VALUES (?, ?, ?, 1)", (title, author, year))
    conn.commit()
    print("Book added successfully!")

# Function to view all books
def view_books():
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    print("\n📚 Library Books 📚")
    for book in books:
        status = "Available" if book[4] else "Issued"
        print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Year: {book[3]}, Status: {status}")

# Function to issue a book
def issue_book():
    user_name = input("Enter user name: ")
    book_id = input("Enter book ID to issue: ")

    cursor.execute("SELECT available FROM books WHERE id=?", (book_id,))
    book = cursor.fetchone()

    if book and book[0] == 1:
        cursor.execute("INSERT INTO users (name) VALUES (?)", (user_name,))
        user_id = cursor.lastrowid

        cursor.execute("INSERT INTO borrowed (user_id, book_id) VALUES (?, ?)", (user_id, book_id))
        cursor.execute("UPDATE books SET available=0 WHERE id=?", (book_id,))
        conn.commit()
        print("Book issued successfully!")
    else:
        print("Book is not available!")

# Function to return a book
def return_book():
    book_id = input("Enter book ID to return: ")

    cursor.execute("DELETE FROM borrowed WHERE book_id=?", (book_id,))
    cursor.execute("UPDATE books SET available=1 WHERE id=?", (book_id,))
    conn.commit()
    print("Book returned successfully!")

# Function to search for a book
def search_book():
    search = input("Enter book title or author to search: ")
    cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", ('%' + search + '%', '%' + search + '%'))
    books = cursor.fetchall()

    print("\n🔎 Search Results 🔎")
    for book in books:
        print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Year: {book[3]}")

# Main menu
while True:
    print("\n📚 Library Management System 📚")
    print("1. Add Book")
    print("2. View Books")
    print("3. Issue Book")
    print("4. Return Book")
    print("5. Search Book")
    print("6. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        add_book()
    elif choice == "2":
        view_books()
    elif choice == "3":
        issue_book()
    elif choice == "4":
        return_book()
    elif choice == "5":
        search_book()
    elif choice == "6":
        print("Exiting Library Management System. Goodbye! 👋")
        break
    else:
        print("Invalid choice! Please try again.")
