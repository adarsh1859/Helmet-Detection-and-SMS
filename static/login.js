document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('loginForm').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent form submission
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        // Predefined username and password
        const predefinedUsername = '123';
        const predefinedPassword = '123';

        // Check if username and password match
        if (username === predefinedUsername && password === predefinedPassword) {
            // Redirect to index.html
            window.location.href = '/dashboard';
        } else {
            alert('Invalid username or password. Please try again.');
        }
    });
});
