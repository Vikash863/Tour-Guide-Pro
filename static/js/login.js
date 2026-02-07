document.getElementById("loginForm").addEventListener("submit", async function (e) {
  e.preventDefault();
  
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;
  const errorDiv = document.getElementById("errorMessage");

  if (!email || !password) {
    errorDiv.textContent = "Please fill in all fields";
    errorDiv.style.display = "block";
    return;
  }

  try {
    const result = await api.login(email, password);
    
    if (result.token) {
      // Store token and user info
      localStorage.setItem('token', result.token);
      localStorage.setItem('user', JSON.stringify(result.user));
      errorDiv.style.display = "none";
      alert("Login successful!");
      window.location.href = "/";
    } else if (result.message) {
      // Login failed with error message
      errorDiv.textContent = result.message;
      errorDiv.style.display = "block";
    } else {
      errorDiv.textContent = "Login failed";
      errorDiv.style.display = "block";
    }
  } catch (error) {
    errorDiv.textContent = "Network error: " + error.message;
    errorDiv.style.display = "block";
  }
});