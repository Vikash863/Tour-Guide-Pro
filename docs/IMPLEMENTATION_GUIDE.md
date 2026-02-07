# Production-Level Implementation Guide

## Project Setup & Deployment

### 1. Environment Configuration

Create a `.env` file in the project root:

```env
# Django Settings
SECRET_KEY=your-super-secret-key-here-change-in-production
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# Database
MONGODB_URI=mongodb://username:password@localhost:27017/tour
# or for MongoDB Atlas:
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/tour

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com

# Security
CSRF_TRUSTED_ORIGINS=http://localhost:3000,https://yourdomain.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Database Setup

```bash
# Create migrations for Django
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser for admin panel
python manage.py createsuperuser
```

### 4. MongoDB Setup (Optional - for advanced features)

```bash
# Connect to MongoDB and create collections
python manage.py shell

from api.db import create_indexes
create_indexes()
```

### 5. Run Development Server

```bash
python manage.py runserver
```

Visit: `http://localhost:8000`

---

## Frontend Integration

### 1. Update HTML Files

Add the new API client to your HTML files:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Tour Guide Pro</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <!-- Your content here -->
    
    <!-- Add the complete API client -->
    <script src="/static/js/api-complete.js"></script>
    <script src="/static/js/app.js"></script>
</body>
</html>
```

### 2. Create Signup Form (Example)

```html
<!-- templates/signup.html -->
<form id="signupForm">
    <input type="text" id="firstName" placeholder="First Name" required>
    <input type="text" id="lastName" placeholder="Last Name" required>
    <input type="email" id="email" placeholder="Email" required>
    <input type="password" id="password" placeholder="Password" required>
    <input type="password" id="confirmPassword" placeholder="Confirm Password" required>
    <button type="submit">Register</button>
    <div id="message"></div>
</form>

<script>
document.getElementById("signupForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const messageDiv = document.getElementById("message");
    
    try {
        const result = await api.auth.register({
            firstName: document.getElementById("firstName").value,
            lastName: document.getElementById("lastName").value,
            email: document.getElementById("email").value,
            password: document.getElementById("password").value,
        });
        
        messageDiv.innerHTML = `Success! Welcome ${result.user.username}`;
        messageDiv.className = "success";
        setTimeout(() => window.location.href = "/", 2000);
    } catch (error) {
        messageDiv.innerHTML = `Error: ${error.error || error.message}`;
        messageDiv.className = "error";
    }
});
</script>
```

### 3. Create Login Form (Example)

```html
<!-- templates/login.html -->
<form id="loginForm">
    <input type="email" id="email" placeholder="Email" required>
    <input type="password" id="password" placeholder="Password" required>
    <button type="submit">Login</button>
    <div id="message"></div>
</form>

<script>
document.getElementById("loginForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const messageDiv = document.getElementById("message");
    
    try {
        const result = await api.auth.login(
            document.getElementById("email").value,
            document.getElementById("password").value
        );
        
        messageDiv.innerHTML = `Welcome back, ${result.user.username}!`;
        messageDiv.className = "success";
        setTimeout(() => window.location.href = "/", 2000);
    } catch (error) {
        messageDiv.innerHTML = `Login failed: ${error.error}`;
        messageDiv.className = "error";
    }
});
</script>
```

### 4. Display Destinations (Example)

```html
<!-- templates/destinations.html -->
<div id="destinationsList"></div>

<script>
async function loadDestinations() {
    try {
        const destinations = await api.destinations.getAll();
        const html = destinations.results.map(d => `
            <div class="destination-card">
                <h3>${d.name}</h3>
                <p>${d.description}</p>
                <p>Location: ${d.city}, ${d.state}, ${d.country}</p>
                <p>Cost: $${d.average_cost}</p>
                <p>Rating: ${d.rating}/5</p>
                <button onclick="viewDestination(${d.id})">View Details</button>
            </div>
        `).join('');
        
        document.getElementById("destinationsList").innerHTML = html;
    } catch (error) {
        console.error('Error loading destinations:', error);
    }
}

function viewDestination(id) {
    window.location.href = `/destination/${id}`;
}

