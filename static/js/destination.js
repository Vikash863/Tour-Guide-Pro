// ============================================
// TOUR GUIDE PRO - DESTINATION PAGE
// Ultra-Modern Interactive Experience
// ============================================

// API Keys
const WEATHER_API_KEY = 'e373769e2050490599b134019252909';
const UNSPLASH_ACCESS_KEY = 'gpfwZz-jHdDm6SmUfqlF-vbGYw2x47T_IQA_8hS8OuQ';

// DOM Elements
const elements = {
  destinationInput: document.getElementById('destinationInput'),
  emptyState: document.getElementById('emptyState'),
  loadingState: document.getElementById('loadingState'),
  errorState: document.getElementById('errorState'),
  errorMessage: document.getElementById('errorMessage'),
  destinationResult: document.getElementById('destinationResult'),
  destinationImage: document.getElementById('destinationImage'),
  destinationName: document.getElementById('destinationName'),
  infoGrid: document.getElementById('infoGrid'),
  weatherCard: document.getElementById('weatherCard'),
  attractionsCard: document.getElementById('attractionsCard'),
  restaurantsCard: document.getElementById('restaurantsCard'),
  tempValue: document.getElementById('tempValue'),
  weatherCondition: document.getElementById('weatherCondition'),
  feelsLike: document.getElementById('feelsLike'),
  humidity: document.getElementById('humidity'),
  windSpeed: document.getElementById('windSpeed'),
  attractionsList: document.getElementById('attractionsList'),
  restaurantsList: document.getElementById('restaurantsList'),
  navbar: document.getElementById('navbar')
};

// Simulated data for attractions and restaurants
const cityData = {
  default: {
    attractions: [
      { name: 'City Palace', type: 'Historical Monument', rating: 4.5 },
      { name: 'Local Museum', type: 'Museum & Gallery', rating: 4.3 },
      { name: 'Botanical Garden', type: 'Nature & Parks', rating: 4.4 },
      { name: 'Central Market', type: 'Shopping District', rating: 4.2 },
      { name: 'Sunset Point', type: 'Scenic Viewpoint', rating: 4.7 }
    ],
    restaurants: [
      { name: 'Spice Villa', cuisine: 'Indian Cuisine', rating: 4.6 },
      { name: 'Tandoori Treats', cuisine: 'North Indian', rating: 4.4 },
      { name: 'Café Delight', cuisine: 'Café & Bakery', rating: 4.3 },
      { name: 'The Garden Kitchen', cuisine: 'Multi-Cuisine', rating: 4.5 },
      { name: 'Street Food Corner', cuisine: 'Local Street Food', rating: 4.2 }
    ]
  }
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
  initializeEventListeners();
  initializeScrollEffects();
});

// Event Listeners
function initializeEventListeners() {
  // Enter key search
  elements.destinationInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      searchDestination();
    }
  });

  // Input focus effects
  elements.destinationInput.addEventListener('focus', () => {
    elements.destinationInput.parentElement.parentElement.classList.add('focused');
  });

  elements.destinationInput.addEventListener('blur', () => {
    elements.destinationInput.parentElement.parentElement.classList.remove('focused');
  });
}

// Scroll Effects
function initializeScrollEffects() {
  window.addEventListener('scroll', () => {
    const scrolled = window.scrollY > 50;
    elements.navbar.classList.toggle('scrolled', scrolled);
  });
}

// Show/Hide State Functions
function showState(stateName) {
  // Hide all states
  elements.emptyState.classList.add('hidden');
  elements.loadingState.classList.add('hidden');
  elements.errorState.classList.add('hidden');
  elements.destinationResult.classList.add('hidden');
  elements.infoGrid.classList.add('hidden');

  // Remove visible classes
  elements.destinationResult.classList.remove('visible');
  elements.weatherCard.classList.remove('visible');
  elements.attractionsCard.classList.remove('visible');
  elements.restaurantsCard.classList.remove('visible');

  // Show requested state
  switch (stateName) {
    case 'empty':
      elements.emptyState.classList.remove('hidden');
      break;
    case 'loading':
      elements.loadingState.classList.remove('hidden');
      break;
    case 'error':
      elements.errorState.classList.remove('hidden');
      break;
    case 'results':
      elements.destinationResult.classList.remove('hidden');
      elements.infoGrid.classList.remove('hidden');
      // Trigger animations with stagger
      setTimeout(() => elements.destinationResult.classList.add('visible'), 100);
      setTimeout(() => elements.weatherCard.classList.add('visible'), 200);
      setTimeout(() => elements.attractionsCard.classList.add('visible'), 400);
      setTimeout(() => elements.restaurantsCard.classList.add('visible'), 600);
      break;
  }
}

// Main Search Function
async function searchDestination() {
  const city = elements.destinationInput.value.trim();
  
  if (!city) {
    shakeInput();
    return;
  }

  showState('loading');
  scrollToResults();

  try {
    // Fetch data in parallel
    const [weatherData, imageUrl] = await Promise.all([
      fetchWeather(city),
      fetchImage(city)
    ]);

    // Update UI with results
    updateDestinationCard(city, imageUrl);
    updateWeatherCard(weatherData);
    updateAttractionsCard(city);
    updateRestaurantsCard(city);

    showState('results');

  } catch (error) {
    console.error('Search error:', error);
    elements.errorMessage.textContent = error.message || 'Unable to fetch destination data. Please try again.';
    showState('error');
  }
}

