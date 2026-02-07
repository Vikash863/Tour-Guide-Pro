const itinerary = [
  { day: 'Day 1', activity: 'Arrive in Jaipur', type: 'Travel' },
  { day: 'Day 2', activity: 'Visit City Palace & Jantar Mantar', type: 'Attraction' },
  { day: 'Day 3', activity: 'Hotel stay at Royal Heritage', type: 'Hotel' },
  { day: 'Day 4', activity: 'Cab to Pushkar', type: 'Cab' },
  { day: 'Day 5', activity: 'Explore Pushkar Lake & Market', type: 'Attraction' }
];

const timeline = document.getElementById('timeline');
itinerary.forEach(item => {
  const card = document.createElement('div');
  card.className = 'card';
  card.innerHTML = `
    <h3>${item.day}</h3>
    <p><strong>Activity:</strong> ${item.activity}</p>
    <p><strong>Type:</strong> ${item.type}</p>
  `;
  timeline.appendChild(card);
});

// Export button (simulated)
document.getElementById('exportBtn').addEventListener('click', () => {
  alert('Your itinerary PDF is being prepared...');
});
