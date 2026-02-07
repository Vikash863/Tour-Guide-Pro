# Tour Guide Pro - Production-Level Full Stack Application

## 🌍 Project Overview

Tour Guide Pro is a comprehensive full-stack web application for managing tours, hotels, cabs, and bookings. It features a Django REST API backend with MongoDB integration and a responsive frontend with complete CRUD operations.

**Status**: Production-Ready ✅

---

## 🎯 Features

### Authentication & User Management
- ✅ User registration and login with token authentication
- ✅ Profile management and updates
- ✅ Secure password handling
- ✅ Logout functionality

### Destinations Management
- ✅ Complete CRUD operations (Create, Read, Update, Delete)
- ✅ Search destinations by name, city, country
- ✅ Filter by popularity/rating
- ✅ Display attractions and best time to visit

### Hotels Management
- ✅ Complete CRUD operations
- ✅ Search and filter by location
- ✅ Price range filtering
- ✅ Availability checking
- ✅ Amenities and room management

### Cabs/Transportation
- ✅ Complete CRUD operations
- ✅ Filter by vehicle type and price
- ✅ Filter by company
- ✅ Availability tracking
- ✅ Multiple vehicle types (Economy, Premium, Luxury, Van)

### Bookings Management
- ✅ Create bookings for hotels/cabs/destinations
- ✅ View user bookings
- ✅ Update booking details
- ✅ Cancel bookings
- ✅ Track booking status (pending, confirmed, cancelled, completed)
- ✅ Payment status tracking

### Contact Management
- ✅ Contact form submission
- ✅ Message status tracking (new, read, resolved)
- ✅ Admin message management

### Database
- ✅ Django ORM with SQLite (can switch to PostgreSQL)
- ✅ MongoDB for analytics and data backup
- ✅ Database indexes for performance
- ✅ Automatic data sync between databases

---

## 🛠️ Technology Stack

### Backend
- **Framework**: Django 4.2+ with Django REST Framework
- **Authentication**: Token-based authentication
- **Primary Database**: SQLite (Development) / PostgreSQL (Production)
- **NoSQL Database**: MongoDB
- **Task Queue**: Celery (optional for async tasks)
- **API Documentation**: DRF Spectacular (Swagger)

### Frontend
- **HTML5** / **CSS3** / **JavaScript (ES6+)**
- **Fetch API** for REST calls
- **Responsive Design** with mobile support
- **Local Storage** for client-side state management

### Deployment
- **Web Server**: Nginx
- **App Server**: Gunicorn
- **Process Manager**: Systemd

---

## 📦 Project Structure

```
Tour/
├── api/                          # Django REST API app
│   ├── views.py                 # API endpoints (enhanced with CRUD)
│   ├── models.py                # Django models
│   ├── serializers.py           # DRF serializers
│   ├── urls.py                  # API routing
│   ├── db.py                    # MongoDB connection & utilities
│   ├── migrations/              # Database migrations
│   └── management/commands/     # Custom management commands
│
├── static/                       # Static files
│   ├── css/                     # Stylesheets
│   │   ├── Home.css
│   │   ├── hotel.css
│   │   ├── cab.css
│   │   └── ...
│   ├── js/                      # JavaScript files
│   │   ├── api-complete.js     # ✨ NEW: Complete API client
│   │   ├── signup.js
│   │   ├── login.js
│   │   └── ...
│   └── images/                  # Image assets
│
├── templates/                    # HTML templates
│   ├── Home.html
│   ├── signup.html
│   ├── login.html
│   ├── hotel.html
│   └── ...
│
├── tourguidepro/                # Django settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── docs/                        # Documentation
│   ├── API_COMPLETE_DOCUMENTATION.md     # ✨ NEW
│   ├── IMPLEMENTATION_GUIDE.md             # ✨ NEW
│   └── ...
│
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies (updated)
└── .env                         # Environment variables
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MongoDB (local or cloud)
- pip/venv

### Installation

1. **Clone & Navigate**
```bash
cd Tour
```

2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup Environment Variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Run Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create Superuser**
```bash
python manage.py createsuperuser
```

7. **Start Development Server**
```bash
python manage.py runserver
```

8. **Access Application**
- Frontend: http://localhost:8000
- Admin Panel: http://localhost:8000/admin
- API: http://localhost:8000/api

---

## 📚 API Usage Examples

### Using JavaScript Fetch API

```javascript
// Import the API client
<script src="/static/js/api-complete.js"></script>

