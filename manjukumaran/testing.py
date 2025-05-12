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
