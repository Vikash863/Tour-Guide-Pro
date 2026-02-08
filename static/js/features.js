/**
 * Tour Guide Pro - All Features API Integration
 * Complete JavaScript API for 15 Features + Bonus Features
 */

const API_BASE = '/api';

// ==================== AUTHENTICATION ====================
const AuthAPI = {
    async login(username, password) {
        const response = await fetch(`${API_BASE}/auth/login/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        return response.json();
    },

    async register(userData) {
        const response = await fetch(`${API_BASE}/register/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(userData)
        });
        return response.json();
    },

    getToken() {
        return localStorage.getItem('token');
    },

    setToken(token) {
        localStorage.setItem('token', token);
    },

    logout() {
        localStorage.removeItem('token');
        window.location.href = '/login/';
    },

    isAuthenticated() {
        return !!this.getToken();
    }
};

// ==================== 1) SMART TRIP ASSISTANT (AI) ====================
const TripAssistant = {
    async generatePlan(data) {
        const response = await fetch(`${API_BASE}/trip-plans/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${AuthAPI.getToken()}`
            },
            body: JSON.stringify(data)
        });
        return response.json();
    },

    async getPlans() {
        const response = await fetch(`${API_BASE}/trip-plans/`, {
            headers: { 'Authorization': `Token ${AuthAPI.getToken()}` }
        });
        return response.json();
    },

    async getPlan(id) {
        const response = await fetch(`${API_BASE}/trip-plans/${id}/`, {
            headers: { 'Authorization': `Token ${AuthAPI.getToken()}` }
        });
        return response.json();
    },

    async regenerate(id, interests) {
        const response = await fetch(`${API_BASE}/trip-plans/${id}/regenerate/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${AuthAPI.getToken()}`
            },
            body: JSON.stringify({ interests })
        });
        return response.json();
    },

    async share(id) {
        const response = await fetch(`${API_BASE}/trip-plans/${id}/share/`, {
            headers: { 'Authorization': `Token ${AuthAPI.getToken()}` }
        });
        return response.json();
    },

    async savePreferences(prefs) {
        const response = await fetch(`${API_BASE}/trip-preferences/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${AuthAPI.getToken()}`
            },
            body: JSON.stringify(prefs)
        });
        return response.json();
    },

    async getPreferences() {
        const response = await fetch(`${API_BASE}/trip-preferences/my/`, {
            headers: { 'Authorization': `Token ${AuthAPI.getToken()}` }
        });
        return response.json();
    }
};

// ==================== 2) TRIP BUDGET CALCULATOR ====================
const BudgetCalculator = {
    async createTracker(data) {
        const response = await fetch(`${API_BASE}/budget-trackers/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${AuthAPI.getToken()}`
            },
            body: JSON.stringify(data)
        });
        return response.json();
    },

    async getTrackers() {
        const response = await fetch(`${API_BASE}/budget-trackers/`, {
            headers: { 'Authorization': `Token ${AuthAPI.getToken()}` }
        });
        return response.json();
    },

    async getSummary(id) {
        const response = await fetch(`${API_BASE}/budget-trackers/${id}/summary/`, {
            headers: { 'Authorization': `Token ${AuthAPI.getToken()}` }
        });
        return response.json();
    },

    async updateCost(id, category, amount) {
        const response = await fetch(`${API_BASE}/budget-trackers/${id}/update_cost/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${AuthAPI.getToken()}`
            },
            body: JSON.stringify({ category, amount })
        });
        return response.json();
    },

    getCurrencies() {
        return [
            { code: 'INR', name: 'Indian Rupee', symbol: '₹' },
            { code: 'USD', name: 'US Dollar', symbol: '$' },
            { code: 'EUR', name: 'Euro', symbol: '€' },
            { code: 'GBP', name: 'British Pound', symbol: '£' }
        ];
    },

    async convertCurrency(amount, fromCurrency, toCurrency) {
        const response = await fetch(`${API_BASE}/currency/convert/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ amount, from_currency: fromCurrency, to_currency: toCurrency })
        });
        return response.json();
    }
};

// ==================== 3) NEARBY PLACES FINDER ====================
const NearbyPlaces = {
    async searchPlaces(lat, lng, type = 'tourist_attraction') {
        const response = await fetch(
            `${API_BASE}/nearby-places/search/?latitude=${lat}&longitude=${lng}&type=${type}`,
            { headers: { 'Authorization': `Token ${AuthAPI.getToken()}` } }
        );
        return response.json();
    },

    async savePlace(placeData) {
        const response = await fetch(`${API_BASE}/nearby-places/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${AuthAPI.getToken()}`
            },
            body: JSON.stringify(placeData)
        });
        return response.json();
    },

    async getSavedPlaces() {
        const response = await fetch(`${API_BASE}/nearby-places/`, {
            headers: { 'Authorization': `Token ${AuthAPI.getToken()}` }
        });
        return response.json();
    },

    // Google Maps integration helper
    initGoogleMaps(apiKey) {
        if (window.google) return;
        const script = document.createElement('script');
        script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&libraries=places`;
        document.head.appendChild(script);
    },

    getPlaceTypes() {
        return [
            { id: 'tourist_attraction', name: 'Tourist Attractions' },
            { id: 'restaurant', name: 'Restaurants' },
            { id: 'hotel', name: 'Hotels' },
            { id: 'shopping_mall', name: 'Shopping Malls' },
            { id: 'museum', name: 'Museums' },
            { id: 'park', name: 'Parks' },
            { id: 'hospital', name: 'Hospitals' }
        ];
    }
};

