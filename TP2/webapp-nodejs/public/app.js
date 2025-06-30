const form = document.getElementById("loginForm");
const username = document.getElementById("username");
const password = document.getElementById("password");

// Listen for form submission
form.addEventListener("submit", async (event) => {
  event.preventDefault(); // Prevent the default form submission

  const userInput = {
    username: username.value,
    password: password.value,
  };

  try {
    // Send a POST request to the login endpoint
    const response = await fetch("/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(userInput),
    });

    const data = await response.json();

    if (response.ok) {
      // Successful login
      alert(`Welcome ${data.user}! Role: ${data.role}`);
    } else {
      // Login failed
      alert(data.message);
    }
  } catch (error) {
    console.error("Error during login:", error);
    alert("An error occurred while trying to log in.");
  }
});
