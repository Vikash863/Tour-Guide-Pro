document.getElementById("signupForm").addEventListener("submit", function (e) {
  e.preventDefault();

  const name = document.getElementById("name").value.trim();
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;
  const confirmPassword = document.getElementById("confirmPassword").value;

  if (password !== confirmPassword) {
    alert("Passwords do not match. Please re-enter.");
    return;
  }

  // Simulate signup success
  alert(`Welcome, ${name}! Your account has been created.`);
  window.location.href = "login.html";
});