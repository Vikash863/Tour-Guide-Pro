document.getElementById('cabForm').addEventListener('submit', function(e) {
  e.preventDefault();

  // Simulate booking confirmation
  document.getElementById('cabForm').classList.add('hidden');
  document.getElementById('confirmation').classList.remove('hidden');
});
