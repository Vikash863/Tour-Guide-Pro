// ==================== GPS MAP TRACKING ====================
const GPSTracking = {
    watchId: null,
    trackData: [],
    
    async startTracking(tripName) {
        if (!navigator.geolocation) {
            alert('Geolocation is not supported by your browser');
            return null;
        }
        
        return new Promise((resolve, reject) => {
            this.watchId = navigator.geolocation.watchPosition(
                async (position) => {
                    const location = {
                        latitude: position.coords.latitude,
                        longitude: position.coords.longitude,
                        accuracy: position.coords.accuracy,
                        altitude: position.coords.altitude,
                        timestamp: new Date().toISOString()
                    };
                    
                    this.trackData.push(location);
                    await this.saveLocation(location);
                    resolve(location);
                },
                (error) => { reject(error); },
                { enableHighAccuracy: true, maximumAge: 30000, timeout: 27000 }
            );
        });
    },
    
    stopTracking() {
        if (this.watchId) {
            navigator.geolocation.clearWatch(this.watchId);
            this.watchId = null;
        }
    },
    
    async saveLocation(location) {
        try {
            const response = await fetch('/api/gps/track/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(location)
            });
            return response.json();
        } catch (error) {
            console.error('Error saving location:', error);
        }
    },
    
    async startTrip(name, startLat, startLng) {
        try {
            return await fetch('/api/trips/start/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: name, start_latitude: startLat, start_longitude: startLng })
            }).then(r => r.json());
        } catch (error) {
            console.error('Error starting trip:', error);
            throw error;
        }
    },
    
    async stopTrip(tripId, endLat, endLng) {
        try {
            return await fetch(`/api/trips/${tripId}/stop/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ end_latitude: endLat, end_longitude: endLng })
            }).then(r => r.json());
        } catch (error) {
            console.error('Error stopping trip:', error);
            throw error;
        }
    }
};

// ==================== WEATHER API ====================
const WeatherAPI = {
    async getWeather(city) {
        try {
            return await fetch(`/api/weather/?city=${encodeURIComponent(city)}`).then(r => r.json());
        } catch (error) {
            console.error('Error fetching weather:', error);
            throw error;
        }
    },
    
    async getForecast(city, days = 7) {
        try {
            return await fetch(`/api/weather/forecast/?city=${encodeURIComponent(city)}&days=${days}`).then(r => r.json());
        } catch (error) {
            console.error('Error fetching forecast:', error);
            throw error;
        }
    },
    
    getWeatherIcon(condition) {
        const icons = { 'Sunny': '☀️', 'Clear': '🌙', 'Partly Cloudy': '⛅', 'Cloudy': '☁️', 'Rainy': '🌧️', 'Light Rain': '🌦️' };
        return icons[condition] || '🌤️';
    }
};

// ==================== EXPENSE TRACKER ====================
const ExpenseTracker = {
    async loadCategories() {
        try {
            return await fetch('/api/expense-categories/default/').then(r => r.json());
        } catch (error) {
            return [];
        }
    },
    
    async addExpense(data) {
        try {
            return await fetch('/api/expenses/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            }).then(r => r.json());
        } catch (error) {
            console.error('Error adding expense:', error);
            throw error;
        }
    },
    
    async getExpenses(tripId = null) {
        try {
            const url = tripId ? `/api/expenses/by_trip/?trip_id=${tripId}` : '/api/expenses/';
            return await fetch(url).then(r => r.json());
        } catch (error) {
            return [];
        }
    },
    
    async getExpenseSummary(tripId = null) {
        try {
            const url = tripId ? `/api/expenses/summary/?trip_id=${tripId}` : '/api/expenses/summary/';
            return await fetch(url).then(r => r.json());
        } catch (error) {
            return { categories: [], total: 0 };
        }
    },
    
    formatCurrency(amount, currency = 'INR') {
        return new Intl.NumberFormat('en-IN', { style: 'currency', currency: currency }).format(amount);
    }
};

// ==================== TRAVEL CHECKLIST ====================
const TravelChecklist = {
    async getTemplates() {
        try {
            return await fetch('/api/checklists/templates/').then(r => r.json());
        } catch (error) {
            return [];
        }
    },
    
    async createFromTemplate(templateId, name, destination, startDate, endDate) {
        try {
            return await fetch('/api/checklists/from_template/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ template_id: templateId, name, destination, start_date: startDate, end_date: endDate })
            }).then(r => r.json());
        } catch (error) {
            console.error('Error creating checklist:', error);
            throw error;
        }
    },
    
    async getChecklists() {
        try {
            return await fetch('/api/checklists/').then(r => r.json());
        } catch (error) {
            return [];
        }
    },
    
    async toggleItem(checklistId, itemId) {
        try {
            return await fetch(`/api/checklists/${checklistId}/toggle_item/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ item_id: itemId })
            }).then(r => r.json());
        } catch (error) {
            console.error('Error toggling item:', error);
            throw error;
        }
    },
    
    getDefaultTemplates() {
        return [
            { id: 1, name: 'Beach Vacation', items: [
                { name: 'Swimsuit', category: 'clothing' }, { name: 'Sunscreen SPF 50+', category: 'toiletries' },
                { name: 'Sunglasses', category: 'accessories' }, { name: 'Beach towel', category: 'accessories' },
                { name: 'Flip flops', category: 'footwear' }, { name: 'Passport', category: 'documents' }
            ]},
            { id: 2, name: 'Mountain Trek', items: [
                { name: 'Hiking boots', category: 'footwear' }, { name: 'Warm jacket', category: 'clothing' },
                { name: 'Trekking poles', category: 'equipment' }, { name: 'Water bottle', category: 'equipment' },
                { name: 'First aid kit', category: 'health' }, { name: 'Flashlight', category: 'equipment' }
            ]},
            { id: 3, name: 'Business Trip', items: [
                { name: 'Laptop', category: 'electronics' }, { name: 'Business suits', category: 'clothing' },
                { name: 'Business cards', category: 'documents' }, { name: 'Charger', category: 'electronics' }
            ]}
        ];
    }
};