// Fetch Weather Data
async function fetchWeather(city) {
  const response = await fetch(
    `https://api.weatherapi.com/v1/current.json?key=${WEATHER_API_KEY}&q=${encodeURIComponent(city)}&aqi=no`
  );

  if (!response.ok) {
    throw new Error('City not found. Please check the spelling and try again.');
  }

  return response.json();
}

// Fetch City Image
async function fetchImage(city) {
  try {
    const response = await fetch(
      `https://api.unsplash.com/search/photos?query=${encodeURIComponent(city)}&client_id=${UNSPLASH_ACCESS_KEY}&per_page=1&orientation=landscape`
    );
    
    const data = await response.json();
    
    if (data.results && data.results.length > 0) {
      return data.results[0].urls.regular;
    }
    
    // Fallback image
    return `https://source.unsplash.com/1200x600/?${encodeURIComponent(city)},travel,city`;
  } catch {
    return `https://source.unsplash.com/1200x600/?${encodeURIComponent(city)},travel,city`;
  }
}

// Update Destination Card
function updateDestinationCard(city, imageUrl) {
  elements.destinationName.textContent = capitalizeCity(city);
  elements.destinationImage.src = imageUrl;
  elements.destinationImage.alt = `${city} - Travel Destination`;
}

// Update Weather Card
function updateWeatherCard(data) {
  const current = data.current;
  
  elements.tempValue.textContent = Math.round(current.temp_c);
  elements.weatherCondition.textContent = current.condition.text;
  elements.feelsLike.textContent = `${Math.round(current.feelslike_c)}°`;
  elements.humidity.textContent = `${current.humidity}%`;
  elements.windSpeed.textContent = `${current.wind_kph} km/h`;
}

// Update Attractions Card
function updateAttractionsCard(city) {
  const attractions = cityData.default.attractions;
  
  elements.attractionsList.innerHTML = attractions.map((attraction, index) => `
    <li class="info-item" style="animation: slideInRight 0.5s ease ${index * 0.1}s both;">
      <div class="info-item-icon">
        <i class="icon-landmark"></i>
      </div>
      <div class="info-item-content">
        <div class="info-item-name">${attraction.name}</div>
        <div class="info-item-meta">${attraction.type}</div>
      </div>
      <div class="rating">
        ${generateStars(attraction.rating)}
        <span class="text-small" style="margin-left: 4px;">${attraction.rating}</span>
      </div>
    </li>
  `).join('');
}

// Update Restaurants Card
function updateRestaurantsCard(city) {
  const restaurants = cityData.default.restaurants;
  
  elements.restaurantsList.innerHTML = restaurants.map((restaurant, index) => `
    <li class="info-item" style="animation: slideInRight 0.5s ease ${index * 0.1}s both;">
      <div class="info-item-icon">
        <i class="icon-utensils"></i>
      </div>
      <div class="info-item-content">
        <div class="info-item-name">${restaurant.name}</div>
        <div class="info-item-meta">${restaurant.cuisine}</div>
      </div>
      <div class="rating">
        ${generateStars(restaurant.rating)}
        <span class="text-small" style="margin-left: 4px;">${restaurant.rating}</span>
      </div>
    </li>
  `).join('');
}

// Generate Star Rating HTML
function generateStars(rating) {
  const fullStars = Math.floor(rating);
  const hasHalf = rating % 1 >= 0.5;
  let stars = '';
  
  for (let i = 0; i < fullStars; i++) {
    stars += '<i class="icon-star" style="fill: currentColor;"></i>';
  }
  
  if (hasHalf && fullStars < 5) {
    stars += '<i class="icon-star-half" style="fill: currentColor;"></i>';
  }
  
  const emptyStars = 5 - fullStars - (hasHalf ? 1 : 0);
  for (let i = 0; i < emptyStars; i++) {
    stars += '<i class="icon-star" style="opacity: 0.3;"></i>';
  }
  
  return stars;
}

// Utility Functions
function capitalizeCity(city) {
  return city.split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(' ');
}

function scrollToResults() {
  setTimeout(() => {
    document.getElementById('resultsSection').scrollIntoView({ 
      behavior: 'smooth',
      block: 'start'
    });
  }, 300);
}

function shakeInput() {
  const searchBox = elements.destinationInput.parentElement.parentElement;
  searchBox.style.animation = 'shake 0.5s ease';
  setTimeout(() => {
    searchBox.style.animation = '';
  }, 500);
}

// Add shake animation dynamically
const style = document.createElement('style');
style.textContent = `
  @keyframes shake {
    0%, 100% { transform: translateX(0); }
    10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
    20%, 40%, 60%, 80% { transform: translateX(5px); }
  }
`;
document.head.appendChild(style);
