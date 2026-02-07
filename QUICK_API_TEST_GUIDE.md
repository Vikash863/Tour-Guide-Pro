# Quick API Testing Guide

## 🧪 Test Your API Locally

### Start the Server
```bash
python manage.py runserver
```

Server will be available at: `http://localhost:8000`

---

## 📝 Test Scenarios

### 1. User Authentication Flow

#### Register User
```javascript
// In browser console
const registerResult = await api.auth.register({
    firstName: 'John',
    lastName: 'Doe',
    email: 'john@example.com',
    password: 'testpass123'
});
console.log(registerResult);
```

**Expected Response**:
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "john",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

#### Login User
```javascript
const loginResult = await api.auth.login('john@example.com', 'testpass123');
console.log(loginResult.token); // Save this token!
// Expected: "abc123def456..."
```

#### Get Current User
```javascript
const user = await api.auth.getCurrentUser();
console.log(user);
```

#### Update Profile
```javascript
const updated = await api.auth.updateProfile(1, {
    first_name: 'Jane',
    email: 'jane@example.com'
});
console.log(updated);
```

---

### 2. Destinations CRUD

#### Create Destination
```javascript
const dest = await api.destinations.create({
    name: 'Paris',
    city: 'Paris',
    state: 'Île-de-France',
    country: 'France',
    description: 'City of lights and romance',
    best_time_to_visit: 'April-May, September-October',
    attractions: ['Eiffel Tower', 'Louvre Museum', 'Arc de Triomphe'],
    average_cost: 5000,
    rating: 4.8,
    image: null
});
console.log(dest);
```

#### Get All Destinations
```javascript
const destinations = await api.destinations.getAll();
console.log(destinations);
```

#### Search Destinations
```javascript
const results = await api.destinations.search('Paris');
console.log(results);
```

#### Get By ID
```javascript
const destination = await api.destinations.getById(1);
console.log(destination);
```

#### Update Destination
```javascript
const updated = await api.destinations.update(1, {
    rating: 4.9,
    average_cost: 5500
});
console.log(updated);
```

#### Delete Destination
```javascript
const result = await api.destinations.delete(1);
console.log(result); // { success: true }
```

#### Get Popular Destinations
```javascript
const popular = await api.destinations.popular();
console.log(popular);
```

#### Filter by Country
```javascript
const french = await api.destinations.getByCountry('France');
console.log(french);
```

---

### 3. Hotels CRUD

#### Create Hotel
```javascript
const hotel = await api.hotels.create({
    name: 'Luxury Hotel Paris',
    location: 'Central Paris',
    destination: 1,
    description: '5-star luxury hotel in the heart of Paris',
    price_per_night: 250,
    rating: 4.7,
    amenities: ['WiFi', 'Pool', 'Gym', 'Restaurant', 'Spa'],
    available_rooms: 15,
    total_rooms: 50,
    phone: '+33-1-234-5678',
    email: 'info@luxhotel.com',
    image: null
});
console.log(hotel);
```

#### Get All Hotels
```javascript
const hotels = await api.hotels.getAll();
console.log(hotels);
```

#### Search Hotels
```javascript
const results = await api.hotels.search('luxury');
console.log(results);
```

#### Filter by Price
```javascript
const affordable = await api.hotels.getByPriceRange(100, 300);
console.log(affordable);
```

#### Get Available Hotels
```javascript
const available = await api.hotels.getAvailable();
console.log(available);
```

#### Update Hotel
```javascript
const updated = await api.hotels.update(1, {
    available_rooms: 10,
    rating: 4.8
});
console.log(updated);
```

#### Delete Hotel
```javascript
const result = await api.hotels.delete(1);
console.log(result);
```

---

### 4. Cabs CRUD

#### Create Cab
```javascript
const cab = await api.cabs.create({
    company_name: 'Uber',
    vehicle_type: 'economy',
    price_per_km: 15.50,
    price_per_hour: 250,
    capacity: 4,
    rating: 4.6,
    available_cars: 25,
    description: 'Affordable ride-sharing service',
    phone: '+33-1-800-UBER',
    email: 'support@uber.com',
    image: null
});
console.log(cab);
```

#### Get All Cabs
```javascript
const cabs = await api.cabs.getAll();
console.log(cabs);
```

#### Filter Cabs
```javascript
const filteredCabs = await api.cabs.filter('economy', 10, 50);
console.log(filteredCabs);
```

#### Get by Company
```javascript
const uberCabs = await api.cabs.getByCompany('Uber');
console.log(uberCabs);
```

#### Get Available Cabs
```javascript
const available = await api.cabs.getAvailable();
console.log(available);
```

#### Update Cab
```javascript
const updated = await api.cabs.update(1, {
    available_cars: 30,
    rating: 4.7
});
console.log(updated);
```

---

### 5. Bookings CRUD (Requires Authentication)

#### Create Booking
```javascript
const booking = await api.bookings.create({
    booking_type: 'hotel',
    hotel: 1,
    cab: null,
    destination: null,
    check_in_date: '2024-02-15',
    check_out_date: '2024-02-20',
    number_of_guests: 2,
    number_of_rooms: 1,
    total_price: 1250,
    booking_status: 'confirmed'
});
console.log(booking);
```

#### Get My Bookings
```javascript
const myBookings = await api.bookings.getMyBookings();
console.log(myBookings);
```

#### Get Pending Bookings
```javascript
const pending = await api.bookings.getPending();
console.log(pending);
```

#### Get Confirmed Bookings
```javascript
const confirmed = await api.bookings.getConfirmed();
console.log(confirmed);
```

#### Cancel Booking
```javascript
const cancelled = await api.bookings.cancel(1);
console.log(cancelled);
```

