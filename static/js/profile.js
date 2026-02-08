// Profile Page JavaScript

// Global variables
let currentUser = null;
let userBookings = [];

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
  checkAuth();
  setupTabNavigation();
  loadUserProfile();
  loadBookings();
  loadTravelHistory();
});

// Check authentication status
function checkAuth() {
  const userData = localStorage.getItem('user');
  const token = localStorage.getItem('authToken');
  
  if (!userData || !token) {
    // Not logged in, redirect to login
    return;
  }
  
  try {
    currentUser = JSON.parse(userData);
    updateProfileDisplay();
  } catch (e) {
    console.error('Error parsing user data:', e);
  }
}

// Update profile display
function updateProfileDisplay() {
  if (!currentUser) return;
  
  const userName = document.getElementById('userName');
  const userEmail = document.getElementById('userEmail');
  
  if (userName) {
    userName.textContent = `${currentUser.first_name || ''} ${currentUser.last_name || ''}`.trim() || currentUser.username || 'User';
  }
  if (userEmail) {
    userEmail.textContent = currentUser.email || 'user@example.com';
  }
  
  // Populate form fields
  const firstNameInput = document.getElementById('firstName');
  const lastNameInput = document.getElementById('lastName');
  const emailInput = document.getElementById('profileEmail');
  const phoneInput = document.getElementById('phone');
  
  if (firstNameInput) firstNameInput.value = currentUser.first_name || '';
  if (lastNameInput) lastNameInput.value = currentUser.last_name || '';
  if (emailInput) emailInput.value = currentUser.email || '';
  if (phoneInput) phoneInput.value = currentUser.phone || '';
}

// Setup tab navigation
function setupTabNavigation() {
  const tabLinks = document.querySelectorAll('.profile-nav a[data-tab]');
  
  tabLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      const tabName = this.getAttribute('data-tab');
      switchTab(tabName);
    });
  });
}

// Switch between tabs
function switchTab(tabName) {
  // Update nav active state
  document.querySelectorAll('.profile-nav a[data-tab]').forEach(link => {
    link.classList.remove('active');
  });
  document.querySelectorAll('.profile-nav a').forEach(link => {
    if (link.getAttribute('data-tab') === tabName) {
      link.classList.add('active');
    }
  });
  
  // Update content active state
  document.querySelectorAll('.tab-content').forEach(content => {
    content.classList.remove('active');
  });
  const targetTab = document.getElementById(tabName + '-tab');
  if (targetTab) {
    targetTab.classList.add('active');
  }
}

// Load user profile from API
async function loadUserProfile() {
  const token = localStorage.getItem('authToken');
  if (!token) return;
  
  try {
    const response = await fetch('/api/users/me/', {
      headers: {
        'Authorization': `Token ${token}`
      }
    });
    
    if (response.ok) {
      currentUser = await response.json();
      localStorage.setItem('user', JSON.stringify(currentUser));
      updateProfileDisplay();
    }
  } catch (error) {
    console.error('Error loading profile:', error);
  }
}

// Load user bookings
async function loadBookings() {
  const token = localStorage.getItem('authToken');
  if (!token) {
    showEmptyBookings();
    return;
  }
  
  try {
    const response = await fetch('/api/bookings/my_bookings/', {
      headers: {
        'Authorization': `Token ${token}`
      }
    });
    
    if (response.ok) {
      userBookings = await response.json();
      renderBookings(userBookings);
    } else {
      showEmptyBookings();
    }
  } catch (error) {
    console.error('Error loading bookings:', error);
    showEmptyBookings();
  }
}

