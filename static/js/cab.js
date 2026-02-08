// ============================================
// TOUR GUIDE PRO - CAB BOOKING PAGE
// Ultra-Modern Interactive Experience
// ============================================

// State
let selectedCabType = null;
let selectedRate = 0;

// DOM Elements
const elements = {
  cabCards: document.querySelectorAll('.cab-type-card'),
  form: document.getElementById('cabForm'),
  durationInput: document.getElementById('duration'),
  durationLabel: document.getElementById('durationLabel'),
  durationGroup: document.getElementById('durationGroup'),
  submitBtn: document.getElementById('submitBtn'),
  modal: document.getElementById('successModal'),
  bookingDetails: document.getElementById('bookingDetails'),
  navbar: document.getElementById('navbar'),
  // Pricing display elements
  selectedTypeDisplay: document.getElementById('selectedTypeDisplay'),
  baseFareDisplay: document.getElementById('baseFareDisplay'),
  chargeLabel: document.getElementById('chargeLabel'),
  chargeValueDisplay: document.getElementById('chargeValueDisplay'),
  totalFareDisplay: document.getElementById('totalFareDisplay')
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
  initializeCabSelection();
  initializeForm();
  initializeScrollEffects();
  setMinDate();
});

// Cab Type Selection
function initializeCabSelection() {
  elements.cabCards.forEach(card => {
    card.addEventListener('click', () => {
      // Remove selected class from all cards
      elements.cabCards.forEach(c => c.classList.remove('selected'));
      
      // Add selected class to clicked card
      card.classList.add('selected');
      
      // Store selected cab type and rate
      selectedCabType = card.dataset.type;
      selectedRate = parseFloat(card.dataset.rate);
      
      // Update duration label based on cab type
      updateDurationLabel();
      
      // Update pricing display
      updatePricingDisplay();
      
      // Enable duration input
      elements.durationInput.disabled = false;
    });
  });
}

// Update Duration Label
function updateDurationLabel() {
  const labels = {
    hourly: 'Duration (Hours)',
    daily: 'Duration (Days)',
    km: 'Distance (Kilometers)'
  };
  
  elements.durationLabel.textContent = labels[selectedCabType] || 'Duration/Distance';
  elements.durationInput.placeholder = selectedCabType === 'km' ? 'Enter kilometers' : 
    selectedCabType === 'hourly' ? 'Enter hours' : 'Enter days';
}

// Update Pricing Display
function updatePricingDisplay() {
  const typeNames = {
    hourly: 'Hourly',
    daily: 'Daily',
    km: 'Per Kilometer'
  };
  
  elements.selectedTypeDisplay.textContent = typeNames[selectedCabType] || 'Not selected';
  elements.baseFareDisplay.textContent = selectedCabType ? `₹${selectedRate}` : '₹0';
  
  // Update charge label
  const chargeLabels = {
    hourly: 'Hours',
    daily: 'Days',
    km: 'Distance'
  };
  elements.chargeLabel.textContent = chargeLabels[selectedCabType] || 'Duration/Distance';
  
  // Calculate total if duration is entered
  calculateFare();
}

// Calculate Fare
function calculateFare() {
  const duration = parseFloat(elements.durationInput.value) || 0;
  
  if (selectedCabType && duration > 0) {
    const total = selectedRate * duration;
    elements.chargeValueDisplay.textContent = `${duration} × ₹${selectedRate}`;
    elements.totalFareDisplay.textContent = `₹${total.toFixed(0)}`;
  } else {
    elements.chargeValueDisplay.textContent = '-';
    elements.totalFareDisplay.textContent = '₹0';
  }
}

// Form Initialization
function initializeForm() {
  // Add input listener for duration
  elements.durationInput.addEventListener('input', calculateFare);
  
  // Form submission
  elements.form.addEventListener('submit', handleFormSubmit);
}

