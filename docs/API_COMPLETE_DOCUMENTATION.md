# Production-Level Tour Guide API - Complete CRUD Documentation

## Overview
This is a production-ready Django REST Framework API with full MongoDB integration for managing tours, hotels, cabs, bookings, and user management.

## Technology Stack
- **Backend**: Django 3.2+, Django REST Framework
- **Database**: SQLite (Django ORM) + MongoDB (Analytics & Analytics)
- **Authentication**: Token-based authentication
- **Frontend**: HTML/CSS/JavaScript with Fetch API

## API Base URL
```
http://localhost:8000/api
```

---

## Authentication Endpoints

### 1. User Registration
**POST** `/users/register/`

**Request Body:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword123",
  "password_confirm": "securepassword123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response (201 Created):**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

### 2. User Login
**POST** `/users/login/`

**Request Body:**
```json
{
  "username": "john_doe",
  "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
  "message": "Login successful",
  "token": "abc123def456...",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  }
}
```

### 3. Get Current User
**GET** `/users/me/`

**Headers:**
```
Authorization: Token abc123def456...
```

**Response (200 OK):**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe"
}
```

### 4. Update User Profile
**PUT** `/users/{id}/update_profile/`

**Headers:**
```
Authorization: Token abc123def456...
```

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Smith",
  "email": "john.smith@example.com"
}
```

**Response (200 OK):**
```json
{
  "message": "Profile updated successfully",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john.smith@example.com",
    "first_name": "John",
    "last_name": "Smith"
  }
}
```

### 5. User Logout
**POST** `/users/logout/`

**Headers:**
```
Authorization: Token abc123def456...
```

**Response (200 OK):**
```json
{
  "message": "Logout successful"
}
```

---

## Destinations Endpoints (Full CRUD)

### 1. List All Destinations
**GET** `/destinations/`

**Query Parameters:**
- `page` - Page number (default: 1)
- `search` - Search by name, city, state, country
- `ordering` - Sort by: `-created_at`, `rating`, `average_cost`

**Response (200 OK):**
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Paris",
      "description": "City of lights",
      "city": "Paris",
      "state": "Île-de-France",
      "country": "France",
      "best_time_to_visit": "April-May, September-October",
      "attractions": ["Eiffel Tower", "Louvre Museum"],
      "average_cost": 5000,
      "rating": 4.8,
      "created_at": "2024-01-23T10:00:00Z"
    }
  ]
}
```

### 2. Create Destination
**POST** `/destinations/`

**Request Body:**
```json
{
  "name": "Paris",
  "description": "City of lights",
  "city": "Paris",
  "state": "Île-de-France",
  "country": "France",
  "best_time_to_visit": "April-May, September-October",
  "attractions": ["Eiffel Tower", "Louvre Museum"],
  "average_cost": 5000,
  "rating": 4.8
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "name": "Paris",
  "description": "City of lights",
  ...
}
```

### 3. Get Destination by ID
**GET** `/destinations/{id}/`

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "Paris",
  ...
}
```

### 4. Update Destination
**PUT** `/destinations/{id}/`

**Request Body:**
```json
{
  "name": "Paris (Updated)",
  "rating": 4.9
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "Paris (Updated)",
  "rating": 4.9,
  ...
}
```

### 5. Delete Destination
**DELETE** `/destinations/{id}/`

**Response (204 No Content)**

### 6. Search Destinations
**GET** `/destinations/search/?q=Paris`

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Paris",
    ...
  }
]
```

### 7. Get Popular Destinations
**GET** `/destinations/popular/`

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Paris",
    "rating": 4.8,
    ...
  }
]
```

### 8. Filter by Country
**GET** `/destinations/by_country/?country=France`

---

## Hotels Endpoints (Full CRUD)

### 1. List All Hotels
**GET** `/hotels/`

**Query Parameters:**
- `page` - Page number
- `search` - Search by name or location
- `ordering` - Sort by: `-created_at`, `price_per_night`, `rating`

**Response (200 OK):**
```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "name": "Luxury Hotel",
      "location": "Central Paris",
      "destination": 1,
      "description": "5-star luxury",
      "price_per_night": 250,
      "rating": 4.7,
      "amenities": ["WiFi", "Pool", "Gym"],
      "available_rooms": 10,
      "total_rooms": 50,
      "phone": "+33-1-234-567",
      "email": "info@hotel.com",
      "created_at": "2024-01-23T10:00:00Z"
    }
  ]
}
```

### 2. Create Hotel
**POST** `/hotels/`

**Request Body:**
```json
{
  "name": "Luxury Hotel",
  "location": "Central Paris",
  "destination": 1,
  "description": "5-star luxury hotel",
  "price_per_night": 250,
  "rating": 4.7,
  "amenities": ["WiFi", "Pool", "Gym"],
  "available_rooms": 10,
  "total_rooms": 50,
  "phone": "+33-1-234-567",
  "email": "info@hotel.com"
}
```