// Register new user
const registerResult = await api.auth.register({
    firstName: 'John',
    lastName: 'Doe',
    email: 'john@example.com',
    password: 'securepass123'
});

// Login
const loginResult = await api.auth.login('john@example.com', 'securepass123');
console.log(loginResult.token); // Save this token

// Get all destinations
const destinations = await api.destinations.getAll();

// Create a destination
await api.destinations.create({
    name: 'Paris',
    city: 'Paris',
    country: 'France',
    description: 'City of lights',
    best_time_to_visit: 'April-May',
    attractions: ['Eiffel Tower', 'Louvre'],
    average_cost: 5000,
    rating: 4.8
});

// Search
const results = await api.destinations.search('Paris');

// Create booking
const booking = await api.bookings.create({
    booking_type: 'hotel',
    hotel: 1,
    check_in_date: '2024-02-15',
    check_out_date: '2024-02-20',
    number_of_guests: 2,
    number_of_rooms: 1,
    total_price: 1250
});
```

### Using cURL

```bash
# Get all destinations
curl http://localhost:8000/api/destinations/

# Create destination
curl -X POST http://localhost:8000/api/destinations/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Paris","city":"Paris","country":"France"...}'

# Get bookings (requires token)
curl http://localhost:8000/api/bookings/ \
  -H "Authorization: Token your-token-here"
