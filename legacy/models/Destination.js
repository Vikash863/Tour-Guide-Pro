const mongoose = require('mongoose');

const destinationSchema = new mongoose.Schema({
  name: {
    type: String,
    required: [true, 'Please provide destination name'],
    unique: true,
    trim: true,
  },
  description: {
    type: String,
    required: true,
  },
  image: {
    type: String,
    default: '',
  },
  location: {
    city: String,
    state: String,
    country: String,
  },
  bestTimeToVisit: String,
  attractions: [String],
  weather: {
    temperature: String,
    condition: String,
  },
  averageCost: Number,
  rating: {
    type: Number,
    default: 0,
    min: 0,
    max: 5,
  },
  createdAt: {
    type: Date,
    default: Date.now,
  },
});

module.exports = mongoose.model('Destination', destinationSchema);
