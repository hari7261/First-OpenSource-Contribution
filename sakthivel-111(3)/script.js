function validateForm() {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    var errorMessage = document.getElementById("error-message");

    // Clear any previous error messages
    errorMessage.textContent = '';

    // Validate the form
    if (username === "" || password === "") {
        errorMessage.textContent = "Please fill in both fields.";
        return false;  // Prevent form submission
    }

    // Simulate successful login (replace with real validation logic)
    if (username === "admin" && password === "password123") {
        alert("Login successful!");
        return true;  // Form is submitted
    } else {
        errorMessage.textContent = "Invalid username or password.";
        return false;  // Prevent form submission
    }
}