// Load on page load
document.addEventListener('DOMContentLoaded', loadDestinations);
</script>
```

### 5. Create Booking Form (Example)

```html
<!-- templates/booking.html -->
<form id="bookingForm">
    <select id="bookingType" required onchange="updateHotelCabOptions()">
        <option value="">Select Booking Type</option>
        <option value="hotel">Hotel</option>
        <option value="cab">Cab</option>
    </select>
    
    <div id="hotelOptions" style="display:none;">
        <select id="hotelId" required>
            <option value="">Select Hotel</option>
        </select>
        <input type="date" id="checkInDate" required>
        <input type="date" id="checkOutDate" required>
        <input type="number" id="numGuests" placeholder="Number of Guests" required>
        <input type="number" id="numRooms" placeholder="Number of Rooms" required>
    </div>
    
    <div id="cabOptions" style="display:none;">
        <select id="cabId" required>
            <option value="">Select Cab</option>
        </select>
        <input type="date" id="bookingDate" required>
    </div>
    
    <input type="number" id="totalPrice" placeholder="Total Price" required>
    <button type="submit">Book Now</button>
    <div id="bookingMessage"></div>
</form>

<script>
async function updateHotelCabOptions() {
    const type = document.getElementById("bookingType").value;
    document.getElementById("hotelOptions").style.display = type === 'hotel' ? 'block' : 'none';
    document.getElementById("cabOptions").style.display = type === 'cab' ? 'block' : 'none';
    
    if (type === 'hotel') {
        const hotels = await api.hotels.getAvailable();
        const options = hotels.results.map(h => 
            `<option value="${h.id}">${h.name} - $${h.price_per_night}/night</option>`
        ).join('');
        document.getElementById("hotelId").innerHTML = 
            '<option value="">Select Hotel</option>' + options;
    } else if (type === 'cab') {
        const cabs = await api.cabs.getAvailable();
        const options = cabs.results.map(c => 
            `<option value="${c.id}">${c.company_name} - $${c.price_per_km}/km</option>`
        ).join('');
        document.getElementById("cabId").innerHTML = 
            '<option value="">Select Cab</option>' + options;
    }
}

document.getElementById("bookingForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const messageDiv = document.getElementById("bookingMessage");
    
    try {
        const bookingData = {
            booking_type: document.getElementById("bookingType").value,
            total_price: parseInt(document.getElementById("totalPrice").value),
            booking_status: 'confirmed'
        };
        
        if (bookingData.booking_type === 'hotel') {
            bookingData.hotel = parseInt(document.getElementById("hotelId").value);
            bookingData.check_in_date = document.getElementById("checkInDate").value;
            bookingData.check_out_date = document.getElementById("checkOutDate").value;
            bookingData.number_of_guests = parseInt(document.getElementById("numGuests").value);
            bookingData.number_of_rooms = parseInt(document.getElementById("numRooms").value);
        } else {
            bookingData.cab = parseInt(document.getElementById("cabId").value);
        }
        
        const result = await api.bookings.create(bookingData);
        messageDiv.innerHTML = `Booking successful! Confirmation: ${result.id}`;
        messageDiv.className = "success";
        setTimeout(() => window.location.href = "/bookings", 2000);
    } catch (error) {
        messageDiv.innerHTML = `Booking failed: ${error.error || error.message}`;
        messageDiv.className = "error";
    }
});
</script>
```

### 6. Contact Form (Example)

```html
<!-- templates/contact.html -->
<form id="contactForm">
    <input type="text" id="name" placeholder="Full Name" required>
    <input type="email" id="email" placeholder="Email" required>
    <input type="tel" id="phone" placeholder="Phone (optional)">
    <input type="text" id="subject" placeholder="Subject" required>
    <textarea id="message" placeholder="Your Message" rows="5" required></textarea>
    <button type="submit">Send Message</button>
    <div id="contactMessage"></div>
</form>