```

---

## 🔑 Key Endpoints

### Authentication
- `POST /api/users/register/` - Register user
- `POST /api/users/login/` - Login user
- `POST /api/users/logout/` - Logout user
- `GET /api/users/me/` - Get current user
- `PUT /api/users/{id}/update_profile/` - Update profile

### Destinations (Full CRUD)
- `GET /api/destinations/` - List all
- `POST /api/destinations/` - Create
- `GET /api/destinations/{id}/` - Read
- `PUT /api/destinations/{id}/` - Update
- `DELETE /api/destinations/{id}/` - Delete
- `GET /api/destinations/search/?q=query` - Search
- `GET /api/destinations/popular/` - Popular destinations
- `GET /api/destinations/by_country/?country=name` - Filter by country

### Hotels (Full CRUD)
- `GET /api/hotels/` - List all
- `POST /api/hotels/` - Create
- `GET /api/hotels/{id}/` - Read
- `PUT /api/hotels/{id}/` - Update
- `DELETE /api/hotels/{id}/` - Delete
- `GET /api/hotels/search/?q=query` - Search
- `GET /api/hotels/available/` - Available hotels
- `GET /api/hotels/by_price_range/?min_price=X&max_price=Y` - Filter by price

### Cabs (Full CRUD)
- `GET /api/cabs/` - List all
- `POST /api/cabs/` - Create
- `GET /api/cabs/{id}/` - Read
- `PUT /api/cabs/{id}/` - Update
- `DELETE /api/cabs/{id}/` - Delete
- `GET /api/cabs/filter/?vehicle_type=X&min_price=Y&max_price=Z` - Filter
- `GET /api/cabs/available/` - Available cabs

### Bookings (Full CRUD + Auth Required)
- `GET /api/bookings/` - List user's bookings
- `POST /api/bookings/` - Create booking
- `GET /api/bookings/{id}/` - Get booking
- `PUT /api/bookings/{id}/` - Update booking
- `DELETE /api/bookings/{id}/` - Delete booking
- `POST /api/bookings/{id}/cancel/` - Cancel booking
- `GET /api/bookings/pending/` - Get pending bookings
- `GET /api/bookings/confirmed/` - Get confirmed bookings

### Contacts
- `POST /api/contacts/` - Submit contact form
- `GET /api/contacts/` - List messages (admin)
- `DELETE /api/contacts/{id}/` - Delete message
- `POST /api/contacts/{id}/mark_as_read/` - Mark as read
- `POST /api/contacts/{id}/mark_as_resolved/` - Mark as resolved

---

## 🗄️ Database Schema

### Django Models
```python
User (Django's built-in)
Destination(id, name, city, country, rating, average_cost, ...)
Hotel(id, name, location, price_per_night, rating, available_rooms, ...)
Cab(id, company_name, vehicle_type, price_per_km, rating, ...)
Booking(id, user, booking_type, hotel/cab/destination, status, ...)
Contact(id, name, email, subject, message, status, ...)
```

### MongoDB Collections
```javascript
tours: {type, django_id, name, rating, price, ...}
users: {user_id, username, email, full_name, ...}
bookings: {user_id, booking_type, status, total_price, ...}
```

---

## 🔐 Security Features

- ✅ Token-based authentication
- ✅ CORS protection
- ✅ CSRF protection
- ✅ SQL injection prevention (Django ORM)
- ✅ XSS protection
- ✅ Secure password hashing (PBKDF2)
- ✅ HTTPS ready
- ✅ Input validation on all endpoints
- ✅ Rate limiting ready (add middleware)
- ✅ Secure MongoDB connection support

---

## 🧪 Testing

### Test API with Python
```python
python manage.py shell

# Test user creation
from api.models import *
from django.contrib.auth.models import User

user = User.objects.create_user(
    username='testuser',
    email='test@example.com',
    password='testpass123'
)

# Test destination creation
dest = Destination.objects.create(
    name='Tokyo',
    city='Tokyo',
    country='Japan',
    average_cost=4000,
    rating=4.7
)
```

### Test API with Postman
1. Import the API documentation
2. Use the token from login response
3. Test each endpoint with sample data

---

## 📈 Performance Optimization

- ✅ Database indexes on frequently queried fields
- ✅ Pagination support for list endpoints
- ✅ MongoDB for analytics (separate from transaction DB)
- ✅ Caching ready (Redis compatible)
- ✅ Lazy loading for images
- ✅ Compression enabled
- ✅ Static file optimization

---

## 🚢 Production Deployment

### Using Gunicorn + Nginx

```bash
# Install Gunicorn
pip install gunicorn

# Run Gunicorn
gunicorn --workers 4 --bind 0.0.0.0:8000 tourguidepro.wsgi:application

# Configure Nginx (see IMPLEMENTATION_GUIDE.md for details)
```

### Environment Variables for Production
```env
DEBUG=False
SECRET_KEY=your-very-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/tour
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

---

## 📖 Documentation

- **[API_COMPLETE_DOCUMENTATION.md](docs/API_COMPLETE_DOCUMENTATION.md)** - Full API endpoint documentation
- **[IMPLEMENTATION_GUIDE.md](docs/IMPLEMENTATION_GUIDE.md)** - Detailed implementation & deployment guide
- **API Swagger/OpenAPI** - Available at `/api/schema/` (when deployed)

---

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

---

## 📝 License

This project is proprietary and confidential.

---

## 🆘 Support & Troubleshooting

### Common Issues

**Database Connection Error**
```bash
# Check MongoDB connection
python manage.py shell
from api.db import db
print(db.command('ping'))
```

**Static Files Not Loading**
```bash
python manage.py collectstatic
```

**Migration Issues**
```bash
python manage.py migrate --fake-initial
python manage.py migrate
```

---

## ✅ Checklist for Production

- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Set strong SECRET_KEY
- [ ] Configure HTTPS/SSL
- [ ] Setup database backups
- [ ] Configure MongoDB security
- [ ] Enable CORS properly
- [ ] Setup logging
- [ ] Configure error tracking (Sentry)
- [ ] Setup monitoring
- [ ] Load test the application
- [ ] Setup CI/CD pipeline
- [ ] Document API with Swagger
- [ ] Setup email notifications
- [ ] Configure CDN for static files

---

## 🎉 What's New (v2.0)

✨ **Production-Level Enhancements**
- Complete CRUD operations for all resources
- MongoDB integration for analytics
- Enhanced API client with error handling
- Comprehensive documentation
- Security hardening
- Performance optimization
- Deployment ready

---

## 📞 Contact

For issues, feature requests, or support:
- Email: support@tourguide.com
- Issues: GitHub Issues
- Documentation: See `/docs` folder

---

**Happy Coding! 🚀**
