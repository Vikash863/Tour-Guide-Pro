document.getElementById("signupForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const name = document.getElementById("name").value.trim();
  const email = document.getElementById("email").value.trim();
  const phone = document.getElementById("phone").value.trim();
  const password = document.getElementById("password").value;
  const confirmPassword = document.getElementById("confirmPassword").value;
  const errorDiv = document.getElementById("errorMessage");

  // Validation
  if (!name || !email || !password) {
    errorDiv.textContent = "Please fill in all required fields";
    errorDiv.style.display = "block";
    return;
  }

  if (password !== confirmPassword) {
    errorDiv.textContent = "Passwords do not match";
    errorDiv.style.display = "block";
    return;
  }

  if (password.length < 6) {
    errorDiv.textContent = "Password must be at least 6 characters";
    errorDiv.style.display = "block";
    return;
  }

  try {
    const result = await api.register(name, email, password, phone);
    
    if (result.message && !result.username && !result.email && !result.password) {
      // Success response
      if (result.user) {
        localStorage.setItem('user', JSON.stringify(result.user));
        errorDiv.style.display = "none";
        alert(`Welcome, ${name}! Your account has been created.`);
        window.location.href = "/";
      }
    } else {
      // Error response - show all errors
      const errors = [];
      if (result.username) errors.push(`Username: ${result.username}`);
      if (result.email) errors.push(`Email: ${result.email}`);
      if (result.password) errors.push(`Password: ${result.password}`);
      if (result.password_confirm) errors.push(`Password Confirm: ${result.password_confirm}`);
      if (result.first_name) errors.push(`First Name: ${result.first_name}`);
      if (result.last_name) errors.push(`Last Name: ${result.last_name}`);
      
      const errorMessage = errors.length > 0 ? errors.join('; ') : (result.message || "Signup failed");
      errorDiv.textContent = errorMessage;
      errorDiv.style.display = "block";
    }
  } catch (error) {
    errorDiv.textContent = "Network error: " + error.message;
    errorDiv.style.display = "block";
  }
});