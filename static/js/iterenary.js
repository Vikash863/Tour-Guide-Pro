// ============================================
// TOUR GUIDE PRO - ITINERARY PAGE
// Ultra-Modern Timeline Experience
// ============================================

// Mock Data - This would come from backend in production
const mockItinerary = [
  {
    day: 1,
    date: 'February 15, 2026',
    activities: [
      {
        id: 1,
        type: 'hotel',
        title: 'Taj Hotel Mumbai',
        time: '2:00 PM - Check-in',
        details: {
          location: 'Colaba, Mumbai',
          duration: '3 nights',
          rooms: '1 Deluxe Room',
          guests: '2 Adults'
        },
        price: '₹15,000'
      },
      {
        id: 2,
        type: 'cab',
        title: 'Airport to Hotel',
        time: '11:00 AM',
        details: {
          pickup: 'Mumbai Airport',
          drop: 'Taj Hotel, Colaba',
          duration: '45 mins',
          passengers: '2'
        },
        price: '₹800'
      }
    ]
  },
  {
    day: 2,
    date: 'February 16, 2026',
    activities: [
      {
        id: 3,
        type: 'destination',
        title: 'Gateway of India',
        time: '10:00 AM',
        details: {
          location: 'Colaba, Mumbai',
          duration: '2 hours',
          type: 'Historical Site',
          tickets: '₹50 per person'
        },
        price: '₹100'
      },
      {
        id: 4,
        type: 'cab',
        title: 'City Tour - Hourly',
        time: '9:00 AM - 6:00 PM',
        details: {
          pickup: 'Taj Hotel',
          drop: 'Taj Hotel',
          duration: '9 hours',
          passengers: '2'
        },
        price: '₹1,350'
      },
      {
        id: 5,
        type: 'destination',
        title: 'Marine Drive Sunset',
        time: '5:30 PM',
        details: {
          location: 'Marine Drive, Mumbai',
          duration: '1.5 hours',
          type: 'Scenic Location',
          tickets: 'Free'
        },
        price: '₹0'
      }
    ]
  },
  {
    day: 3,
    date: 'February 17, 2026',
    activities: [
      {
        id: 6,
        type: 'destination',
        title: 'Elephanta Caves',
        time: '8:00 AM',
        details: {
          location: 'Elephanta Island',
          duration: '4 hours',
          type: 'UNESCO Site',
          tickets: '₹40 per person'
        },
        price: '₹80'
      }
    ]
  },
  {
    day: 4,
    date: 'February 18, 2026',
    activities: [
      {
        id: 7,
        type: 'hotel',
        title: 'Taj Hotel - Check-out',
        time: '11:00 AM',
        details: {
          location: 'Colaba, Mumbai',
          duration: '3 nights completed',
          rooms: '1 Deluxe Room',
          guests: '2 Adults'
        },
        price: '₹0'
      },
      {
        id: 8,
        type: 'cab',
        title: 'Hotel to Airport',
        time: '12:00 PM',
        details: {
          pickup: 'Taj Hotel, Colaba',
          drop: 'Mumbai Airport',
          duration: '45 mins',
          passengers: '2'
        },
        price: '₹800'
      }
    ]
  }
];

// State
let currentFilter = 'all';

// DOM Elements
const elements = {
  timelineContainer: document.getElementById('timelineContainer'),
  filterTabs: document.querySelectorAll('.filter-tab'),
  totalBookings: document.getElementById('totalBookings'),
  totalDays: document.getElementById('totalDays'),
  totalCost: document.getElementById('totalCost'),
  navbar: document.getElementById('navbar')
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  initializeFilters();
  renderItinerary();
  updateSummary();
  initializeScrollEffects();
});

// Initialize Filter Tabs
function initializeFilters() {
  elements.filterTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      // Remove active class from all tabs
      elements.filterTabs.forEach(t => t.classList.remove('active'));
      
      // Add active class to clicked tab
      tab.classList.add('active');
      
      // Update filter
      currentFilter = tab.dataset.filter;
      
      // Re-render timeline
      renderItinerary();
    });
  });
}

// Render Itinerary
function renderItinerary() {
  const filteredData = filterItinerary(mockItinerary, currentFilter);
  
  if (filteredData.length === 0 || filteredData.every(day => day.activities.length === 0)) {
    renderEmptyState();
    return;
  }
  
  let html = '';
  
  filteredData.forEach(day => {
    if (day.activities.length === 0) return; // Skip days with no activities
    
    html += `
      <div class="day-section">
        <div class="day-header">
          <div class="day-marker">
            <span>Day ${day.day}</span>
          </div>
          <div class="day-info">
            <h3>Day ${day.day}</h3>
            <p class="day-date">${day.date}</p>
          </div>
        </div>
        
        <div class="timeline">
          ${day.activities.map(activity => renderActivityCard(activity)).join('')}
        </div>
      </div>
    `;
  });
  
  elements.timelineContainer.innerHTML = html;
}