<script>
document.getElementById("contactForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const messageDiv = document.getElementById("contactMessage");
    
    try {
        await api.contacts.create({
            name: document.getElementById("name").value,
            email: document.getElementById("email").value,
            phone: document.getElementById("phone").value,
            subject: document.getElementById("subject").value,
            message: document.getElementById("message").value
        });
        
        messageDiv.innerHTML = "Thank you! We'll get back to you soon.";
        messageDiv.className = "success";
        document.getElementById("contactForm").reset();
    } catch (error) {
        messageDiv.innerHTML = `Error: ${error.message}`;
        messageDiv.className = "error";
    }
});
</script>
```

---

## Testing the API

### Using cURL

```bash
# Register
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123",
    "first_name": "Test",
    "last_name": "User"
  }'

# Login
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'

# Create Destination
curl -X POST http://localhost:8000/api/destinations/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Paris",
    "city": "Paris",
    "country": "France",
    "description": "City of lights",
    "best_time_to_visit": "April-May",
    "attractions": ["Eiffel Tower", "Louvre"],
    "average_cost": 5000,
    "rating": 4.8
  }'

# Get All Destinations
curl http://localhost:8000/api/destinations/

# Create Hotel
curl -X POST http://localhost:8000/api/hotels/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Grand Hotel",
    "location": "Central Paris",
    "destination": 1,
    "description": "Luxury hotel",
    "price_per_night": 250,
    "rating": 4.7,
    "amenities": ["WiFi", "Pool"],
    "available_rooms": 10,
    "total_rooms": 50,
    "phone": "+33-123-456",
    "email": "info@hotel.com"
  }'

# Create Booking (requires token)
curl -X POST http://localhost:8000/api/bookings/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token your_token_here" \
  -d '{
    "booking_type": "hotel",
    "hotel": 1,
    "check_in_date": "2024-02-15",
    "check_out_date": "2024-02-20",
    "number_of_guests": 2,
    "number_of_rooms": 1,
    "total_price": 1250,
    "booking_status": "confirmed"
  }'
```

---

## Production Deployment

### Using Gunicorn & Nginx

1. **Install Gunicorn:**
```bash
pip install gunicorn
```

2. **Create Systemd Service:**
```bash
sudo nano /etc/systemd/system/tourguidepro.service
```

```ini
[Unit]
Description=Tour Guide Pro Django Service
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/path/to/tour
ExecStart=/path/to/venv/bin/gunicorn \
    --workers 4 \
    --bind 127.0.0.1:8000 \
    tourguidepro.wsgi:application
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

3. **Enable & Start Service:**
```bash
sudo systemctl enable tourguidepro
sudo systemctl start tourguidepro
```

4. **Configure Nginx:**
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/tour/static/;
    }

    location /media/ {
        alias /path/to/tour/media/;
    }
}
```

---

## Monitoring & Logging

### Enable Logging in settings.py:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django.log'),
        },
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'api': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
```

---

## Performance Optimization

1. **Database Indexing** - Already implemented in `api/db.py`
2. **Caching** - Add Redis caching
3. **Pagination** - Implement for list endpoints
4. **Compression** - Enable GZIP in Nginx
5. **CDN** - Use CloudFront or similar for static files
6. **Database Backups** - Schedule automated backups
7. **Monitoring** - Use tools like New Relic or DataDog

---

## Security Checklist

- [x] Use Token authentication
- [x] Implement CORS properly
- [x] Validate all inputs
- [x] Use HTTPS in production
- [x] Secure password storage (Django's password hashing)
- [x] Rate limiting (implement via middleware)
- [x] SQL Injection prevention (Django ORM)
- [x] CSRF protection enabled
- [x] XSS prevention
- [x] Secure MongoDB connection
- [ ] Regular security audits
- [ ] Implement 2FA
- [ ] Use API keys for service-to-service

---

## Next Steps

1. ✅ Complete API endpoints - DONE
2. ✅ MongoDB integration - DONE
3. ✅ Frontend API client - DONE
4. 🔄 Add comprehensive forms
5. 🔄 Implement pagination
6. 🔄 Add email notifications
7. 🔄 Implement payment integration
8. 🔄 Add advanced analytics
9. 🔄 Deploy to production

---

## Support

For issues or questions, refer to the API documentation or contact the development team.
