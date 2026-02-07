# TourGuidePro - Complete Travel Planning Application

A full-stack travel planning and booking application built with Node.js, Express, MongoDB, and vanilla JavaScript.

## 🚀 Features

- **User Authentication**: Secure registration and login with JWT
- **Destination Management**: Browse and search thousands of destinations
- **Hotel Booking**: Find and book hotels near tourist spots
- **Cab Services**: Book cabs with various vehicle types and pricing
- **Itinerary Planning**: Create and manage personalized travel plans
- **Contact Management**: Send queries and get responses from support team
- **Real-time Booking**: Make instant bookings and manage them
- **User Dashboard**: View all bookings and travel history

## 📋 Prerequisites

- Node.js (v14 or higher)
- MongoDB (local or cloud instance like MongoDB Atlas)
- npm or yarn

## 🔧 Installation & Setup

### 1. Install Dependencies

```bash
cd Tour
npm install
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```env
MONGODB_URI=mongodb://localhost:27017/tourguidepro
JWT_SECRET=your_super_secret_jwt_key_change_in_production
JWT_EXPIRE=7d
PORT=5000
NODE_ENV=development
```

**For MongoDB Atlas (Cloud):**
```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/tourguidepro
```

### 3. Seed Initial Data

Add sample destinations, hotels, and cabs to the database:

```bash
node seed.js
```

### 4. Start the Server

```bash
npm start
```

Or for development with auto-reload:

```bash
npm run dev
```

The server will run on `http://localhost:5000`

## 📁 Project Structure

```
Tour/
├── models/                 # MongoDB models
│   ├── User.js
│   ├── Destination.js
│   ├── Hotel.js
│   ├── Cab.js
│   ├── Booking.js
│   └── Contact.js
├── controllers/            # Business logic
│   ├── authController.js
│   ├── destinationController.js
│   ├── hotelController.js
│   ├── cabController.js
│   ├── bookingController.js
│   └── contactController.js
├── routes/                 # API routes
│   ├── auth.js
│   ├── destinations.js
│   ├── hotels.js
│   ├── cabs.js
│   ├── bookings.js
│   └── contact.js
├── middleware/             # Express middleware
│   └── auth.js
├── api.js                  # Frontend API utility
├── server.js               # Main server file
├── seed.js                 # Database seed script
├── Home.html/.js/.css      # Home page
├── login.html/.js/.css     # Login page
├── signup.html/.js/.css    # Sign up page
├── destination.html/.js/.css
├── hotel.html/.js/.css
├── cab.html/.js/.css
├── iterenary.html/.js/.css
├── contact.html/.js/.css
└── package.json
```

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user (requires token)

### Destinations
- `GET /api/destinations` - Get all destinations
- `GET /api/destinations/search?name=` - Search destination by name
- `GET /api/destinations/:id` - Get destination by ID
- `POST /api/destinations` - Create destination (admin)
- `PUT /api/destinations/:id` - Update destination
- `DELETE /api/destinations/:id` - Delete destination

### Hotels
- `GET /api/hotels` - Get all hotels
- `GET /api/hotels/search?location=` - Search hotels by location
- `GET /api/hotels/:id` - Get hotel by ID
- `POST /api/hotels` - Create hotel (admin)
- `PUT /api/hotels/:id` - Update hotel
- `DELETE /api/hotels/:id` - Delete hotel

### Cabs
- `GET /api/cabs` - Get all cabs
- `GET /api/cabs/filter?vehicleType=&minPrice=&maxPrice=` - Filter cabs
- `GET /api/cabs/:id` - Get cab by ID
- `POST /api/cabs` - Create cab (admin)
- `PUT /api/cabs/:id` - Update cab
- `DELETE /api/cabs/:id` - Delete cab

### Bookings
- `GET /api/bookings` - Get user bookings (requires auth)
- `GET /api/bookings/:id` - Get booking by ID
- `POST /api/bookings` - Create booking (requires auth)
- `PUT /api/bookings/:id` - Update booking
- `DELETE /api/bookings/:id` - Cancel booking

### Contact
- `POST /api/contact` - Submit contact form
- `GET /api/contact` - Get all messages (admin)
- `GET /api/contact/:id` - Get message by ID
- `PUT /api/contact/:id/read` - Mark as read
- `DELETE /api/contact/:id` - Delete message

## 🔐 Authentication

The app uses JWT (JSON Web Tokens) for authentication:

1. Users register/login to get a token
2. Token is stored in localStorage
3. Token is sent in Authorization header: `Bearer <token>`
4. Token expires after 7 days

## 📊 MongoDB Collections

### User Schema
```javascript
{
  name: String,
  email: String (unique),
  password: String (hashed),
  phone: String,
  createdAt: Date
}
```

### Destination Schema
```javascript
{
  name: String (unique),
  description: String,
  location: { city, state, country },
  bestTimeToVisit: String,
  attractions: [String],
  averageCost: Number,
  rating: Number,
  createdAt: Date
}
```

### Hotel Schema
```javascript
{
  name: String,
  location: String,
  destination: ObjectId,
  description: String,
  pricePerNight: Number,
  rating: Number,
  amenities: [String],
  rooms: { available, total },
  contact: { phone, email },
  createdAt: Date
}
```

### Cab Schema
```javascript
{
  companyName: String,
  vehicleType: enum ['economy', 'premium', 'luxury', 'van'],
  pricePerKm: Number,
  pricePerHour: Number,
  capacity: Number,
  rating: Number,
  contact: { phone, email },
  availableCars: Number,
  createdAt: Date
}
```

### Booking Schema
```javascript
{
  userId: ObjectId,
  bookingType: enum ['hotel', 'cab', 'destination'],
  hotelId/cabId/destinationId: ObjectId,
  checkInDate: Date,
  checkOutDate: Date,
  totalPrice: Number,
  paymentStatus: enum ['pending', 'completed', 'cancelled'],
  bookingStatus: enum ['confirmed', 'cancelled', 'completed'],
  bookingDate: Date
}
```

## 🛠️ Using the Frontend API

All frontend files have access to the `api` object which provides these methods:

```javascript
// Auth
await api.register(name, email, password, phone);
await api.login(email, password);
await api.getCurrentUser();

// Destinations
await api.getAllDestinations();
await api.searchDestination(name);
await api.getDestinationById(id);

// Hotels
await api.getAllHotels();
await api.searchHotels(location);
await api.getHotelById(id);

// Cabs
await api.getAllCabs();
await api.filterCabs(vehicleType, minPrice, maxPrice);
await api.getCabById(id);

// Bookings
await api.getUserBookings();
await api.createBooking(bookingData);
await api.updateBooking(id, bookingData);
await api.cancelBooking(id);

// Contact
await api.submitContact(name, email, phone, subject, message);
```

## 🚀 Deployment

### Deploy to Heroku

```bash
heroku login
heroku create your-app-name
heroku config:set MONGODB_URI=your_mongodb_uri JWT_SECRET=your_secret
git push heroku main
```

### Deploy to AWS/Azure

Use Docker:

```dockerfile
FROM node:16
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 5000
CMD ["npm", "start"]
```

## 📝 Notes

- All passwords are hashed with bcryptjs
- JWT tokens expire after 7 days
- Authentication is required for bookings
- Admin routes can be added for managing destinations, hotels, and cabs
- CORS is enabled for frontend access

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

MIT License

## 📞 Support

For issues and questions, please contact: support@tourguidepro.com

---

Happy traveling with TourGuidePro! 🌍✈️
