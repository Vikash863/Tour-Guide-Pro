# 📊 TourGuidePro Database Schema

Complete documentation of all database models and relationships.

---

## Models Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    User (Django Built-in)                   │
│  • id, username, email, password, created_at, updated_at    │
└─────────────────────────────────────────────────────────────┘
                    ↓              ↓
         ┌──────────┴──────────────┴──────────┐
         ↓                                    ↓
┌─────────────────────┐          ┌──────────────────────┐
│     Booking         │          │   Contact            │
│                     │          │                      │
│ • user_id (FK)      │          │ • name               │
│ • booking_type      │          │ • email              │
│ • hotel_id (FK)     │          │ • phone              │
│ • cab_id (FK)       │          │ • subject            │
│ • destination_id    │          │ • message            │
│ • total_price       │          │ • status             │
│ • status            │          │ • created_at         │
│ • created_at        │          │ • updated_at         │
└─────────────────────┘          └──────────────────────┘

        ↓                    ↓
┌──────────────────┐  ┌──────────────────────┐
│   Destination    │  │      Hotel           │
│                  │  │                      │
│ • name           │  │ • name               │
│ • description    │  │ • location           │
│ • city           │  │ • destination_id(FK) │
│ • state          │  │ • description        │
│ • country        │  │ • price_per_night    │
│ • attractions    │  │ • total_rooms        │
│ • average_cost   │  │ • available_rooms    │
│ • rating         │  │ • amenities          │
│ • image          │  │ • phone              │
│ • created_at     │  │ • email              │
│ • updated_at     │  │ • rating             │
└──────────────────┘  │ • image              │
                      │ • created_at         │
    ↓                 │ • updated_at         │
