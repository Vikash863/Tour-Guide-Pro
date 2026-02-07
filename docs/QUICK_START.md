# 🚀 TourGuidePro - Quick Start Guide

## ✅ What's Been Created

Your TourGuidePro application is now fully functional with a complete backend! Here's what you have:

### Backend
- ✅ Express.js server
- ✅ MongoDB database with 6 models (User, Destination, Hotel, Cab, Booking, Contact)
- ✅ JWT authentication system
- ✅ RESTful API with 30+ endpoints
- ✅ Password hashing with bcryptjs
- ✅ CORS enabled for frontend

### Frontend Integration
- ✅ Updated login/signup pages with backend API integration
- ✅ Contact form connected to MongoDB
- ✅ User authentication with token management
- ✅ API utility file (api.js) for easy API calls

### Database Models
- User (with authentication)
- Destination (tourist spots)
- Hotel (accommodations)
- Cab (transportation)
- Booking (reservations)
- Contact (customer messages)

---

## 🎯 Getting Started (5 Minutes)

### Step 1: Install MongoDB
**Option A: Local Installation**
- Download from https://www.mongodb.com/try/download/community
- Install and start MongoDB service

**Option B: MongoDB Atlas (Cloud - Recommended)**
- Sign up at https://www.mongodb.com/cloud/atlas
- Create a free cluster
- Copy your connection string

### Step 2: Configure Environment
Edit `.env` file with your MongoDB URI:
```env
MONGODB_URI=mongodb://localhost:27017/tourguidepro
# OR for MongoDB Atlas:
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/tourguidepro
JWT_SECRET=your_super_secret_key_123
PORT=5000
```

### Step 3: Install Dependencies
```bash
npm install
```

### Step 4: Seed Sample Data
```bash
node seed.js
```
This will add sample destinations, hotels, and cabs to your database.

### Step 5: Start the Server
```bash
npm start
```

You should see:
```
Server running on port 5000
MongoDB connected successfully
```

---

## 🧪 Testing the Application

### In Your Browser:
1. Open `http://localhost:5000`
2. You'll see the TourGuidePro home page
3. Click user icon → Sign Up
4. Create an account with email and password
5. Login with your credentials
6. Explore destinations, hotels, and cabs
7. Make bookings

### Using Postman/cURL:

**Test Registration:**
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"John","email":"john@example.com","password":"password123"}'
```

**Test Login:**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"password123"}'
```

**Get All Destinations:**
```bash
curl http://localhost:5000/api/destinations
```

**Search Hotels:**
```bash
curl "http://localhost:5000/api/hotels/search?location=Agra"
```

---

## 📱 Frontend Pages & Functionality

| Page | Features |
|------|----------|
| **Home** | Hero section, destination showcase, authentication |
| **Login** | Email/password login with backend validation |
| **Signup** | Create new account with validation |
| **Destinations** | Search and view destination details |
| **Hotels** | Search hotels by location, view details |
| **Cabs** | Browse cabs, filter by type and price |
| **Itinerary** | Create and manage travel plans |
| **Contact** | Send messages to support team |

---

## 🔑 Key Features

### 1. User Authentication
```javascript
// Automatically handled in frontend
// Users are logged in and token stored in localStorage
const user = auth.getUser(); // Get current user
const isLoggedIn = auth.isLoggedIn(); // Check if logged in
auth.logout(); // Logout user
```

### 2. Making API Calls
```javascript
// All API calls are in api.js
// Example: Search hotels
const result = await api.searchHotels('Agra');
```

### 3. Bookings
Users can:
- Book hotels with check-in/check-out dates
- Book cabs with pickup/dropoff
- View all their bookings
- Cancel bookings
- Track payment status

---

## 📊 Database Structure

Your MongoDB database will have these collections:

```
tourguidepro (database)
├── users (User accounts)
├── destinations (Tourist destinations)
├── hotels (Accommodations)
├── cabs (Transportation)
├── bookings (User reservations)
└── contacts (Customer messages)
```

You can view and manage data using:
- MongoDB Compass (GUI tool)
- MongoDB Atlas Dashboard (cloud)
- Postman

---

## 🔒 Security Features

✅ Passwords hashed with bcryptjs
✅ JWT token-based authentication
✅ CORS protection
✅ Input validation
✅ Secure headers
✅ Environment variable protection

---

## 🐛 Troubleshooting

### "MongoDB connection error"
- Make sure MongoDB is running
- Check connection string in .env
- For MongoDB Atlas: whitelist your IP address

### "Port 5000 already in use"
- Change PORT in .env file
- Or kill the process: `npx kill-port 5000`

### "Token not found"
- Clear localStorage: `localStorage.clear()`
- Login again

### "CORS error"
- Backend already has CORS enabled
- Clear browser cache

---

## 🚀 Next Steps

### Add More Features:
1. **Payment Integration**: Stripe or Razorpay
2. **Email Notifications**: Send booking confirmations
3. **Admin Panel**: Manage destinations, hotels, cabs
4. **Reviews & Ratings**: Users can review bookings
5. **Search Filters**: Advanced filtering options
6. **Real-time Chat**: Live customer support
7. **Mobile App**: React Native version

### Deployment:
1. Deploy backend to Heroku, AWS, or Azure
2. Update API_BASE_URL in api.js to production URL
3. Deploy frontend to Vercel or Netlify

### Database Optimization:
1. Add indexes for frequently searched fields
2. Implement caching with Redis
3. Add pagination for large datasets

---

## 📚 File Reference

**Key Backend Files:**
- `server.js` - Main server file
- `models/` - MongoDB schemas
- `controllers/` - Business logic
- `routes/` - API endpoints
- `middleware/auth.js` - Authentication

**Key Frontend Files:**
- `api.js` - API utility for all HTTP requests
- `Home.html/.js` - Home page with auth
- `login.html/.js` - Login form connected to backend
- `signup.html/.js` - Registration form
- Other pages are ready for API integration

---

## 💡 Pro Tips

1. **Use MongoDB Atlas** for cloud database (easier than local)
2. **Test APIs with Postman** before integrating with frontend
3. **Check browser console** for JavaScript errors
4. **Use `npm run dev`** during development for auto-reload
5. **Keep .env file secure** - never commit to git

---

## 🎉 You're All Set!

Your TourGuidePro application is now:
✅ Fully functional
✅ Database-backed with MongoDB
✅ User authentication ready
✅ API-connected frontend
✅ Ready for production

Start the server and visit `http://localhost:5000` to see your application in action!

---

**Need help?** Check the SETUP_GUIDE.md for detailed documentation.

Happy coding! 🚀
