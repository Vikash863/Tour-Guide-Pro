// API Base URL - Django Backend
const API_BASE_URL = '/api';

// Local storage for token
const getToken = () => localStorage.getItem('authToken');
const setToken = (token) => localStorage.setItem('authToken', token);
const removeToken = () => localStorage.removeItem('authToken');

// Headers with authentication
const getHeaders = () => {
    const headers = { 'Content-Type': 'application/json' };
    const token = getToken();
    if (token) headers['Authorization'] = `Token ${token}`;
    return headers;
};

// API calls
const api = {
    // Auth - using correct endpoints
    register: async (username, email, password) => {
        const response = await fetch(`${API_BASE_URL}/users/register/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, password, password_confirm: password }),
        });
        return response.json();
    },

    login: async (username, password) => {
        const response = await fetch(`${API_BASE_URL}/users/login/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password }),
        });
        return response.json();
    },

    logout: async () => {
        const response = await fetch(`${API_BASE_URL}/users/logout/`, {
            method: 'POST',
            headers: getHeaders(),
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

    getPopularDestinations: async () => {
        const response = await fetch(`${API_BASE_URL}/destinations/popular/`, {
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

    getAvailableHotels: async () => {
        const response = await fetch(`${API_BASE_URL}/hotels/available/`, {
            headers: getHeaders(),
        });
        return response.json();
    },

    // Bookings
    getUserBookings: async () => {
        const response = await fetch(`${API_BASE_URL}/bookings/my_bookings/`, {
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