// ==================== REFERRAL SYSTEM ====================
const ReferralSystem = {
    async generateCode(discountPercent = 10, maxUses = 10) {
        try {
            return await fetch('/api/referral-codes/generate/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ discount_percent: discountPercent, max_uses: maxUses })
            }).then(r => r.json());
        } catch (error) {
            console.error('Error generating referral code:', error);
            throw error;
        }
    },
    
    async getMyCode() {
        try {
            return await fetch('/api/referral-codes/my_code/').then(r => r.json());
        } catch (error) {
            return null;
        }
    },
    
    async getStats() {
        try {
            return await fetch('/api/referral-codes/stats/').then(r => r.json());
        } catch (error) {
            return null;
        }
    },
    
    async applyCode(code, email) {
        try {
            return await fetch('/api/referrals/apply/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ code: code, email: email })
            }).then(r => r.json());
        } catch (error) {
            console.error('Error applying referral code:', error);
            throw error;
        }
    },
    
    shareViaWhatsApp(code) {
        const message = `Join TourGuidePro! Use my referral code: ${code}`;
        window.open(`https://wa.me/?text=${encodeURIComponent(message)}`, '_blank');
    },
    
    shareViaEmail(code) {
        const subject = 'Join TourGuidePro - Get Exclusive Discounts!';
        const body = `Use my referral code "${code}" when signing up for TourGuidePro!`;
        window.location.href = `mailto:?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    },
    
    copyReferralCode(code) {
        navigator.clipboard.writeText(code).then(() => {
            alert('Referral code copied!');
        }).catch(() => {
            prompt('Copy this code:', code);
        });
    }
};

// Export all modules
window.GPSTracking = GPSTracking;
window.WeatherAPI = WeatherAPI;
window.ExpenseTracker = ExpenseTracker;
window.TravelChecklist = TravelChecklist;
window.ReferralSystem = ReferralSystem;
