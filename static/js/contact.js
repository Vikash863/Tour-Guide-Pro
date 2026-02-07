document.getElementById('contactForm').addEventListener('submit', async function(e) {
  e.preventDefault();
  
  const name = document.getElementById('name').value.trim();
  const email = document.getElementById('email').value.trim();
  const phone = document.getElementById('phone').value.trim();
  const subject = document.getElementById('subject').value.trim();
  const message = document.getElementById('message').value.trim();
  const responseDiv = document.getElementById('responseMessage');
  const errorDiv = document.getElementById('errorMessage');

  if (!name || !email || !subject || !message) {
    errorDiv.textContent = 'Please fill in all required fields';
    errorDiv.style.display = 'block';
    return;
  }

  try {
    const result = await api.submitContact(name, email, phone, subject, message);
    
    if (result.contact) {
      responseDiv.textContent = 'Thanks for reaching out! We\'ll get back to you soon.';
      responseDiv.style.display = 'block';
      errorDiv.style.display = 'none';
      document.getElementById('contactForm').reset();
      
      // Hide message after 3 seconds
      setTimeout(() => {
        responseDiv.style.display = 'none';
      }, 3000);
    } else {
      errorDiv.textContent = result.message || 'Failed to send message';
      errorDiv.style.display = 'block';
      responseDiv.style.display = 'none';
    }
  } catch (error) {
    errorDiv.textContent = 'Network error: ' + error.message;
    errorDiv.style.display = 'block';
    responseDiv.style.display = 'none';
  }
});
