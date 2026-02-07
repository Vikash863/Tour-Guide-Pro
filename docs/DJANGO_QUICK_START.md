# 🚀 TourGuidePro Django - Quick Start Guide

## ✅ What's Included

Your TourGuidePro application is now fully built with:
- ✅ **Django REST Framework** backend
- ✅ **SQLite database** (can switch to PostgreSQL)
- ✅ **Complete API** (31+ endpoints)
- ✅ **User authentication** system
- ✅ **Sample data** seeding script

---

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

---

## 🎯 Installation (5 Minutes)

### Step 1: Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Database
The project uses SQLite by default (no configuration needed).

### Step 4: Run Migrations
```bash
python manage.py migrate
```

### Step 5: Create Superuser (Admin)
```bash
python manage.py createsuperuser
# Enter username, email, and password
```

### Step 6: Seed Sample Data
```bash
python manage.py seed
```
This adds:
- 6 Destinations
- 5 Hotels  
- 4 Cab Services

### Step 7: Start Development Server
```bash
python manage.py runserver
```

Your app will run at: `http://localhost:8000`

---

## 🌐 Accessing Your Application

- **Frontend**: `http://localhost:8000` (Home page)
- **API**: `http://localhost:8000/api/`
- **Admin Panel**: `http://localhost:8000/admin/`
  - Login with the superuser credentials you created

---

## 📁 Project Structure

```
Tour/
├── tourguidepro/              # Project configuration
│   ├── settings.py            # Django settings
│   ├── urls.py                # URL routing
│   ├── wsgi.py                # WSGI config
│   └── asgi.py                # ASGI config
│
├── api/                        # REST API app
│   ├── models.py              # Database models (6)
│   ├── serializers.py         # DRF serializers
│   ├── views.py               # ViewSets and views
│   ├── urls.py                # API URL routing
│   ├── admin.py               # Admin configuration
│   └── management/
│       └── commands/
│           └── seed.py        # Data seeding script
│
├── manage.py                  # Django management
├── requirements.txt           # Python dependencies
├── .env                       # Environment config
│
├── Home.html/js/css          # Home page
├── login.html/js/css         # Login page
├── signup.html/js/css        # Registration
├── destination.html/js/css   # Destinations
├── hotel.html/js/css         # Hotels
├── cab.html/js/css           # Cabs
├── iterenary.html/js/css     # Itinerary
├── contact.html/js/css       # Contact
│
└── api.js                     # Frontend API client
```

---

## 🔌 API Endpoints

All endpoints are at: `http://localhost:8000/api/`

### Users (4 endpoints)
```
POST   /users/register/   - Register user
GET    /users/            - Get all users
GET    /users/me/         - Get current user
GET    /users/:id/        - Get user by ID
```

### Destinations (CRUD)
```
GET    /destinations/             - Get all
POST   /destinations/             - Create
GET    /destinations/:id/         - Get by ID
PUT    /destinations/:id/         - Update
DELETE /destinations/:id/         - Delete
GET    /destinations/search/      - Search by name
```

### Hotels (CRUD)
```
GET    /hotels/            - Get all
POST   /hotels/            - Create
GET    /hotels/:id/        - Get by ID
PUT    /hotels/:id/        - Update
DELETE /hotels/:id/        - Delete
GET    /hotels/search/     - Search by location
```

### Cabs (CRUD)
```
GET    /cabs/        - Get all
POST   /cabs/        - Create
GET    /cabs/:id/    - Get by ID
PUT    /cabs/:id/    - Update
DELETE /cabs/:id/    - Delete
GET    /cabs/filter/ - Filter cabs
```

### Bookings (CRUD - Auth Required)
```
GET    /bookings/         - Get user bookings
POST   /bookings/         - Create booking
GET    /bookings/:id/     - Get by ID
PUT    /bookings/:id/     - Update
DELETE /bookings/:id/     - Delete
POST   /bookings/:id/cancel/ - Cancel booking
```

### Contacts (CRUD)
```
GET    /contacts/           - Get all
POST   /contacts/           - Create
GET    /contacts/:id/       - Get by ID
PUT    /contacts/:id/       - Update
DELETE /contacts/:id/       - Delete
POST   /contacts/:id/mark_as_read/ - Mark as read
```

---

## 🧪 Testing API with cURL

### Get All Destinations
```bash
curl http://localhost:8000/api/destinations/
```

### Search Hotels
```bash
curl "http://localhost:8000/api/hotels/search/?location=Agra"
```

### Get All Cabs
```bash
curl http://localhost:8000/api/cabs/
```

### Filter Cabs
```bash
curl "http://localhost:8000/api/cabs/filter/?vehicleType=economy&minPrice=5&maxPrice=20"
```

### Submit Contact Form
```bash
curl -X POST http://localhost:8000/api/contacts/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+919876543210",
    "subject": "Test",
    "message": "Hello"
  }'
```

---

## 📊 Database Models

### Destination
```python
- name (unique)
- description
- city, state, country
- best_time_to_visit
- attractions (list)
- average_cost
- rating (0-5)
```

### Hotel
```python
- name
- location
- destination (FK)
- description
- price_per_night
- amenities (list)
- available_rooms
- total_rooms
- rating
- contact (phone, email)
```

### Cab
```python
- company_name
- vehicle_type (economy/premium/luxury/van)
- price_per_km
- price_per_hour
- capacity
- available_cars
- rating
- contact (phone, email)
```

### Booking
```python
- user (FK)
- booking_type (hotel/cab/destination)
- hotel/cab/destination (FK)
- check_in_date
- check_out_date
- number_of_guests
- total_price
- payment_status
- booking_status
```

### Contact
```python
- name
- email
- phone
- subject
- message
- status (new/read/resolved)
```

---

## 🔐 Authentication

Django uses token-based authentication by default. To implement JWT:

### Install drf-simplejwt
```bash
pip install djangorestframework-simplejwt
```

### Update settings.py
```python
INSTALLED_APPS = [
    ...
    'rest_framework_simplejwt',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}
```

### Update urls.py
```python
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

---

## 🛠️ Common Commands

```bash
# Run development server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Seed database
python manage.py seed

# Access admin panel
python manage.py runserver
# Then visit http://localhost:8000/admin/

# Create new app
python manage.py startapp appname

# Clear database
python manage.py flush

# Run shell
python manage.py shell
```

---

## 📝 Useful Features

### Admin Panel
- Full CRUD for all models
- Search and filter
- Custom list displays
- Bulk actions

### API Documentation
- Auto-generated browsable API
- Detailed error messages
- Pagination support

### Data Validation
- Required fields
- Email validation
- Rating constraints (0-5)
- Phone number validation

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| `No migrations detected` | Run `python manage.py makemigrations api` |
| `Port 8000 in use` | Use `python manage.py runserver 8001` |
| `Database locked` | Delete `db.sqlite3` and run migrations again |
| `Permission denied` | Activate virtual environment first |

---

## 🚀 Next Steps

1. **Test the API** with cURL or Postman
2. **Visit admin panel** to view/edit data
3. **Use the frontend** at http://localhost:8000
4. **Add authentication** (JWT recommended)
5. **Deploy** to production

---

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Python Best Practices](https://pep8.org/)

---

**Happy coding with Django! 🎉**