// Render bookings list
function renderBookings(bookings) {
  const container = document.getElementById('bookingsList');
  if (!container) return;
  
  if (!bookings || bookings.length === 0) {
    container.innerHTML = `
      <div class="empty-state">
        <i class="fas fa-suitcase" style="font-size: 48px; color: #ddd;"></i>
        <h3>No Bookings Yet</h3>
        <p>Start exploring and book your first adventure!</p>
      </div>
    `;
    return;
  }
  
  container.innerHTML = bookings.map(booking => `
    <div class="booking-card ${booking.booking_status || 'upcoming'}">
      <div class="booking-header">
        <span class="booking-title">${booking.booking_type || 'Booking'} #${booking.id}</span>
        <span class="booking-status ${booking.booking_status || 'pending'}">${booking.booking_status || 'Pending'}</span>
      </div>
      <div class="booking-details">
        <div class="booking-detail">
          <i class="fas fa-calendar"></i>
          <span>${formatDate(booking.booking_date)}</span>
        </div>
        <div class="booking-detail">
          <i class="fas fa-users"></i>
          <span>${booking.number_of_guests || 1} Guest(s)</span>
        </div>
        <div class="booking-detail">
          <i class="fas fa-rupee-sign"></i>
          <span>₹${booking.total_price || 0}</span>
        </div>
      </div>
    </div>
  `).join('');
}

// Show empty bookings state
function showEmptyBookings() {
  const container = document.getElementById('bookingsList');
  if (container) {
    container.innerHTML = `
      <div class="empty-state">
        <i class="fas fa-suitcase" style="font-size: 48px; color: #ddd;"></i>
        <h3>No Bookings Yet</h3>
        <p>Start exploring and book your first adventure!</p>
      </div>
    `;
  }
}

// Filter bookings
function filterBookings() {
  const filter = document.getElementById('bookingFilter')?.value || 'all';
  
  if (filter === 'all') {
    renderBookings(userBookings);
  } else if (filter === 'upcoming') {
    const upcoming = userBookings.filter(b => b.booking_status === 'pending' || b.booking_status === 'confirmed');
    renderBookings(upcoming);
  } else if (filter === 'completed') {
    const completed = userBookings.filter(b => b.booking_status === 'completed');
    renderBookings(completed);
  } else if (filter === 'cancelled') {
    const cancelled = userBookings.filter(b => b.booking_status === 'cancelled');
    renderBookings(cancelled);
  }
}

// Load travel history
async function loadTravelHistory() {
  const token = localStorage.getItem('authToken');
  if (!token) {
    showEmptyHistory();
    return;
  }
  
  try {
    const response = await fetch('/api/bookings/my_bookings/', {
      headers: {
        'Authorization': `Token ${token}`
      }
    });
    
    if (response.ok) {
      const bookings = await response.json();
      const completed = bookings.filter(b => b.booking_status === 'completed');
      
      // Calculate stats
      const totalSpent = completed.reduce((sum, b) => sum + (parseFloat(b.total_price) || 0), 0);
      const hotels = completed.filter(b => b.booking_type === 'hotel').length;
      const cabs = completed.filter(b => b.booking_type === 'cab').length;
      
      const totalTripsEl = document.getElementById('totalTrips');
      const totalHotelsEl = document.getElementById('totalHotels');
      const totalCabsEl = document.getElementById('totalCabs');
      const totalSpentEl = document.getElementById('totalSpent');
      
      if (totalTripsEl) totalTripsEl.textContent = completed.length;
      if (totalHotelsEl) totalHotelsEl.textContent = hotels;
      if (totalCabsEl) totalCabsEl.textContent = cabs;
      if (totalSpentEl) totalSpentEl.textContent = '₹' + totalSpent.toLocaleString();
      
      // Render timeline
      renderTimeline(completed);
    } else {
      showEmptyHistory();
    }
  } catch (error) {
    console.error('Error loading history:', error);
    showEmptyHistory();
  }
}

