const mongoose = require('mongoose');
const dotenv = require('dotenv');

dotenv.config();

const Destination = require('./models/Destination');
const Hotel = require('./models/Hotel');
const Cab = require('./models/Cab');

async function seedDatabase() {
  try {
    await mongoose.connect(process.env.MONGODB_URI, {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    });

    console.log('Connected to MongoDB');

    // Clear existing data
    await Destination.deleteMany({});
    await Hotel.deleteMany({});
    await Cab.deleteMany({});

    // Seed Destinations
    const destinations = await Destination.insertMany([
      {
        name: 'Agra',
        description: 'Home to the iconic Taj Mahal, one of the Seven Wonders of the World.',
        location: {
          city: 'Agra',
          state: 'Uttar Pradesh',
          country: 'India',
        },
        bestTimeToVisit: 'October to March',
        attractions: ['Taj Mahal', 'Agra Fort', 'Mehtab Bagh'],
        averageCost: 5000,
        rating: 4.8,
      },
      {
        name: 'Jaipur',
        description: 'The Pink City known for its vibrant culture and historical architecture.',
        location: {
          city: 'Jaipur',
          state: 'Rajasthan',
          country: 'India',
        },
        bestTimeToVisit: 'September to March',
        attractions: ['City Palace', 'Jantar Mantar', 'Hawa Mahal'],
        averageCost: 4000,
        rating: 4.6,
      },
      {
        name: 'Goa',
        description: 'Tropical paradise with beautiful beaches and Portuguese architecture.',
        location: {
          city: 'Goa',
          state: 'Goa',
          country: 'India',
        },
        bestTimeToVisit: 'November to February',
        attractions: ['Baga Beach', 'Fort Aguada', 'Basilica of Bom Jesus'],
        averageCost: 6000,
        rating: 4.7,
      },
      {
        name: 'Kerala',
        description: 'God\'s own country with lush backwaters and tropical beauty.',
        location: {
          city: 'Kochi',
          state: 'Kerala',
          country: 'India',
        },
        bestTimeToVisit: 'September to February',
        attractions: ['Backwaters', 'Chinese Fishing Nets', 'Fort Kochi'],
        averageCost: 5500,
        rating: 4.8,
      },
      {
        name: 'Ladakh',
        description: 'High-altitude desert with breathtaking mountain scenery.',
        location: {
          city: 'Leh',
          state: 'Ladakh',
          country: 'India',
        },
        bestTimeToVisit: 'June to September',
        attractions: ['Pangong Lake', 'Nubra Valley', 'Khardung La'],
        averageCost: 7000,
        rating: 4.9,
      },
      {
        name: 'Varanasi',
        description: 'Spiritual capital of India with sacred ghats along the Ganges.',
        location: {
          city: 'Varanasi',
          state: 'Uttar Pradesh',
          country: 'India',
        },
        bestTimeToVisit: 'October to March',
        attractions: ['Kashi Vishwanath Temple', 'Ganges Ghats', 'Sarnath'],
        averageCost: 3500,
        rating: 4.5,
      },
    ]);

    console.log(`${destinations.length} destinations seeded`);

    // Seed Hotels
    const hotels = await Hotel.insertMany([
      {
        name: 'Taj View Hotel',
        location: 'Agra',
        destination: destinations[0]._id,
        description: 'Luxury hotel with direct view of Taj Mahal',
        pricePerNight: 8000,
        rating: 4.7,
        amenities: ['WiFi', 'AC', 'Restaurant', 'Pool'],
        rooms: { available: 15, total: 30 },
        contact: { phone: '+91-9876543210', email: 'info@tajview.com' },
      },
      {
        name: 'Jaipur Palace Hotel',
        location: 'Jaipur',
        destination: destinations[1]._id,
        description: 'Royal experience in the heart of Pink City',
        pricePerNight: 6000,
        rating: 4.5,
        amenities: ['WiFi', 'Spa', 'Gym', 'Restaurant'],
        rooms: { available: 20, total: 40 },
        contact: { phone: '+91-9876543211', email: 'info@jaipurpalace.com' },
      },
      {
        name: 'Goa Beach Resort',
        location: 'Goa',
        destination: destinations[2]._id,
        description: 'Beach resort with water sports and evening entertainment',
        pricePerNight: 5500,
        rating: 4.6,
        amenities: ['Beach Access', 'Pool', 'Restaurant', 'Bar'],
        rooms: { available: 25, total: 50 },
        contact: { phone: '+91-9876543212', email: 'info@goabeach.com' },
      },
      {
        name: 'Kerala Backwaters Resort',
        location: 'Kochi',
        destination: destinations[3]._id,
        description: 'Serene resort overlooking the backwaters',
        pricePerNight: 7000,
        rating: 4.8,
        amenities: ['Backwater View', 'Boat Tours', 'Restaurant', 'Spa'],
        rooms: { available: 18, total: 35 },
        contact: { phone: '+91-9876543213', email: 'info@keralaresort.com' },
      },
      {
        name: 'Ladakh Mountain Lodge',
        location: 'Leh',
        destination: destinations[4]._id,
        description: 'Cozy lodge with stunning mountain views',
        pricePerNight: 4500,
        rating: 4.4,
        amenities: ['Mountain View', 'Heater', 'Restaurant', 'Tour Assistance'],
        rooms: { available: 12, total: 25 },
        contact: { phone: '+91-9876543214', email: 'info@ladakhlodge.com' },
      },
    ]);

    console.log(`${hotels.length} hotels seeded`);

    // Seed Cabs
    const cabs = await Cab.insertMany([
      {
        companyName: 'TourCabs',
        vehicleType: 'economy',
        pricePerKm: 8,
        pricePerHour: 400,
        capacity: 4,
        rating: 4.5,
        contact: { phone: '+91-9876543220', email: 'info@tourcabs.com' },
        availableCars: 25,
        description: 'Affordable cab service for budget travelers',
      },
      {
        companyName: 'Premium Rides',
        vehicleType: 'premium',
        pricePerKm: 15,
        pricePerHour: 800,
        capacity: 5,
        rating: 4.7,
        contact: { phone: '+91-9876543221', email: 'info@premiumrides.com' },
        availableCars: 15,
        description: 'Comfortable premium cabs for leisure travel',
      },
      {
        companyName: 'Luxury Transport',
        vehicleType: 'luxury',
        pricePerKm: 25,
        pricePerHour: 1500,
        capacity: 4,
        rating: 4.9,
        contact: { phone: '+91-9876543222', email: 'info@luxurytransport.com' },
        availableCars: 8,
        description: 'Ultra-luxury cars for premium experience',
      },
      {
        companyName: 'Group Tours',
        vehicleType: 'van',
        pricePerKm: 20,
        pricePerHour: 1200,
        capacity: 12,
        rating: 4.6,
        contact: { phone: '+91-9876543223', email: 'info@grouptours.com' },
        availableCars: 10,
        description: 'Van service for group tours and family trips',
      },
    ]);

    console.log(`${cabs.length} cabs seeded`);

    console.log('Database seeded successfully!');
    process.exit(0);
  } catch (error) {
    console.error('Error seeding database:', error);
    process.exit(1);
  }
}

seedDatabase();