┌──────────────────┐  └──────────────────────┘
│      Cab         │
│                  │       ↓
│ • company_name   │
│ • vehicle_type   │
│ • price_per_km   │
│ • price_per_hour │
│ • capacity       │
│ • available_cars │
│ • total_cars     │
│ • amenities      │
│ • phone          │
│ • email          │
│ • rating         │
│ • image          │
│ • created_at     │
│ • updated_at     │
└──────────────────┘
```

---

## Detailed Model Definitions

### 1. **User** (Django Built-in)

#### Purpose
User account management for registration, authentication, and authorization.

#### Fields
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | PK, Auto | Primary key |
| username | String(150) | Unique | User login ID |
| email | Email | Unique | User email |
| password | String(128) | Hashed | Encrypted password |
| first_name | String(150) | - | User first name |
| last_name | String(150) | - | User last name |
| is_active | Boolean | Default: True | Account active status |
| is_staff | Boolean | Default: False | Admin access |
| date_joined | DateTime | Auto | Registration date |
| last_login | DateTime | Nullable | Last login time |

#### Relationships
- **One-to-Many**: User → Booking (user_id)
- **One-to-Many**: User → Contact (optional creator)

---

### 2. **Destination**

#### Purpose
Store tourist destinations with descriptions, attractions, and pricing information.

#### Fields
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | PK, Auto | Primary key |
| name | String(100) | Unique | Destination name |
| description | Text | - | Full description |
| city | String(50) | - | City name |
| state | String(50) | - | State/Region |
| country | String(50) | - | Country |
| best_time_to_visit | String(100) | - | Recommended season |
| attractions | JSON | Default: [] | List of attractions |
| average_cost | Integer | - | Estimated daily cost (INR) |
| rating | Float | Range: 0-5 | User rating |
| image | ImageField | Nullable | Destination photo |
| created_at | DateTime | Auto | Creation timestamp |
| updated_at | DateTime | Auto | Last update timestamp |

#### Examples
```json
{
  "id": 1,
  "name": "Agra",
  "city": "Agra",
  "state": "Uttar Pradesh",
  "country": "India",
  "attractions": ["Taj Mahal", "Agra Fort", "Fatehpur Sikri"],
  "best_time_to_visit": "October to March",
  "average_cost": 3000,
  "rating": 4.8
}
```

#### Relationships
- **One-to-Many**: Destination → Hotel (destination_id)
- **One-to-Many**: Destination → Booking (destination_id)

---

### 3. **Hotel**

#### Purpose
Store hotel information with pricing, amenities, and availability.

#### Fields
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | PK, Auto | Primary key |
| name | String(100) | - | Hotel name |
| location | String(100) | - | Hotel location |
| destination | ForeignKey | Destination | Associated destination |
| description | Text | - | Hotel description |
| price_per_night | Integer | - | Nightly rate (INR) |
| total_rooms | Integer | - | Total rooms available |
| available_rooms | Integer | - | Currently available |
| amenities | JSON | Default: [] | List of facilities |
| rating | Float | Range: 0-5 | Guest rating |
| phone | String(15) | - | Contact number |
| email | Email | - | Contact email |
| image | ImageField | Nullable | Hotel photo |
| created_at | DateTime | Auto | Creation timestamp |
| updated_at | DateTime | Auto | Last update timestamp |

#### Examples
```json
{
  "id": 1,
  "name": "Taj View Hotel",
  "location": "Taj Ganj, Agra",
  "destination": 1,
  "price_per_night": 5000,
  "total_rooms": 50,
  "available_rooms": 12,
  "amenities": ["WiFi", "AC", "Restaurant", "Parking", "Pool"],
  "rating": 4.5,
  "phone": "9876543210",
  "email": "info@tajview.com"
}
```

#### Relationships
- **Many-to-One**: Hotel → Destination (destination_id)
- **One-to-Many**: Hotel → Booking (hotel_id)

---

### 4. **Cab**

#### Purpose
Store taxi/transportation services with vehicle types and pricing.

#### Fields
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | PK, Auto | Primary key |
| company_name | String(100) | - | Company name |
| vehicle_type | String(20) | Choices | Type: economy/premium/luxury/van |
| price_per_km | Float | - | Pricing per kilometer |
| price_per_hour | Float | - | Hourly rate |
| capacity | Integer | - | Passenger capacity |
| total_cars | Integer | - | Fleet size |
| available_cars | Integer | - | Available vehicles |
| amenities | JSON | Default: [] | Vehicle features |
| rating | Float | Range: 0-5 | Service rating |
| phone | String(15) | - | Contact number |
| email | Email | - | Contact email |
| image | ImageField | Nullable | Vehicle photo |
| created_at | DateTime | Auto | Creation timestamp |
| updated_at | DateTime | Auto | Last update timestamp |

#### Vehicle Types
- **economy**: Standard cars ($5/km, 4 seats)
- **premium**: Sedans/SUVs ($8/km, 5 seats)
- **luxury**: High-end vehicles ($12/km, 4-5 seats)
- **van**: Group transport ($6/km, 8-12 seats)

#### Examples
```json
{
  "id": 1,
  "company_name": "TourCabs",
  "vehicle_type": "economy",
  "price_per_km": 5.0,
  "price_per_hour": 30.0,
  "capacity": 4,
  "total_cars": 100,
  "available_cars": 25,
  "amenities": ["AC", "Music System", "Basic Comfort"],
  "rating": 4.2,
  "phone": "9876543210",
  "email": "cabs@tourcabs.com"
}
```

#### Relationships
- **One-to-Many**: Cab → Booking (cab_id)

---

### 5. **Booking**

#### Purpose
Store user bookings for hotels, cabs, and destinations.

#### Fields
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | PK, Auto | Primary key |
| user | ForeignKey | User | Booking user |
| booking_type | String(20) | Choices | Type: hotel/cab/destination |
| hotel | ForeignKey | Hotel | Associated hotel (nullable) |
| cab | ForeignKey | Cab | Associated cab (nullable) |
| destination | ForeignKey | Destination | Associated destination (nullable) |
| check_in_date | Date | - | Check-in date |
| check_out_date | Date | - | Check-out date |
| number_of_guests | Integer | - | Number of travelers |
| number_of_rooms | Integer | Nullable | Rooms for hotel booking |
| total_price | Float | - | Total booking amount |
| payment_status | String(20) | Choices | pending/completed/failed |
| booking_status | String(20) | Choices | confirmed/cancelled/completed |
| booking_date | DateTime | Auto | Booking creation date |
| created_at | DateTime | Auto | Creation timestamp |
| updated_at | DateTime | Auto | Last update timestamp |

#### Status Choices
**Payment Status**:
- `pending` - Payment not yet received
- `completed` - Payment received
- `failed` - Payment failed

**Booking Status**:
- `confirmed` - Booking is confirmed
- `cancelled` - Booking cancelled
- `completed` - Trip completed

#### Examples
```json
{
  "id": 1,
  "user": 1,
  "booking_type": "hotel",
  "hotel": 1,
  "destination": 1,
  "check_in_date": "2026-02-01",
  "check_out_date": "2026-02-03",
  "number_of_guests": 2,
  "number_of_rooms": 1,
  "total_price": 10000.00,
  "payment_status": "completed",
  "booking_status": "confirmed"
}
```

#### Relationships
- **Many-to-One**: Booking → User (user_id)
- **Many-to-One**: Booking → Hotel (hotel_id, nullable)
- **Many-to-One**: Booking → Cab (cab_id, nullable)
- **Many-to-One**: Booking → Destination (destination_id, nullable)

---

### 6. **Contact**

#### Purpose
Store user inquiries and support messages.

#### Fields
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | PK, Auto | Primary key |
| name | String(100) | - | Sender name |
| email | Email | - | Sender email |
| phone | String(15) | - | Sender phone |
| subject | String(200) | - | Message subject |
| message | Text | - | Message content |
| status | String(20) | Choices | new/read/resolved |
| created_at | DateTime | Auto | Creation timestamp |
| updated_at | DateTime | Auto | Last update timestamp |

#### Status Choices
- `new` - Unread message
- `read` - Message read
- `resolved` - Issue resolved

#### Examples
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "9876543210",
  "subject": "Hotel Booking Issue",
  "message": "I have a question about my upcoming booking...",
  "status": "new"
}
```