// Render timeline
function renderTimeline(items) {
  const container = document.getElementById('historyTimeline');
  if (!container) return;
  
  if (!items || items.length === 0) {
    container.innerHTML = `
      <div class="empty-state">
        <i class="fas fa-history" style="font-size: 48px; color: #ddd;"></i>
        <h3>No Travel History</h3>
        <p>Your completed trips will appear here!</p>
      </div>
    `;
    return;
  }
  
  // Sort by date (newest first)
  items.sort((a, b) => new Date(b.booking_date) - new Date(a.booking_date));
  
  container.innerHTML = items.map(item => `
    <div class="timeline-item">
      <div class="timeline-date">${formatDate(item.booking_date)}</div>
      <div class="timeline-title">${item.booking_type || 'Trip'} - ${item.destination || 'Destination'}</div>
      <div class="timeline-desc">
        <i class="fas fa-rupee-sign"></i> ₹${item.total_price || 0}
      </div>
    </div>
  `).join('');
}

// Show empty history state
function showEmptyHistory() {
  const totalTripsEl = document.getElementById('totalTrips');
  const totalHotelsEl = document.getElementById('totalHotels');
  const totalCabsEl = document.getElementById('totalCabs');
  const totalSpentEl = document.getElementById('totalSpent');
  const container = document.getElementById('historyTimeline');
  
  if (totalTripsEl) totalTripsEl.textContent = '0';
  if (totalHotelsEl) totalHotelsEl.textContent = '0';
  if (totalCabsEl) totalCabsEl.textContent = '0';
  if (totalSpentEl) totalSpentEl.textContent = '₹0';
  
  if (container) {
    container.innerHTML = `
      <div class="empty-state">
        <i class="fas fa-history" style="font-size: 48px; color: #ddd;"></i>
        <h3>No Travel History</h3>
        <p>Your completed trips will appear here!</p>
      </div>
    `;
  }
}

// Format date helper
function formatDate(dateString) {
  if (!dateString) return 'N/A';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-IN', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  });
}

// Profile form submission
document.getElementById('profileForm')?.addEventListener('submit', async function(e) {
  e.preventDefault();
  
  const token = localStorage.getItem('authToken');
  if (!token) {
    alert('Please login to update your profile');
    return;
  }
  
  const data = {
    first_name: document.getElementById('firstName')?.value || '',
    last_name: document.getElementById('lastName')?.value || '',
    phone: document.getElementById('phone')?.value || ''
  };
  
  try {
    const response = await fetch(`/api/users/${currentUser?.id || 'me'}/update_profile/`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${token}`
      },
      body: JSON.stringify(data)
    });
    
    if (response.ok) {
      const updatedUser = await response.json();
      currentUser = { ...currentUser, ...updatedUser.user };
      localStorage.setItem('user', JSON.stringify(currentUser));
      alert('Profile updated successfully!');
      updateProfileDisplay();
    } else {
      alert('Failed to update profile');
    }
  } catch (error) {
    console.error('Error updating profile:', error);
    alert('Error updating profile');
  }
});

// Preferences form submission
document.getElementById('preferencesForm')?.addEventListener('submit', function(e) {
  e.preventDefault();
  const preferences = {
    wifi: document.getElementById('prefWifi')?.checked || false,
    breakfast: document.getElementById('prefBreakfast')?.checked || false,
    pool: document.getElementById('prefPool')?.checked || false
  };
  localStorage.setItem('userPreferences', JSON.stringify(preferences));
  alert('Preferences saved!');
});

// Logout function
function logout() {
  const token = localStorage.getItem('authToken');
  
  if (token) {
    fetch('/api/users/logout/', {
      method: 'POST',
      headers: {
        'Authorization': `Token ${token}`
      }
    }).finally(() => {
      localStorage.removeItem('authToken');
      localStorage.removeItem('user');
      localStorage.removeItem('userPreferences');
      window.location.href = '/';
    });
  } else {
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
    localStorage.removeItem('userPreferences');
    window.location.href = '/';
  }
}

// Delete account
function deleteAccount() {
  if (confirm('Are you sure you want to delete your account? This cannot be undone.')) {
    if (confirm('This will permanently delete all your data. Continue?')) {
      localStorage.removeItem('authToken');
      localStorage.removeItem('user');
      localStorage.removeItem('userPreferences');
      alert('Account deleted');
      window.location.href = '/';
    }
  }
}