// Filter Itinerary
function filterItinerary(data, filter) {
  if (filter === 'all') return data;
  
  return data.map(day => ({
    ...day,
    activities: day.activities.filter(activity => activity.type === filter)
  }));
}

// Render Activity Card
function renderActivityCard(activity) {
  const iconMap = {
    hotel: 'ti-bed',
    cab: 'ti-car',
    destination: 'ti-map-pin'
  };
  
  const detailsHtml = Object.entries(activity.details).map(([key, value]) => {
    const iconMapping = {
      location: 'ti-map-pin',
      pickup: 'ti-map-pin',
      drop: 'ti-location-pin',
      duration: 'ti-clock',
      rooms: 'ti-bed',
      guests: 'ti-user',
      passengers: 'ti-user',
      type: 'ti-category',
      tickets: 'ti-ticket'
    };
    
    const icon = iconMapping[key] || 'ti-info-circle';
    const label = key.charAt(0).toUpperCase() + key.slice(1);
    
    return `
      <div class="detail-item">
        <i class="ti ${icon}"></i>
        <div class="detail-content">
          <div class="detail-label">${label}</div>
          <div class="detail-value">${value}</div>
        </div>
      </div>
    `;
  }).join('');
  
  return `
    <div class="timeline-item">
      <div class="timeline-dot"></div>
      <div class="activity-card ${activity.type}">
        <div class="activity-price">${activity.price}</div>
        
        <div class="activity-header">
          <div class="activity-icon">
            <i class="ti ${iconMap[activity.type]}"></i>
          </div>
          <div class="activity-info">
            <div class="activity-type">${activity.type}</div>
            <h4 class="activity-title">${activity.title}</h4>
            <div class="activity-time">
              <i class="ti ti-clock"></i>
              ${activity.time}
            </div>
          </div>
        </div>
        
        <div class="activity-details">
          ${detailsHtml}
        </div>
      </div>
    </div>
  `;
}

// Render Empty State
function renderEmptyState() {
  elements.timelineContainer.innerHTML = `
    <div class="empty-state">
      <div class="empty-icon">
        <i class="ti ti-calendar-event"></i>
      </div>
      <h2 class="empty-title">No Bookings Yet</h2>
      <p class="empty-message">Start planning your perfect trip by adding hotels, cabs, or destinations to your itinerary.</p>
      <div class="empty-actions">
        <a href="/hotel/" class="empty-btn">
          <i class="ti ti-bed"></i>
          Book a Hotel
        </a>
        <a href="/cab/" class="empty-btn">
          <i class="ti ti-car"></i>
          Book a Cab
        </a>
        <a href="/destination/" class="empty-btn">
          <i class="ti ti-map-pin"></i>
          Explore Destinations
        </a>
      </div>
    </div>
  `;
}

// Update Summary
function updateSummary() {
  // Calculate totals
  let totalBookings = 0;
  let totalCost = 0;
  
  mockItinerary.forEach(day => {
    totalBookings += day.activities.length;
    day.activities.forEach(activity => {
      const price = parseInt(activity.price.replace(/[₹,]/g, '')) || 0;
      totalCost += price;
    });
  });
  
  // Update DOM
  elements.totalBookings.textContent = totalBookings;
  elements.totalDays.textContent = mockItinerary.length;
  elements.totalCost.textContent = `₹${totalCost.toLocaleString('en-IN')}`;
}

// Share Itinerary
function shareItinerary() {
  if (navigator.share) {
    navigator.share({
      title: 'My Travel Itinerary - TourGuidePro',
      text: 'Check out my travel itinerary!',
      url: window.location.href
    }).catch(err => console.log('Error sharing:', err));
  } else {
    // Fallback: Copy to clipboard
    navigator.clipboard.writeText(window.location.href)
      .then(() => alert('Itinerary link copied to clipboard!'))
      .catch(err => console.error('Failed to copy:', err));
  }
}

// Export Itinerary
function exportItinerary() {
  alert('Export feature coming soon! Your itinerary will be downloaded as PDF.');
  // In production, this would generate a PDF or send to backend
}

// Scroll Effects
function initializeScrollEffects() {
  window.addEventListener('scroll', () => {
    const scrolled = window.scrollY > 50;
    elements.navbar.classList.toggle('scrolled', scrolled);
  });
}