### 3. Get Hotel by ID
**GET** `/hotels/{id}/`

### 4. Update Hotel
**PUT** `/hotels/{id}/`

### 5. Delete Hotel
**DELETE** `/hotels/{id}/`

### 6. Search Hotels
**GET** `/hotels/search/?q=luxury`

### 7. Filter by Price Range
**GET** `/hotels/by_price_range/?min_price=100&max_price=500`

### 8. Get Available Hotels
**GET** `/hotels/available/`

---

## Cabs Endpoints (Full CRUD)

### 1. List All Cabs
**GET** `/cabs/`

**Response (200 OK):**
```json
{
  "count": 3,
  "results": [
    {
      "id": 1,
      "company_name": "Uber",
      "vehicle_type": "economy",
      "price_per_km": 15.50,
      "price_per_hour": 250,
      "capacity": 4,
      "rating": 4.6,
      "available_cars": 25,
      "description": "Affordable rides",
      "phone": "+33-1-800-UBER",
      "email": "support@uber.com",
      "created_at": "2024-01-23T10:00:00Z"
    }
  ]
}
```

### 2. Create Cab Service
**POST** `/cabs/`

**Request Body:**
```json
{
  "company_name": "Uber",
  "vehicle_type": "economy",
  "price_per_km": 15.50,
  "price_per_hour": 250,
  "capacity": 4,
  "rating": 4.6,
  "available_cars": 25,
  "description": "Affordable rides",
  "phone": "+33-1-800-UBER",
  "email": "support@uber.com"
}
```

### 3. Get Cab by ID
**GET** `/cabs/{id}/`

### 4. Update Cab
**PUT** `/cabs/{id}/`

### 5. Delete Cab
**DELETE** `/cabs/{id}/`

### 6. Filter Cabs
**GET** `/cabs/filter/?vehicle_type=economy&min_price=10&max_price=50`

**Query Parameters:**
- `vehicle_type` - economy, premium, luxury, van
- `min_price` - Minimum price per km
- `max_price` - Maximum price per km

### 7. Get Cabs by Company
**GET** `/cabs/by_company/?company=Uber`

### 8. Get Available Cabs
**GET** `/cabs/available/`

---

## Bookings Endpoints (Full CRUD) - Authentication Required

### 1. List User's Bookings
**GET** `/bookings/`

**Headers:**
```
Authorization: Token abc123def456...
```

**Response (200 OK):**
```json
{
  "count": 2,
  "results": [
    {
      "id": 1,
      "user": 1,
      "booking_type": "hotel",
      "hotel": 1,
      "cab": null,
      "destination": null,
      "check_in_date": "2024-02-15",
      "check_out_date": "2024-02-20",
      "number_of_guests": 2,
      "number_of_rooms": 1,
      "total_price": 1250,
      "payment_status": "pending",
      "booking_status": "confirmed",
      "booking_date": "2024-01-23T10:00:00Z"
    }
  ]
}
```

### 2. Create Booking
**POST** `/bookings/`

**Headers:**
```
Authorization: Token abc123def456...
```

**Request Body:**
```json
{
  "booking_type": "hotel",
  "hotel": 1,
  "check_in_date": "2024-02-15",
  "check_out_date": "2024-02-20",
  "number_of_guests": 2,
  "number_of_rooms": 1,
  "total_price": 1250,
  "booking_status": "confirmed"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "user": 1,
  "booking_type": "hotel",
  ...
}
```

### 3. Get Booking by ID
**GET** `/bookings/{id}/`

**Headers:**
```
Authorization: Token abc123def456...
```

### 4. Update Booking
**PUT** `/bookings/{id}/`

**Headers:**
```
Authorization: Token abc123def456...
```

**Request Body:**
```json
{
  "number_of_rooms": 2,
  "total_price": 2500
}
```

### 5. Delete Booking
**DELETE** `/bookings/{id}/`

**Headers:**
```
Authorization: Token abc123def456...
```

**Note:** Only pending bookings can be deleted.

### 6. Cancel Booking
**POST** `/bookings/{id}/cancel/`

**Headers:**
```
Authorization: Token abc123def456...
```

**Response (200 OK):**
```json
{
  "id": 1,
  "booking_status": "cancelled",
  ...
}
```

### 7. Get My Bookings
**GET** `/bookings/my_bookings/`

### 8. Get Pending Bookings
**GET** `/bookings/pending/`

### 9. Get Confirmed Bookings
**GET** `/bookings/confirmed/`

---

## Contact Endpoints (Full CRUD)