#### Relationships
- None (standalone model)

---

## Database Relationships Diagram

```
┌──────────────────┐
│   User (Django)  │
│  id (PK)         │
│  username        │
│  email           │
│  password        │
└────────┬─────────┘
         │ (One-to-Many)
         │
         └──────────────────┬────────────────┐
                            ↓                 ↓
                    ┌─────────────────┐  ┌──────────────────┐
                    │   Booking       │  │   Contact        │
                    │                 │  │                  │
                    │ id (PK)         │  │ id (PK)          │
                    │ user_id (FK)    │  │ name             │
                    │ booking_type    │  │ email            │
                    │ total_price     │  │ subject          │
                    └────┬────┬───┬───┘  │ status           │
                         │    │   │      └──────────────────┘
            ┌────────────┴─┐  │   └─┐
            ↓              ↓  │     ↓
      ┌──────────────┐  ┌─────────────────┐  ┌──────────────────┐
      │   Destination│  │   Hotel         │  │      Cab         │
      │              │  │                 │  │                  │
      │ id (PK)      │  │ id (PK)         │  │ id (PK)          │
      │ name         │  │ destination_id  │  │ company_name     │
      │ description  │  │ (FK)→Destination│  │ vehicle_type     │
      │ attractions  │  │ name            │  │ price_per_km     │
      │ rating       │  │ price_per_night │  │ capacity         │
      │ image        │  │ available_rooms │  │ available_cars   │
      └──────────────┘  │ amenities       │  │ rating           │
                        │ rating          │  │ image            │
                        └─────────────────┘  └──────────────────┘
```

---

## SQL Schema

### Destination Table
```sql
CREATE TABLE api_destination (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL,
    description LONGTEXT NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL,
    best_time_to_visit VARCHAR(100),
    attractions JSON DEFAULT '[]',
    average_cost INTEGER NOT NULL,
    rating FLOAT DEFAULT 0 CHECK (rating >= 0 AND rating <= 5),
    image VARCHAR(100),
    created_at DATETIME AUTO_CURRENT_TIMESTAMP,
    updated_at DATETIME AUTO_UPDATE_CURRENT_TIMESTAMP
);
```

### Hotel Table
```sql
CREATE TABLE api_hotel (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(100) NOT NULL,
    destination_id INTEGER NOT NULL,
    description LONGTEXT,
    price_per_night INTEGER NOT NULL,
    total_rooms INTEGER NOT NULL,
    available_rooms INTEGER NOT NULL,
    amenities JSON DEFAULT '[]',
    rating FLOAT DEFAULT 0 CHECK (rating >= 0 AND rating <= 5),
    phone VARCHAR(15),
    email VARCHAR(254),
    image VARCHAR(100),
    created_at DATETIME AUTO_CURRENT_TIMESTAMP,
    updated_at DATETIME AUTO_UPDATE_CURRENT_TIMESTAMP,
    FOREIGN KEY (destination_id) REFERENCES api_destination(id)
);
```

### Cab Table
```sql
CREATE TABLE api_cab (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    company_name VARCHAR(100) NOT NULL,
    vehicle_type VARCHAR(20) NOT NULL CHECK (vehicle_type IN ('economy', 'premium', 'luxury', 'van')),
    price_per_km FLOAT NOT NULL,
    price_per_hour FLOAT NOT NULL,
    capacity INTEGER NOT NULL,
    total_cars INTEGER NOT NULL,
    available_cars INTEGER NOT NULL,
    amenities JSON DEFAULT '[]',
    rating FLOAT DEFAULT 0 CHECK (rating >= 0 AND rating <= 5),
    phone VARCHAR(15),
    email VARCHAR(254),
    image VARCHAR(100),
    created_at DATETIME AUTO_CURRENT_TIMESTAMP,
    updated_at DATETIME AUTO_UPDATE_CURRENT_TIMESTAMP
);
```

