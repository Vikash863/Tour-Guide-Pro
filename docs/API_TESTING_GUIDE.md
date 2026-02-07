# 🧪 API Testing Guide for TourGuidePro

## Using Postman or cURL

### 1. User Registration

**URL:** `POST http://localhost:5000/api/auth/register`

**cURL:**
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123",
    "phone": "+919876543210"
  }'
```

**Postman:**
- Method: POST
- URL: http://localhost:5000/api/auth/register
- Body (JSON):
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123",
  "phone": "+919876543210"
}
```

**Expected Response:**
```json
{
  "message": "User registered successfully",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "507f1f77bcf86cd799439011",
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+919876543210"
  }
}
```

---

### 2. User Login

**URL:** `POST http://localhost:5000/api/auth/login`

**cURL:**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'
```

**Expected Response:**
```json
{
  "message": "Logged in successfully",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "507f1f77bcf86cd799439011",
    "name": "John Doe",
    "email": "john@example.com"
  }
}
```

---

### 3. Get Current User (Requires Token)

**URL:** `GET http://localhost:5000/api/auth/me`

**cURL:**
```bash
curl -X GET http://localhost:5000/api/auth/me \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Postman:**
- Method: GET
- URL: http://localhost:5000/api/auth/me
- Headers:
  - Key: Authorization
  - Value: Bearer {your_token}

---

### 4. Get All Destinations

**URL:** `GET http://localhost:5000/api/destinations`

**cURL:**
```bash
curl http://localhost:5000/api/destinations
```

**Expected Response:**
```json
{
  "destinations": [
    {
      "_id": "507f1f77bcf86cd799439011",
      "name": "Agra",
      "description": "Home to the iconic Taj Mahal...",
      "location": {
        "city": "Agra",
        "state": "Uttar Pradesh",
        "country": "India"
      },
      "bestTimeToVisit": "October to March",
      "attractions": ["Taj Mahal", "Agra Fort", "Mehtab Bagh"],
      "averageCost": 5000,
      "rating": 4.8
    }
    // ... more destinations
  ]
}
```

---

### 5. Search Destinations

**URL:** `GET http://localhost:5000/api/destinations/search?name=Agra`

**cURL:**
```bash
curl "http://localhost:5000/api/destinations/search?name=Agra"
```

---

### 6. Get All Hotels

**URL:** `GET http://localhost:5000/api/hotels`

**cURL:**
```bash
curl http://localhost:5000/api/hotels
```

---

### 7. Search Hotels by Location

**URL:** `GET http://localhost:5000/api/hotels/search?location=Agra`

**cURL:**
```bash
curl "http://localhost:5000/api/hotels/search?location=Agra"
```

---

### 8. Get All Cabs

**URL:** `GET http://localhost:5000/api/cabs`

**cURL:**
```bash
curl http://localhost:5000/api/cabs
```

---

### 9. Filter Cabs

**URL:** `GET http://localhost:5000/api/cabs/filter?vehicleType=economy&minPrice=5&maxPrice=20`

**cURL:**
```bash
curl "http://localhost:5000/api/cabs/filter?vehicleType=economy&minPrice=5&maxPrice=20"
```

---

### 10. Create a Booking (Requires Token)

**URL:** `POST http://localhost:5000/api/bookings`

**cURL:**
```bash
curl -X POST http://localhost:5000/api/bookings \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {your_token}" \
  -d '{
    "bookingType": "hotel",
    "hotelId": "507f1f77bcf86cd799439011",
    "checkInDate": "2025-02-15",
    "checkOutDate": "2025-02-20",
    "numberOfGuests": 2,
    "numberOfRooms": 1,
    "totalPrice": 40000
  }'
```

**Postman:**
- Method: POST
- URL: http://localhost:5000/api/bookings
- Headers:
  - Key: Authorization
  - Value: Bearer {your_token}
- Body (JSON):
```json
{
  "bookingType": "hotel",
  "hotelId": "507f1f77bcf86cd799439011",
  "checkInDate": "2025-02-15",
  "checkOutDate": "2025-02-20",
  "numberOfGuests": 2,
  "numberOfRooms": 1,
  "totalPrice": 40000
}
```

---

### 11. Get User Bookings (Requires Token)

**URL:** `GET http://localhost:5000/api/bookings`

**cURL:**
```bash
curl -X GET http://localhost:5000/api/bookings \
  -H "Authorization: Bearer {your_token}"
```

---

### 12. Submit Contact Form

**URL:** `POST http://localhost:5000/api/contact`

**cURL:**
```bash
curl -X POST http://localhost:5000/api/contact \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+919876543210",
    "subject": "Booking Issue",
    "message": "I have an issue with my booking"
  }'
```

---

## Postman Collection Setup

### 1. Create Environment Variable

In Postman, create an environment variable:
- Variable Name: `token`
- Initial Value: (empty)

### 2. After Login Request

In the "Tests" tab of the login request, add:
```javascript
var jsonData = pm.response.json();
pm.environment.set("token", jsonData.token);
```

### 3. Use Token in Requests

For any request requiring authentication, in the Headers tab:
- Key: `Authorization`
- Value: `Bearer {{token}}`

---

## Testing Workflow

### Step 1: Register
```bash
POST /api/auth/register
→ Save the token
```

### Step 2: Login (Optional)
```bash
POST /api/auth/login
→ Save the token
```

### Step 3: View Destinations
```bash
GET /api/destinations
→ Get list of all destinations
```

### Step 4: Search Hotels
```bash
GET /api/hotels/search?location=Agra
→ Get hotels in Agra
```

### Step 5: Create Booking
```bash
POST /api/bookings
→ Create a new booking (requires token)
```

### Step 6: View Your Bookings
```bash
GET /api/bookings
→ Get all your bookings (requires token)
```

### Step 7: Submit Contact
```bash
POST /api/contact
→ Send a message
```

---

## Common Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request (invalid data) |
| 401 | Unauthorized (missing/invalid token) |
| 403 | Forbidden (no permission) |
| 404 | Not Found |
| 500 | Server Error |

---

## Error Response Example

```json
{
  "message": "Invalid credentials"
}
```

---

## Tips for Testing

1. **Save Tokens** - After login, copy the token and use in Authorization header
2. **Use Postman Collections** - Create a collection for easy testing
3. **Check Content-Type** - Always use `Content-Type: application/json`
4. **Verify Token Format** - Should start with "Bearer "
5. **Test One Endpoint at a Time** - Verify each endpoint works

---

## Troubleshooting

### "Token not valid"
- Make sure token hasn't expired
- Check token format in Authorization header
- Verify .env JWT_SECRET matches

### "MongoDB connection error"
- Make sure MongoDB is running
- Check MONGODB_URI in .env
- For MongoDB Atlas, whitelist your IP

### "Port 5000 already in use"
- Change PORT in .env
- Or kill the process: `npx kill-port 5000`

### "CORS error"
- Backend already has CORS enabled
- Clear browser cache
- Check browser console for exact error

---

## Quick Test Commands

```bash
# Test server is running
curl http://localhost:5000

# Get all destinations
curl http://localhost:5000/api/destinations | json_pp

# Get all hotels
curl http://localhost:5000/api/hotels | json_pp

# Get all cabs
curl http://localhost:5000/api/cabs | json_pp
```

---

**Happy Testing! 🚀**
