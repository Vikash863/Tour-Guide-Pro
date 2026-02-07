// API Base URL - Django Backend
const API_BASE_URL = 'http://localhost:8000/api';

// Local storage for token
const getToken = () => localStorage.getItem('authToken');
const setToken = (token) => localStorage.setItem('authToken', token);
const removeToken = () => localStorage.removeItem('authToken');

// Headers with authentication
const getHeaders = () => ({
  'Content-Type': 'application/json',
  'Authorization': getToken() ? `Token ${getToken()}` : '',
});

// API calls
const api = {
  // Auth
  register: async (name, email, password, phone = '') => {
    const response = await fetch(`${API_BASE_URL}/users/register/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        username: email.split('@')[0],
        email, 
        password, 
        password_confirm: password,
        first_name: name.split(' ')[0],
        last_name: name.split(' ').slice(1).join(' ')
      }),
    });
    return response.json();
  },

  login: async (email, password) => {
    const response = await fetch(`${API_BASE_URL}/users/login/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        username: email.split('@')[0],  // Extract username from email
        password 
      }),
    });
    return response.json();
  },

  getCurrentUser: async () => {
    const response = await fetch(`${API_BASE_URL}/users/me/`, {
      headers: getHeaders(),
    });
    return response.json();
  },

  // Destinations
  getAllDestinations: async () => {
    const response = await fetch(`${API_BASE_URL}/destinations/`, {
      headers: getHeaders(),
    });
    return response.json();
  },

  searchDestination: async (name) => {
    const response = await fetch(`${API_BASE_URL}/destinations/search/?name=${name}`, {
      headers: getHeaders(),
    });
    return response.json();
  },

  getDestinationById: async (id) => {
    const response = await fetch(`${API_BASE_URL}/destinations/${id}/`, {
      headers: getHeaders(),
    });
    return response.json();
  },

  // Hotels
  getAllHotels: async () => {
    const response = await fetch(`${API_BASE_URL}/hotels/`, {
      headers: getHeaders(),
    });
    return response.json();
  },

  searchHotels: async (location) => {
    const response = await fetch(`${API_BASE_URL}/hotels/search/?location=${location}`, {
      headers: getHeaders(),
    });
    return response.json();
  },

  getHotelById: async (id) => {
    const response = await fetch(`${API_BASE_URL}/hotels/${id}/`, {
      headers: getHeaders(),
    });
    return response.json();
  },

  // Cabs
  getAllCabs: async () => {
    const response = await fetch(`${API_BASE_URL}/cabs/`, {
      headers: getHeaders(),
    });
    return response.json();
  },

  filterCabs: async (vehicleType = '', minPrice = '', maxPrice = '') => {
    let url = `${API_BASE_URL}/cabs/filter/`;
    const params = [];
    if (vehicleType) params.push(`vehicleType=${vehicleType}`);
    if (minPrice) params.push(`minPrice=${minPrice}`);
    if (maxPrice) params.push(`maxPrice=${maxPrice}`);
    if (params.length) url += '?' + params.join('&');

    const response = await fetch(url, {
      headers: getHeaders(),
    });
    return response.json();
  },

  getCabById: async (id) => {
    const response = await fetch(`${API_BASE_URL}/cabs/${id}/`, {
      headers: getHeaders(),
    });
    return response.json();
  },

  // Bookings
  getUserBookings: async () => {
    const response = await fetch(`${API_BASE_URL}/bookings/`, {
      headers: getHeaders(),
    });
    return response.json();
  },

  createBooking: async (bookingData) => {
    const response = await fetch(`${API_BASE_URL}/bookings/`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(bookingData),
    });
    return response.json();
  },

  updateBooking: async (id, bookingData) => {
    const response = await fetch(`${API_BASE_URL}/bookings/${id}/`, {
      method: 'PUT',
      headers: getHeaders(),
      body: JSON.stringify(bookingData),
    });
    return response.json();
  },

  cancelBooking: async (id) => {
    const response = await fetch(`${API_BASE_URL}/bookings/${id}/cancel/`, {
      method: 'POST',
      headers: getHeaders(),
    });
    return response.json();
  },

  // Contact
  submitContact: async (name, email, phone, subject, message) => {
    const response = await fetch(`${API_BASE_URL}/contacts/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, phone, subject, message }),
    });
    return response.json();
  },
};

// Auth helper functions
const auth = {
  isLoggedIn: () => !!getToken(),

  logout: () => {
    removeToken();
    localStorage.removeItem('user');
    window.location.href = '/';
  },

  getUser: () => {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  },
};