### Booking Table
```sql
CREATE TABLE api_booking (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    booking_type VARCHAR(20) NOT NULL CHECK (booking_type IN ('hotel', 'cab', 'destination')),
    hotel_id INTEGER,
    cab_id INTEGER,
    destination_id INTEGER,
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    number_of_guests INTEGER NOT NULL,
    number_of_rooms INTEGER,
    total_price FLOAT NOT NULL,
    payment_status VARCHAR(20) DEFAULT 'pending' CHECK (payment_status IN ('pending', 'completed', 'failed')),
    booking_status VARCHAR(20) DEFAULT 'confirmed' CHECK (booking_status IN ('confirmed', 'cancelled', 'completed')),
    booking_date DATETIME AUTO_CURRENT_TIMESTAMP,
    created_at DATETIME AUTO_CURRENT_TIMESTAMP,
    updated_at DATETIME AUTO_UPDATE_CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES auth_user(id),
    FOREIGN KEY (hotel_id) REFERENCES api_hotel(id),
    FOREIGN KEY (cab_id) REFERENCES api_cab(id),
    FOREIGN KEY (destination_id) REFERENCES api_destination(id)
);
```

### Contact Table
```sql
CREATE TABLE api_contact (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(254) NOT NULL,
    phone VARCHAR(15),
    subject VARCHAR(200) NOT NULL,
    message LONGTEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'new' CHECK (status IN ('new', 'read', 'resolved')),
    created_at DATETIME AUTO_CURRENT_TIMESTAMP,
    updated_at DATETIME AUTO_UPDATE_CURRENT_TIMESTAMP
);
```

---

## Current Sample Data

### Destinations
1. **Agra** - Uttar Pradesh, India | Rating: 4.8 | Cost: ₹3,000/day
2. **Jaipur** - Rajasthan, India | Rating: 4.6 | Cost: ₹2,500/day
3. **Goa** - Goa, India | Rating: 4.7 | Cost: ₹2,000/day
4. **Kerala** - Kerala, India | Rating: 4.8 | Cost: ₹2,500/day
5. **Ladakh** - Ladakh, India | Rating: 4.9 | Cost: ₹3,500/day
6. **Varanasi** - Uttar Pradesh, India | Rating: 4.5 | Cost: ₹1,500/day

### Hotels
- **Taj View Hotel** - Agra | ₹5,000/night | 50 rooms
- **Jaipur Palace Hotel** - Jaipur | ₹4,000/night | 40 rooms
- **Goa Beach Resort** - Goa | ₹3,500/night | 60 rooms
- **Kerala Backwaters Resort** - Kerala | ₹4,500/night | 35 rooms
- **Ladakh Mountain Lodge** - Ladakh | ₹3,000/night | 25 rooms

### Cabs
- **TourCabs** - Economy | ₹5/km, ₹30/hr | 4 seats
- **Premium Rides** - Premium | ₹8/km, ₹50/hr | 5 seats
- **Luxury Transport** - Luxury | ₹12/km, ₹80/hr | 4 seats
- **Group Tours** - Van | ₹6/km, ₹40/hr | 8-12 seats

---

## Query Examples

### Find hotels in a destination
```python
hotels = Hotel.objects.filter(destination__name='Agra')
```

### Get user's bookings
```python
bookings = Booking.objects.filter(user=request.user)
```

### Search destinations by name
```python
results = Destination.objects.filter(name__icontains='Agra')
```

### Find available cabs
```python
cabs = Cab.objects.filter(available_cars__gt=0)
```

### Get contacts with status='new'
```python
new_contacts = Contact.objects.filter(status='new')
```

---

## Indexes

Recommended indexes for performance:
- `Destination.name` - For search queries
- `Hotel.destination_id` - For foreign key lookups
- `Hotel.name` - For search queries
- `Booking.user_id` - For user-specific queries
- `Booking.booking_status` - For filtering
- `Contact.status` - For filtering
- `Contact.created_at` - For date sorting

---

## Data Validation

### Destination
- `name`: 1-100 characters, unique
- `description`: Required, any text length
- `rating`: Float between 0 and 5

### Hotel
- `name`: 1-100 characters
- `price_per_night`: Positive integer
- `available_rooms`: Must be ≤ total_rooms
- `rating`: Float between 0 and 5

### Cab
- `company_name`: 1-100 characters
- `vehicle_type`: Must be in ['economy', 'premium', 'luxury', 'van']
- `capacity`: Positive integer (1-15)
- `price_per_km`: Positive float
- `rating`: Float between 0 and 5

### Booking
- `check_in_date` < `check_out_date`
- `number_of_guests`: Positive integer
- `total_price`: Positive float
- `payment_status`: Must be in ['pending', 'completed', 'failed']
- `booking_status`: Must be in ['confirmed', 'cancelled', 'completed']

### Contact
- `email`: Valid email format
- `phone`: Valid phone format (optional)
- `status`: Must be in ['new', 'read', 'resolved']

---