#### Update Booking
```javascript
const updated = await api.bookings.update(1, {
    number_of_rooms: 2,
    total_price: 2500
});
console.log(updated);
```

#### Delete Booking
```javascript
const result = await api.bookings.delete(1);
console.log(result);
```

---

### 6. Contacts CRUD

#### Submit Contact Form
```javascript
const contact = await api.contacts.create({
    name: 'John Smith',
    email: 'john.smith@example.com',
    phone: '+33-123-456-7890',
    subject: 'Tour Package Inquiry',
    message: 'I would like more information about your Paris tour packages.'
});
console.log(contact);
```

#### Get All Messages (Admin)
```javascript
const messages = await api.contacts.getAll();
console.log(messages);
```

#### Mark as Read
```javascript
const read = await api.contacts.markAsRead(1);
console.log(read);
```

#### Mark as Resolved
```javascript
const resolved = await api.contacts.markAsResolved(1);
console.log(resolved);
```

#### Get Unread Messages
```javascript
const unread = await api.contacts.getUnread();
console.log(unread);
```

---

## 🔍 Using cURL Commands

### Register User
```bash
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john",
    "email": "john@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### Login User
```bash
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john",
    "password": "testpass123"
  }'
```

### Create Destination
```bash
curl -X POST http://localhost:8000/api/destinations/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tokyo",
    "city": "Tokyo",
    "state": "Tokyo",
    "country": "Japan",
    "description": "Capital of Japan",
    "best_time_to_visit": "March-May",
    "attractions": ["Senso-ji", "Meiji Shrine"],
    "average_cost": 4000,
    "rating": 4.7
  }'
```

### Get All Destinations
```bash
curl http://localhost:8000/api/destinations/
```

### Create Hotel
```bash
curl -X POST http://localhost:8000/api/hotels/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Grand Hotel Tokyo",
    "location": "Shibuya",
    "destination": 1,
    "description": "Luxury hotel",
    "price_per_night": 200,
    "rating": 4.6,
    "amenities": ["WiFi", "Pool"],
    "available_rooms": 20,
    "total_rooms": 100,
    "phone": "+81-3-1234-5678",
    "email": "info@grandhotel.jp"
  }'
```

### Create Booking (Requires Token)
```bash
curl -X POST http://localhost:8000/api/bookings/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -d '{
    "booking_type": "hotel",
    "hotel": 1,
    "check_in_date": "2024-02-15",
    "check_out_date": "2024-02-20",
    "number_of_guests": 2,
    "number_of_rooms": 1,
    "total_price": 1000,
    "booking_status": "confirmed"
  }'
```

### Get Bookings (Requires Token)
```bash
curl http://localhost:8000/api/bookings/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### Submit Contact Form
```bash
curl -X POST http://localhost:8000/api/contacts/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "email": "jane@example.com",
    "phone": "+1-234-567-8900",
    "subject": "Tour Inquiry",
    "message": "I want information about tours."
  }'
```

---

## 🧠 Test Data to Use

### Destinations
```javascript
[
  {
    name: 'Paris',
    city: 'Paris',
    country: 'France',
    description: 'City of lights',
    attractions: ['Eiffel Tower', 'Louvre'],
    average_cost: 5000,
    rating: 4.8
  },
  {
    name: 'Tokyo',
    city: 'Tokyo',
    country: 'Japan',
    description: 'Modern metropolis',
    attractions: ['Senso-ji', 'Tokyo Tower'],
    average_cost: 4000,
    rating: 4.6
  },
  {
    name: 'Dubai',
    city: 'Dubai',
    country: 'UAE',
    description: 'Luxury shopping',
    attractions: ['Burj Khalifa', 'Palm Jumeirah'],
    average_cost: 6000,
    rating: 4.5
  }
]
```

### Hotels
```javascript
[
  {
    name: 'Luxury Hotel Paris',
    location: 'Central Paris',
    destination: 1,
    price_per_night: 250,
    amenities: ['WiFi', 'Pool', 'Gym'],
    available_rooms: 10,
    total_rooms: 50
  },
  {
    name: 'Budget Hotel Tokyo',
    location: 'Shibuya',
    destination: 2,
    price_per_night: 80,
    amenities: ['WiFi', 'Breakfast'],
    available_rooms: 25,
    total_rooms: 75
  }
]
```

---

## ✅ Expected Test Results

All tests should return **HTTP 200/201** with proper JSON responses:

```json
{
  "id": 1,
  "name": "...",
  "created_at": "2024-01-23T...",
  "status": "success"
}
```

---

## 🐛 Troubleshooting

### Token Not Working
```javascript
// Clear storage and login again
localStorage.clear();
const result = await api.auth.login('email@example.com', 'password');
```

### CORS Error
- Check if CORS is enabled in Django settings
- Verify ALLOWED_ORIGINS in .env

### Database Error
- Check MongoDB is running
- Verify connection string in .env

### 404 Error
- Verify API endpoint URL
- Check if resource exists
- Verify HTTP method

---

## 📊 Sample Test Workflow

1. **Register**: Create a new user
2. **Login**: Get authentication token
3. **Create**: Add destination, hotel, cab
4. **Read**: Retrieve the created items
5. **Update**: Modify the items
6. **Search**: Find items by criteria
7. **Book**: Create booking (requires auth)
8. **Contact**: Submit contact form
9. **Cancel**: Cancel booking
10. **Delete**: Remove destination/hotel

---

## 🎉 Success Indicators

✅ Registration returns 201 with user data  
✅ Login returns token  
✅ CRUD operations return proper status codes  
✅ MongoDB stores data  
✅ Search filters work correctly  
✅ Bookings require authentication  
✅ Contact form submits successfully  

---

**Happy Testing! 🧪**
