# 🌍 TourGuidePro - Django Version

> A full-stack travel booking platform built with Django REST Framework, SQLite database, and vanilla JavaScript frontend.

![Version](https://img.shields.io/badge/version-2.0.0--django-blue)
![Status](https://img.shields.io/badge/status-Fully%20Functional-brightgreen)
![Framework](https://img.shields.io/badge/framework-Django-green)

---

## 🎯 Overview

TourGuidePro is a comprehensive travel planning application built with **Django** as the backend framework. This is the fully functional Django version with:

- ✅ Django REST Framework APIs
- ✅ SQLite/PostgreSQL database support
- ✅ Complete CRUD operations
- ✅ User authentication
- ✅ Admin panel
- ✅ Sample data seeding

---

## ✨ Features

### Core Features
- 🔐 User registration and authentication
- 🌏 Browse and search destinations
- 🏨 Hotel booking system
- 🚕 Cab reservation services
- 📅 Create travel itineraries
- 💬 Contact support team
- 📊 Admin dashboard

### Technical Features
- RESTful API with 30+ endpoints
- Role-based access control
- Data validation and error handling
- CORS enabled for frontend
- Database relationships and constraints
- Admin interface for management

---

## 🛠️ Tech Stack

### Backend
- **Django 4.2** - Web framework
- **Django REST Framework** - REST API toolkit
- **SQLite** - Default database (PostgreSQL ready)
- **Python 3.8+** - Programming language
- **CORS Headers** - Cross-origin requests

### Frontend
- **HTML5/CSS3** - Markup & styling
- **Vanilla JavaScript** - Interactivity
- **Bootstrap 5** - UI framework
- **Fetch API** - HTTP requests

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Step-by-Step Setup

**1. Activate Virtual Environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**2. Install Dependencies**
```bash
pip install -r requirements.txt
```

**3. Run Migrations**
```bash
python manage.py migrate
```

**4. Create Admin User**
```bash
python manage.py createsuperuser
# Follow the prompts to create admin account
```

**5. Seed Database**
```bash
python manage.py seed
# Adds sample destinations, hotels, and cabs
```

**6. Start Server**
```bash
python manage.py runserver
```

Visit: `http://localhost:8000`

---

## 🚀 Quick Start

### Access Points

| URL | Purpose |
|-----|---------|
| `http://localhost:8000` | Frontend application |
| `http://localhost:8000/api/` | API endpoints |
| `http://localhost:8000/admin/` | Admin panel |

### Test API
```bash
# Get all destinations
curl http://localhost:8000/api/destinations/

# Search hotels
curl "http://localhost:8000/api/hotels/search/?location=Agra"

# Submit contact
curl -X POST http://localhost:8000/api/contacts/ \
  -H "Content-Type: application/json" \
  -d '{"name":"John","email":"john@example.com","subject":"Help","message":"Test"}'
```

---

## 📁 Directory Structure

```
Tour/
├── tourguidepro/           # Project settings
│   ├── settings.py         # Django configuration
│   ├── urls.py             # URL routing
│   ├── wsgi.py             # WSGI
│   └── asgi.py             # ASGI
│
├── api/                    # REST API app
│   ├── models.py           # Database models (6)
│   ├── serializers.py      # DRF serializers
│   ├── views.py            # ViewSets
│   ├── urls.py             # API URLs
│   ├── admin.py            # Admin config
│   └── management/commands/seed.py
│
├── manage.py               # Django CLI
├── requirements.txt        # Dependencies
├── .env                    # Config
│
├── Home.html/js/css       # Frontend files
├── login.html/js/css
├── api.js                  # API client
└── ... (other pages)
```

---

## 🔌 API Endpoints (30+)

### Users
```
POST   /users/register/     - Register
GET    /users/              - List all
GET    /users/:id/          - Get user
GET    /users/me/           - Current user
```

### Destinations (Full CRUD)
```
GET    /destinations/
POST   /destinations/
GET    /destinations/:id/
PUT    /destinations/:id/
DELETE /destinations/:id/
GET    /destinations/search/?name=
```

### Hotels (Full CRUD)
```
GET    /hotels/
POST   /hotels/
GET    /hotels/:id/
PUT    /hotels/:id/
DELETE /hotels/:id/
GET    /hotels/search/?location=
```

### Cabs (Full CRUD)
```
GET    /cabs/
POST   /cabs/
GET    /cabs/:id/
PUT    /cabs/:id/
DELETE /cabs/:id/
GET    /cabs/filter/?vehicleType=
```

### Bookings
```
GET    /bookings/              - User bookings
POST   /bookings/              - Create
GET    /bookings/:id/          - Get
PUT    /bookings/:id/          - Update
DELETE /bookings/:id/          - Delete
POST   /bookings/:id/cancel/   - Cancel
```

### Contacts
```
GET    /contacts/
POST   /contacts/
GET    /contacts/:id/
PUT    /contacts/:id/
DELETE /contacts/:id/
POST   /contacts/:id/mark_as_read/
```

---

## 📊 Database Models

All models use Django's ORM:

### Destination
- name (unique)
- description, city, state, country
- attractions (JSON), best_time_to_visit
- average_cost, rating

### Hotel
- name, location, destination (FK)
- price_per_night, amenities
- available_rooms, total_rooms
- rating, contact info

### Cab
- company_name, vehicle_type
- price_per_km, price_per_hour
- capacity, available_cars
- rating, contact info

### Booking
- user (FK), booking_type
- hotel/cab/destination (FK)
- check_in/out dates, total_price
- payment_status, booking_status

### Contact
- name, email, phone
- subject, message
- status (new/read/resolved)

---

## 🔐 Authentication

Django provides built-in authentication. For production with tokens:

```bash
pip install djangorestframework-simplejwt
```

Then update settings.py with JWT configuration.

---

## 🧪 Testing

### Using cURL
```bash
# List destinations
curl http://localhost:8000/api/destinations/

# Search hotels
curl "http://localhost:8000/api/hotels/search/?location=Agra"

# Create contact
curl -X POST http://localhost:8000/api/contacts/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@example.com","subject":"Hello","message":"World"}'
```

### Using Admin Panel
1. Visit `http://localhost:8000/admin/`
2. Login with superuser credentials
3. Manage all entities
4. View contacts and bookings

---

## 🛠️ Useful Commands

```bash
# Development server
python manage.py runserver

# Create migrations
python manage.py makemigrations api

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Seed data
python manage.py seed

# Shell
python manage.py shell

# Flush database
python manage.py flush

# Collect static files
python manage.py collectstatic
```

---

## 🚀 Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn tourguidepro.wsgi:application --bind 0.0.0.0:8000
```

### Using Docker
```dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "tourguidepro.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### Production Checklist
- [ ] Set `DEBUG = False` in settings.py
- [ ] Generate new `SECRET_KEY`
- [ ] Set `ALLOWED_HOSTS` properly
- [ ] Use PostgreSQL instead of SQLite
- [ ] Setup HTTPS
- [ ] Configure email settings
- [ ] Setup logging
- [ ] Configure static files CDN

---

## 📚 Documentation

- [DJANGO_QUICK_START.md](DJANGO_QUICK_START.md) - 5-minute setup
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Detailed guide
- [API_TESTING_GUIDE.md](API_TESTING_GUIDE.md) - API testing
- [Django Docs](https://docs.djangoproject.com/)
- [DRF Docs](https://www.django-rest-framework.org/)

---

## 🎯 Key Differences from Express Version

| Feature | Express | Django |
|---------|---------|--------|
| Database | MongoDB | SQLite/PostgreSQL |
| ORM | Mongoose | Django ORM |
| Authentication | JWT | Session/Token |
| API Framework | Express | DRF |
| Admin Panel | None | Built-in |
| Migrations | Manual | Automated |
| Validation | Manual | Built-in |

---

## 🤝 Contributing

1. Fork repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

---

## 📄 License

MIT License - See LICENSE file

---

## 🎉 Status

✅ **Fully Functional and Production Ready**

---

<div align="center">

**Built with Django ⚡**

[Quick Start →](DJANGO_QUICK_START.md) | [API Testing →](API_TESTING_GUIDE.md)

</div>
