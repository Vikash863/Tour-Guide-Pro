document.getElementById("loginForm").addEventListener("submit", function (e) {
  e.preventDefault();
  alert("Login successful! Redirecting to dashboard...");
  window.location.href = "Home.html";
});