// Handle Form Submit
function handleFormSubmit(e) {
  e.preventDefault();
  
  // Validate cab type selection
  if (!selectedCabType) {
    alert('Please select a cab type');
    return;
  }
  
  // Get form values
  const formData = {
    cabType: selectedCabType,
    pickup: document.getElementById('pickup').value,
    drop: document.getElementById('drop').value,
    date: document.getElementById('date').value,
    time: document.getElementById('time').value,
    passengers: document.getElementById('passengers').value,
    duration: elements.durationInput.value,
    rate: selectedRate,
    total: (selectedRate * parseFloat(elements.durationInput.value)).toFixed(0)
  };
  
  // Show loading state
  elements.submitBtn.innerHTML = '<i class="ti ti-loader"></i> Processing...';
  elements.submitBtn.disabled = true;
  
  // Simulate API call
  setTimeout(() => {
    showSuccessModal(formData);
    elements.submitBtn.innerHTML = '<i class="ti ti-circle-check-filled"></i> Book Now';
    elements.submitBtn.disabled = false;
  }, 1500);
}

// Show Success Modal
function showSuccessModal(data) {
  const typeNames = {
    hourly: 'Hourly',
    daily: 'Daily',
    km: 'Per Kilometer'
  };
  
  const unitLabels = {
    hourly: 'hours',
    daily: 'days',
    km: 'km'
  };
  
  // Format date for display
  const dateObj = new Date(data.date);
  const formattedDate = dateObj.toLocaleDateString('en-IN', { 
    day: 'numeric', 
    month: 'long', 
    year: 'numeric' 
  });
  
  // Populate booking details
  elements.bookingDetails.innerHTML = `
    <div class="detail-row">
      <span class="detail-label">Cab Type</span>
      <span class="detail-value">${typeNames[data.cabType]}</span>
    </div>
    <div class="detail-row">
      <span class="detail-label">From</span>
      <span class="detail-value">${data.pickup}</span>
    </div>
    <div class="detail-row">
      <span class="detail-label">To</span>
      <span class="detail-value">${data.drop}</span>
    </div>
    <div class="detail-row">
      <span class="detail-label">Date & Time</span>
      <span class="detail-value">${formattedDate} at ${data.time}</span>
    </div>
    <div class="detail-row">
      <span class="detail-label">Passengers</span>
      <span class="detail-value">${data.passengers}</span>
    </div>
    <div class="detail-row">
      <span class="detail-label">Duration/Distance</span>
      <span class="detail-value">${data.duration} ${unitLabels[data.cabType]}</span>
    </div>
    <div class="detail-row" style="border-top: 2px solid #f0f9ff; margin-top: 12px; padding-top: 12px;">
      <span class="detail-label" style="font-size: 1rem; font-weight: 600; color: #0f172a;">Total Fare</span>
      <span class="detail-value" style="font-size: 1.25rem; color: #0891b2;">₹${data.total}</span>
    </div>
  `;
  
  // Show modal
  elements.modal.classList.add('show');
}

// Close Modal
function closeModal() {
  elements.modal.classList.remove('show');
  elements.form.reset();
  
  // Reset cab type selection
  elements.cabCards.forEach(c => c.classList.remove('selected'));
  selectedCabType = null;
  selectedRate = 0;
  
  // Reset pricing display
  elements.selectedTypeDisplay.textContent = 'Not selected';
  elements.baseFareDisplay.textContent = '₹0';
  elements.chargeValueDisplay.textContent = '-';
  elements.totalFareDisplay.textContent = '₹0';
  
  // Disable duration input
  elements.durationInput.disabled = true;
  elements.durationInput.value = '';
}

// Set Minimum Date (today)
function setMinDate() {
  const today = new Date().toISOString().split('T')[0];
  document.getElementById('date').setAttribute('min', today);
}

// Scroll Effects
function initializeScrollEffects() {
  window.addEventListener('scroll', () => {
    const scrolled = window.scrollY > 50;
    elements.navbar.classList.toggle('scrolled', scrolled);
  });
}

// Make closeModal available globally
window.closeModal = closeModal;

// Add loading animation styles dynamically
const style = document.createElement('style');
style.textContent = `
  @keyframes rotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }
  .ti-loader {
    animation: rotate 1s linear infinite;
  }
`;
document.head.appendChild(style);
