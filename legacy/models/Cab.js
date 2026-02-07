const mongoose = require('mongoose');

const cabSchema = new mongoose.Schema({
  companyName: {
    type: String,
    required: [true, 'Please provide company name'],
  },
  vehicleType: {
    type: String,
    enum: ['economy', 'premium', 'luxury', 'van'],
    required: true,
  },
  pricePerKm: {
    type: Number,
    required: true,
  },
  pricePerHour: {
    type: Number,
    required: true,
  },
  capacity: {
    type: Number,
    required: true,
  },
  image: String,
  rating: {
    type: Number,
    default: 0,
    min: 0,
    max: 5,
  },
  contact: {
    phone: String,
    email: String,
  },
  availableCars: Number,
  description: String,
  createdAt: {
    type: Date,
    default: Date.now,
  },
});

module.exports = mongoose.model('Cab', cabSchema);