// ==================== 4) OFFLINE TRAVEL GUIDE ====================
const OfflineGuide = {
    async getGuides(destinationId) {
        const response = await fetch(`${API_BASE}/offline-guides/by_destination/?destination_id=${destinationId}`);
        return response.json();
    },

    async createGuide(data) {
        const response = await fetch(`${API_BASE}/offline-guides/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return response.json();
    },

    async downloadPDF(guideId) {
        window.open(`${API_BASE}/offline-guides/${guideId}/download/`, '_blank');
    }
};

const TripChecklist = {
    async create(data) {
        const response = await fetch(`${API_BASE}/trip-checklists/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${AuthAPI.getToken()}`
            },
            body: JSON.stringify(data)
        });
        return response.json();
    },

    async getChecklists() {
        const response = await fetch(`${API_BASE}/trip-checklists/`, {
            headers: { 'Authorization': `Token ${AuthAPI.getToken()}` }
        });
        return response.json();
    },

    async updateItems(id, items) {
        const response = await fetch(`${API_BASE}/trip-checklists/${id}/update_items/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${AuthAPI.getToken()}`
            },
            body: JSON.stringify({ items })
        });
        return response.json();
    },

    getDefaultItems() {
        return {
            documents: ['Passport', 'Visa', 'ID Proof', 'Booking Confirmations', 'Travel Insurance'],
            clothing: ['T-Shirts', 'Jeans', 'Jackets', 'Comfortable Shoes', 'Swimwear'],
            electronics: ['Phone Charger', 'Power Bank', 'Camera', 'Adapter'],
            toiletries: ['Toothbrush', 'Toothpaste', 'Shampoo', 'Sunscreen', 'Medicines'],
            miscellaneous: ['Cash', 'Credit Cards', 'sunglasses', 'Hat']
        };
    }
};

// ==================== 5) TRAVEL MEMORY SCRAPBOOK ====================
const TravelMemory = {
    async create(data) {
        const response = await fetch(`${API_BASE}/travel-memories/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${AuthAPI.getToken()}`
            },
            body: JSON.stringify(data)
        });
        return response.json();
    },

    async getMemories() {
        const response = await fetch(`${API_BASE}/travel-memories/`, {
            headers: { 'Authorization': `Token ${AuthAPI.getToken()}` }
        });
        return response.json();
    },

    async addPhoto(memoryId, photo, caption = '') {
        const formData = new FormData();
        formData.append('photo', photo);
        formData.append('caption', caption);
        const response = await fetch(`${API_BASE}/travel-memories/${memoryId}/add_photo/`, {
            method: 'POST',
            headers: { 'Authorization': `Token ${AuthAPI.getToken()}` },
            body: formData
        });
        return response.json();
    },

    async addNote(memoryId, content) {
        const response = await fetch(`${API_BASE}/travel-memories/${memoryId}/add_note/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${AuthAPI.getToken()}`
            },
            body: JSON.stringify({ content })
        });
        return response.json();
    },

    async share(memoryId) {
        const response = await fetch(`${API_BASE}/travel-memories/${memoryId}/share/`, {
            headers: { 'Authorization': `Token ${AuthAPI.getToken()}` }
        });
        return response.json();
    }
};

// ==================== 6) GROUP TRIP PLANNER ====================
const GroupTrip = {
    async create(data) {
        const response = await fetch(`${API_BASE}/group-trips/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${AuthAPI.getToken()}`
            },
            body: JSON.stringify(data)
        });
        return response.json();
    },

    async getTrips() {
        const response = await fetch(`${API_BASE}/group-trips/`, {
            headers: { 'Authorization': `Token ${AuthAPI.getToken()}` }
        });
        return response.json();
    },

    async inviteMember(tripId, userId) {
        const response = await fetch(`${API_BASE}/group-trips/${tripId}/invite/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${AuthAPI.getToken()}`
            },
            body: JSON.stringify({ user_id: userId })
        });
        return response.json();
    },

    async createPoll(tripId, pollData) {
        const response = await fetch(`${API_BASE}/group-trips/${tripId}/create_poll/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${AuthAPI.getToken()}`
            },
            body: JSON.stringify(pollData)
        });
        return response.json();
    },

    async getExpenses(tripId) {
        const response = await fetch(`${API_BASE}/group-trips/${tripId}/expenses/`, {
            headers: { 'Authorization': `Token ${AuthAPI.getToken()}` }
        });
        return response.json();
    }
};

// ==================== 7) RECOMMENDATION ENGINE ====================
const Recommendations = {
    async getPersonalized() {
        const response = await fetch(`${API_BASE}/recommendations/`, {
            headers: { 'Authorization': `Token ${AuthAPI.getToken()}` }
        });
        return response.json();
    },

    async trackView(id) {
        await fetch(`${API_BASE}/recommendations/${id}/view/`, {
            method: 'POST',
            headers: { 'Authorization': `Token ${AuthAPI.getToken()}` }
        });
    },

    async trackClick(id) {
        await fetch(`${API_BASE}/recommendations/${id}/click/`, {
            method: 'POST',
            headers: { 'Authorization': `Token ${AuthAPI.getToken()}` }
        });
    }
};

// ==================== 8) SMART NOTIFICATIONS ====================
const Notifications = {
    async getAll() {
        const response = await fetch(`${API_BASE}/notifications/`, {
            headers: { 'Authorization': `Token ${AuthAPI.getToken()}` }
        });
        return response.json();
    },

    async markAsRead(id) {
        const response = await fetch(`${API_BASE}/notifications/${id}/mark_read/`, {
            method: 'POST',
            headers: { 'Authorization': `Token ${AuthAPI.getToken()}` }
        });
        return response.json();
    },

    async createPriceAlert(data) {
        const response = await fetch(`${API_BASE}/notifications/create_price_alert/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${AuthAPI.getToken()}`
            },
            body: JSON.stringify(data)
        });
        return response.json();
    },

    initPushNotifications() {
        if ('Notification' in window) {
            Notification.requestPermission();
        }
    },

    async subscribeToPush() {
        if (!('serviceWorker' in navigator)) return;
        // Service worker push notification setup
    }
};

// ==================== 9) WEATHER INTEGRATION ====================
const Weather = {
    async getWeather(city, destinationId = null) {
        const url = destinationId 
            ? `${API_BASE}/weather/?destination_id=${destinationId}`
            : `${API_BASE}/weather/?city=${encodeURIComponent(city)}`;
        const response = await fetch(url);
        return response.json();
    },

    async getForecast(city, days = 7) {
        const response = await fetch(`${API_BASE}/weather/forecast/?city=${city}&days=${days}`);
        return response.json();
    },

    getWeatherIcon(condition) {
        const icons = {
            'sunny': '☀️',
            'cloudy': '☁️',
            'partly_cloudy': '⛅',
            'rain': '🌧️',
            'storm': '⛈️',
            'snow': '❄️',
            'fog': '🌫️'
        };
        return icons[condition.toLowerCase()] || '🌤️';
    },

    getBestTimeToVisit(region) {
        const recommendations = {
            'goa': 'November to February',
            'rajasthan': 'October to March',
            'kerala': 'September to March',
            'himachal': 'March to June, October to November',
            'default': 'October to March'
        };
        const key = region.toLowerCase();
        return recommendations[key] || recommendations['default'];
    }
};

// ==================== 10) SAFETY & EMERGENCY ====================
const Safety = {
    async getInfo(destinationId) {
        const response = await fetch(`${API_BASE}/safety/?destination_id=${destinationId}`);
        return response.json();
    },

    getIndiaEmergencyNumbers() {
        return {
            police: '100',
            ambulance: '102',
            fire: '101',
            women_helpline: '1091',
            child_helpline: '1098',
            general_emergency: '112',
            tourist_police: '1363'
        };
    },

    getSafetyTips() {
        return [
            'Keep copies of important documents',
            'Share itinerary with family',
            'Use authorized taxis and transportation',
            'Keep valuables in hotel safe',
            'Stay aware of surroundings',
            'Avoid isolated areas at night',
            'Keep emergency contacts saved',
            'Register with embassy for international travel'
        ];
    }
};

// ==================== 11) QR BASED TICKETS ====================
const QRTickets = {
    async create(data) {
        const response = await fetch(`${API_BASE}/qr-tickets/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${AuthAPI.getToken()}`
            },
            body: JSON.stringify(data)
        });
        return response.json();
    },

    async getMyTickets() {
        const response = await fetch(`${API_BASE}/qr-tickets/`, {
            headers: { 'Authorization': `Token ${AuthAPI.getToken()}` }
        });
        return response.json();
    },

    async verify(ticketId) {
        const response = await fetch(`${API_BASE}/qr-tickets/${ticketId}/verify/`, {
            headers: { 'Authorization': `Token ${AuthAPI.getToken()}` }
        });
        return response.json();
    },

    generateQRCode(data) {
        // Using QRCode.js or similar library
        if (typeof QRCode !== 'undefined') {
            return new QRCode(document.createElement('div'), {
                text: data,
                width: 200,
                height: 200
            });
        }
        return null;
    }
};

// =================