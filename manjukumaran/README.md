## 🧪 Web Route Handler – Unit Testing Example

This project demonstrates a **simple, single-file Python script** that simulates web route handling logic and tests it using Python’s built-in `unittest` framework — all **without any external web framework** like Flask or Django.

---

### 📁 Project Structure

```
web_test.py       # Main Python file with logic and unit tests
README.md         # Project documentation
```

---

### 📜 Description

* A basic function `handle_request(route)` simulates handling of URL-like paths (`/`, `/about`, `/contact`).
* The `unittest` module is used to validate the function's behavior with different route inputs.

---

### 🚀 How to Run

1. Make sure Python is installed (`python3 --version`).
2. Save the following code in a file named `web_test.py`.
3. Run the test with:

```bash
python web_test.py
```

---

### 🧩 Example Code

```python
import unittest

# --- Simulated web-like function ---
def handle_request(route):
    if route == "/":
        return "Welcome to the homepage!"
    elif route == "/about":
        return "This is the about page."
    elif route == "/contact":
        return "Contact us at example@example.com."
    else:
        return "404 Not Found"

# --- Unit Tests ---
class TestWebHandler(unittest.TestCase):

    def test_home(self):
        self.assertEqual(handle_request("/"), "Welcome to the homepage!")

    def test_about(self):
        self.assertEqual(handle_request("/about"), "This is the about page.")

    def test_contact(self):
        self.assertEqual(handle_request("/contact"), "Contact us at example@example.com.")

    def test_not_found(self):
        self.assertEqual(handle_request("/invalid"), "404 Not Found")

# --- Run tests ---
if __name__ == "__main__":
    unittest.main()
```

---

### ✅ Output Example

If all tests pass, the output will be:

```
....
----------------------------------------------------------------------
Ran 4 tests in 0.001s

OK
```

---

### 📚 Concepts Used

* Basic function simulation of a web route.
* `unittest.TestCase` for testing different input cases.
* Command-line execution of test scripts.

---

### 🛠️ Requirements

* Python 3.x (no external packages required)

---

### 🧑‍💻 Author

*Your Name Here*
Feel free to contribute or modify this script for learning or extension purposes.

---