### 1. Create Contact Message
**POST** `/contacts/`

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+33-123-456",
  "subject": "Tour Inquiry",
  "message": "I would like more information about your tours"
}
```

**Response (201 Created):**
```json
{
  "message": "Thank you for contacting us. We will get back to you soon.",
  "contact": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+33-123-456",
    "subject": "Tour Inquiry",
    "message": "I would like more information about your tours",
    "status": "new",
    "created_at": "2024-01-23T10:00:00Z"
  }
}
```

### 2. List All Contact Messages (Admin)
**GET** `/contacts/`

**Headers:**
```
Authorization: Token admin_token...
```

### 3. Get Contact by ID
**GET** `/contacts/{id}/`

### 4. Delete Contact Message
**DELETE** `/contacts/{id}/`

### 5. Mark as Read
**POST** `/contacts/{id}/mark_as_read/`

**Response (200 OK):**
```json
{
  "id": 1,
  "status": "read",
  ...
}
```

### 6. Mark as Resolved
**POST** `/contacts/{id}/mark_as_resolved/`

**Response (200 OK):**
```json
{
  "id": 1,
  "status": "resolved",
  ...
}
```

### 7. Get Unread Messages
**GET** `/contacts/unread/`

---

## JavaScript API Client Usage

### Import the API
```html
<script src="/static/js/api-complete.js"></script>
```

### Authentication Examples
```javascript
// Register
await api.auth.register({
  email: 'user@example.com',
  password: 'securepassword',
  firstName: 'John',
  lastName: 'Doe'
});

// Login
const loginResult = await api.auth.login('user@example.com', 'securepassword');
console.log(loginResult.token); // Use this token for authenticated requests

// Get current user
const user = await api.auth.getCurrentUser();

// Update profile
await api.auth.updateProfile(userId, {
  first_name: 'Jane',
  last_name: 'Smith'
});

// Logout
await api.auth.logout();
```

### Destinations Examples
```javascript
// Get all destinations
const destinations = await api.destinations.getAll();

// Search destinations
const results = await api.destinations.search('Paris');

// Get popular destinations
const popular = await api.destinations.getPopular();

// Create new destination
await api.destinations.create({
  name: 'Tokyo',
  city: 'Tokyo',
  country: 'Japan',
  description: 'Capital of Japan',
  best_time_to_visit: 'March-May',
  attractions: ['Senso-ji', 'Meiji Shrine'],
  average_cost: 4000,
  rating: 4.7
});

// Update destination
await api.destinations.update(1, {
  rating: 4.9
});

// Delete destination
await api.destinations.delete(1);
```

### Hotels Examples
```javascript
// Get all hotels
const hotels = await api.hotels.getAll();

// Search hotels
const results = await api.hotels.search('luxury');

// Filter by price
const affordable = await api.hotels.getByPriceRange(50, 200);

// Get available hotels
const available = await api.hotels.getAvailable();

// Create hotel
await api.hotels.create({
  name: 'Grand Hotel',
  location: 'Tokyo Center',
  destination: 1,
  price_per_night: 150,
  amenities: ['WiFi', 'Pool'],
  available_rooms: 20,
  total_rooms: 100
});
```

### Bookings Examples
```javascript
// Get my bookings
const bookings = await api.bookings.getMyBookings();

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

// Cancel booking
await api.bookings.cancel(bookingId);

// Get pending bookings
const pending = await api.bookings.getPending();
```

### Contact Examples
```javascript
// Send contact message
await api.contacts.create({
  name: 'John Doe',
  email: 'john@example.com',
  phone: '+1-234-567',
  subject: 'Inquiry',
  message: 'I have a question about tours'
});
```

---

## Error Handling

All API endpoints return appropriate HTTP status codes:

- **200 OK** - Successful GET, PUT
- **201 Created** - Successful POST
- **204 No Content** - Successful DELETE
- **400 Bad Request** - Invalid input
- **401 Unauthorized** - Missing/invalid token
- **403 Forbidden** - Insufficient permissions
- **404 Not Found** - Resource not found
- **500 Internal Server Error** - Server error

### Error Response Example
```json
{
  "error": "Invalid credentials",
  "detail": "Username and password do not match"
}
```

---

## Database Structure

### Django ORM Models
- **User** - Django's built-in User model with authentication
- **Destination** - Tour destinations
- **Hotel** - Hotel accommodations
- **Cab** - Transportation services
- **Booking** - User bookings
- **Contact** - Contact messages

### MongoDB Collections
- **tours** - Destination, Hotel, Cab data (analytics)
- **users** - User reference data
- **bookings** - Booking analytics
- **reviews** - User reviews (future)
- **payments** - Payment tracking (future)

---

## Production Deployment Checklist

- [ ] Set `DEBUG = False` in settings.py
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set strong `SECRET_KEY`
- [ ] Configure CORS properly
- [ ] Use HTTPS only
- [ ] Set up proper logging
- [ ] Configure database backups
- [ ] Set up MongoDB authentication
- [ ] Use environment variables for secrets
- [ ] Enable rate limiting
- [ ] Set up monitoring and alerts
- [ ] Configure proper error tracking (Sentry)
- [ ] Set up API documentation (Swagger/OpenAPI)

---

## Support & Contact
For API support, contact: support@tourguide.com
