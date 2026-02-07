// Production-Level API Integration
// Complete CRUD operations with MongoDB support

const API_BASE_URL = 'http://localhost:8000/api';

// ==================== UTILITY FUNCTIONS ====================
const getToken = () => localStorage.getItem('authToken');
const setToken = (token) => localStorage.setItem('authToken', token);
const removeToken = () => localStorage.removeItem('authToken');
const getUser = () => JSON.parse(localStorage.getItem('currentUser') || '{}');
const setUser = (user) => localStorage.setItem('currentUser', JSON.stringify(user));

const getHeaders = () => ({
  'Content-Type': 'application/json',
  'Authorization': getToken() ? `Token ${getToken()}` : '',
});

// Error handling
const handleError = (error) => {
  console.error('API Error:', error);
  throw error;
};

// ==================== AUTHENTICATION API ====================
const api = {
  auth: {
    register: async (userData) => {
      try {
        const response = await fetch(`${API_BASE_URL}/users/register/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            username: userData.email.split('@')[0],
            email: userData.email,
            password: userData.password,
            password_confirm: userData.password,
            first_name: userData.firstName || '',
            last_name: userData.lastName || '',
          }),
        });
        const data = await response.json();
        if (!response.ok) throw data;
        return data;
      } catch (error) {
        return handleError(error);
      }
    },

    login: async (email, password) => {
      try {
        const response = await fetch(`${API_BASE_URL}/users/login/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            username: email.split('@')[0],
            password,
          }),
        });
        const data = await response.json();
        if (!response.ok) throw data;
        
        setToken(data.token);
        setUser(data.user);
        return data;
      } catch (error) {
        return handleError(error);
      }
    },

    logout: async () => {
      try {
        await fetch(`${API_BASE_URL}/users/logout/`, {
          method: 'POST',
          headers: getHeaders(),
        });
        removeToken();
        localStorage.removeItem('currentUser');
      } catch (error) {
        return handleError(error);
      }
    },

    getCurrentUser: async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/users/me/`, {
          headers: getHeaders(),
        });
        const data = await response.json();
        if (!response.ok) throw data;
        return data;
      } catch (error) {
        return handleError(error);
      }
    },

    updateProfile: async (userId, userData) => {
      try {
        const response = await fetch(`${API_BASE_URL}/users/${userId}/update_profile/`, {
          method: 'PUT',
          headers: getHeaders(),
          body: JSON.stringify(userData),
        });
        const data = await response.json();
        if (!response.ok) throw data;
        return data;
      } catch (error) {
        return handleError(error);
      }
    },
  },

  // ==================== DESTINATIONS CRUD ====================
  destinations: {
    getAll: async (page = 1) => {
      try {
        const response = await fetch(`${API_BASE_URL}/destinations/?page=${page}`, {
          headers: getHeaders(),
        });
        const data = await response.json();
        if (!response.ok) throw data;
        return data;
      } catch (error) {
        return handleError(error);
      }
    },

    getById: async (id) => {
      try {
        const response = await fetch(`${API_BASE_URL}/destinations/${id}/`, {
          headers: getHeaders(),
        });
        const data = await response.json();
        if (!response.ok) throw data;
        return data;
      } catch (error) {
        return handleError(error);
      }
    },

    create: async (destinationData) => {
      try {
        const response = await fetch(`${API_BASE_URL}/destinations/`, {
          method: 'POST',
          headers: getHeaders(),
          body: JSON.stringify(destinationData),
        });
        const data = await response.json();
        if (!response.ok) throw data;
        return data;
      } catch (error) {
        return handleError(error);
      }
    },

    update: async (id, destinationData) => {
      try {
        const response = await fetch(`${API_BASE_URL}/destinations/${id}/`, {
          method: 'PUT',
          headers: getHeaders(),
          body: JSON.stringify(destinationData),
        });
        const data = await response.json();
        if (!response.ok) throw data;
        return data;
      } catch (error) {
        return handleError(error);
      }
    },

    delete: async (id) => {
      try {
        const response = await fetch(`${API_BASE_URL}/destinations/${id}/`, {
          method: 'DELETE',
          headers: getHeaders(),
        });
        if (!response.ok) throw { error: 'Failed to delete' };
        return { success: true };
      } catch (error) {
        return handleError(error);
      }
    },

    search: async (query) => {
      try {
        const response = await fetch(`${API_BASE_URL}/destinations/search/?q=${encodeURIComponent(query)}`, {
          headers: getHeaders(),
        });
        const data = await response.json();
        if (!response.ok) throw data;
        return data;
      } catch (error) {
        return handleError(error);
      }
    },

    getPopular: async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/destinations/popular/`, {
          headers: getHeaders(),
        });
        const data = await response.json();
        if (!response.ok) throw data;
        return data;
      } catch (error) {
        return handleError(error);
      }
    },

    getByCountry: async (country) => {
      try {
        const response = await fetch(`${API_BASE_URL}/destinations/by_country/?country=${encodeURIComponent(country)}`, {
          headers: getHeaders(),
        });
        const data = await response.json();
        if (!response.ok) throw data;
        return data;
      } catch (error) {
        return handleError(error);
      }
    },
  },

  // ==================== HOTELS CRUD ====================
  hotels: {
    getAll: async (page = 1) => {
      try {
        const response = await fetch(`${API_BASE_URL}/hotels/?page=${page}`, {
          headers: getHeaders(),
        });
        const data = await response.json();
        if (!response.ok) throw data;
        return data;
      } catch (error) {
        return handleError(error);
      }
    },

    getById: async (id) => {
      try {
        const response = await fetch(`${API_BASE_URL}/hotels/${id}/`, {
          headers: getHeaders(),
        });
        const data = await response.json();
        if (!response.ok) throw data;
        return data;
      } catch (error) {
        return handleError(error);
      }
    },

    create: async (hotelData) => {
      try {
        const response = await fetch(`${API_BASE_URL}/hotels/`, {
          method: 'POST',
          headers: getHeaders(),
          body: JSON.stringify(hotelData),
        });
        const data = await response.json();
        if (!response.ok) throw data;
        return data;
      } catch (error) {
        return handleError(error);
      }
    },

    update: async (id, hotelData) => {
      try {
        const response = await fetch(`${API_BASE_URL}/hotels/${id}/`, {
          method: 'PUT',
          headers: getHeaders(),
          body: JSON.stringify(hotelData),
        });
        const data = await response.json();
        if (!response.ok) throw data;
        return data;
      } catch (error) {
        return handleError(error);
      }
    },

    delete: async (id) => {
      try {
        const response = await fetch(`${API_BASE_URL}/hotels/${id}/`, {
          method: 'DELETE',
          headers: getHeaders(),
        });
        if (!response.ok) throw { error: 'Failed to delete' };
        return { success: true };
      } catch (error) {
        return handleError(error);
      }
    },

    search: async (query) => {
      try {
        const response = await fetch(`${API_BASE_URL}/hotels/search/?q=${encodeURIComponent(query)}`, {
          headers: getHeaders(),
        });
        const data = await response.json();
        if (!response.ok) throw data;
        return data;
      } catch (error) {
        return handleError(error);
      }
    },

    getByPriceRange: async (minPrice, maxPrice) => {
      try {
        const response = await fetch(
          `${API_BASE_URL}/hotels/by_price_range/?min_price=${minPrice}&max_price=${maxPrice}`,
          { headers: getHeaders() }
        );
        const data = await response.json();
        if (!response.ok) throw data;
        return data;
      } catch (error) {
        return handleError(error);
      }
    },

    getAvailable: async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/hotels/available/`, {
          headers: getHeaders(),
        });
        const data = await response.json();
        if (!response.ok) throw data;
        return data;
      } catch (error) {
        return handleError(error);
      }
    },
  },

  // ==================== CABS CRUD ====================
  cabs: {
    getAll: async (page = 1) => {
      try {
        const response = await fetch(`${API_BASE_URL}/cabs/?page=${page}`, {
          headers: getHeaders(),
        });
        const data = await response.json();
        if (!response.ok) throw data;
        return data;
      } catch (error) {
        return handleError(error);
      }
    },

    getById: async (id) => {
      try {
        const response = await fetch(`${API_BASE_URL}/cabs/${id}/`, {
          headers: getHeaders(),
        });
        const data = await response.json();
        if (!response.ok) throw data;
        return data;
      } catch (error) {
        return handleError(error);
      }
    },

    create: async (cabData) => {
      try {
        const response = await fetch(`${API_BASE_URL}/cabs/`, {
          method: 'POST',
          headers: getHeaders(),
          body: JSON.stringify(cabData),
        });
        const data = await response.json();
        if (!response.ok) throw data;
        return data;
      } catch (error) {
        return handleError(error);
      }
    },

    update: async (id, cabData) => {
      try {
        const response = await fetch(`${API_BASE_URL}/cabs/${id}/`, {
          method: 'PUT',
          headers: getHeaders(),
          body: JSON.stringify(cabData),
        });
        const data = await response.json();
        if (!response.ok) throw data;
        return data;
      } catch (error) {
        return handleError(error);
      }
    },

    delete: async (id) => {
      try {
        const response = await fetch(`${API_BASE_URL}/cabs/${id}/`, {
          method: 'DELETE',
          headers: getHeaders(),
        });
        if (!response.ok) throw { error: 'Failed to delete' };
        return { success: true };
      } catch (error) {
        return handleError(error);
      }
    },

    filter: async (vehicleType, minPrice, maxPrice) => {
      try {
        const params = new URLSearchParams();
        if (vehicleType) params.append('vehicle_type', vehicleType);
        if (minPrice) params.append('min_price', minPrice);
        if (maxPrice) params.append('max_price', maxPrice);

        const response = await fetch(`${API_BASE_URL}/cabs/filter/?${params.toString()}`, {
          headers: getHeaders(),
        });
        const data = await response.json();
        if (!response.ok) throw data;
        return data;
      } catch (error) {
        return handleError(error);
      }
    },

    getByCompany: async (company) => {
      try {
        const response = await fetch(`${API_BASE_URL}/cabs/by_company/?company=${encodeURIComponent(company)}`, {
          headers: getHeaders(),
        });
        const data = await response.json();
        if (!response.ok) throw data;
        return data;
      } catch (error) {
        return handleError(error);
      }
    },

    getAvailable: async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/cabs/available/`, {
          headers: getHeaders(),
        });
        const data = await response.json();
        if (!response.ok) throw data;
        return data;
      } catch (error) {
        return handleError(error);
      }
    },
  },

  // ==================== BOOKINGS CRUD ====================
  bookings: {
    getAll: async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/bookings/`, {
          headers: getHeaders(),
        });
        const data = await response.json();
        if (!response.ok) throw data;
        return data;
      } catch (error) {
        return handleError(error);
      }
    },

    getById: async (id) => {
      try {
        const response = await fetch(`${API_BASE_URL}/bookings/${id}/`, {
          headers: getHeaders(),
        });
        const data = await response.json();
        if (!response.ok) throw data;
        return data;
      } catch (error) {
        return handleError(error);
      }
    },

    create: async (bookingData) => {
      try {
        const response = await fetch(`${API_BASE_URL}/bookings/`, {
          method: 'POST',
          headers: getHeaders(),
          body: JSON.stringify(bookingData),
        });
        const data = await response.json();
        if (!response.ok) throw data;
        return data;
      } catch (error) {
        return handleError(error);
      }
    },

    update: async (id, bookingData) => {
      try {
        const response = await fetch(`${API_BASE_URL}/bookings/${id}/`, {
          method: 'PUT',
          headers: getHeaders(),
          body: JSON.stringify(bookingData),
        });
        const data = await response.json();
        if (!response.ok) throw data;
        return data;
      } catch (error) {
        return handleError(error);
      }
    },

    delete: async (id) => {
      try {
        const response = await fetch(`${API_BASE_URL}/bookings/${id}/`, {
          method: 'DELETE',
          headers: getHeaders(),
        });
        if (!response.ok) throw { error: 'Failed to delete' };
        return { success: true };
      } catch (error) {
        return handleError(error);
      }
    },

    cancel: async (id) => {
      try {
        const response = await fetch(`${API_BASE_URL}/bookings/${id}/cancel/`, {
          method: 'POST',
          headers: getHeaders(),
        });
        const data = await response.json();
        if (!response.ok) throw data;
        return data;
      } catch (error) {
        return handleError(error);
      }
    },

    getMyBookings: async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/bookings/my_bookings/`, {
          headers: getHeaders(),
        });
        const data = await response.json();
        if (!response.ok) throw data;
        return data;
      } catch (error) {
        return handleError(error);
      }
    },

    getPending: async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/bookings/pending/`, {
          headers: getHeaders(),
        });
        const data = await response.json();
        if (!response.ok) throw data;
        return data;
      } catch (error) {
        return handleError(error);
      }
    },

    getConfirmed: async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/bookings/confirmed/`, {
          headers: getHeaders(),
        });
        const data = await response.json();
        if (!response.ok) throw data;
        return data;
      } catch (error) {
        return handleError(error);
      }
    },
  },

  // ==================== CONTACTS CRUD ====================
  contacts: {
    create: async (contactData) => {
      try {
        const response = await fetch(`${API_BASE_URL}/contacts/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(contactData),
        });
        const data = await response.json();
        if (!response.ok) throw data;
        return data;
      } catch (error) {
        return handleError(error);
      }
    },

    getAll: async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/contacts/`, {
          headers: getHeaders(),
        });
        const data = await response.json();
        if (!response.ok) throw data;
        return data;
      } catch (error) {
        return handleError(error);
      }
    },

    getById: async (id) => {
      try {
        const response = await fetch(`${API_BASE_URL}/contacts/${id}/`, {
          headers: getHeaders(),
        });
        const data = await response.json();
        if (!response.ok) throw data;
        return data;
      } catch (error) {
        return handleError(error);
      }
    },

    delete: async (id) => {
      try {
        const response = await fetch(`${API_BASE_URL}/contacts/${id}/`, {
          method: 'DELETE',
          headers: getHeaders(),
        });
        if (!response.ok) throw { error: 'Failed to delete' };
        return { success: true };
      } catch (error) {
        return handleError(error);
      }
    },

    markAsRead: async (id) => {
      try {
        const response = await fetch(`${API_BASE_URL}/contacts/${id}/mark_as_read/`, {
          method: 'POST',
          headers: getHeaders(),
        });
        const data = await response.json();
        if (!response.ok) throw data;
        return data;
      } catch (error) {
        return handleError(error);
      }
    },

    markAsResolved: async (id) => {
      try {
        const response = await fetch(`${API_BASE_URL}/contacts/${id}/mark_as_resolved/`, {
          method: 'POST',
          headers: getHeaders(),
        });
        const data = await response.json();
        if (!response.ok) throw data;
        return data;
      } catch (error) {
        return handleError(error);
      }
    },

    getUnread: async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/contacts/unread/`, {
          headers: getHeaders(),
        });
        const data = await response.json();
        if (!response.ok) throw data;
        return data;
      } catch (error) {
        return handleError(error);
      }
    },
  },
};
