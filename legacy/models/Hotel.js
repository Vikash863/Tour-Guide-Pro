const mongoose = require('mongoose');

const hotelSchema = new mongoose.Schema({
  name: { type: String, required: true },
  location: { type: String, required: true },
  destination: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Destination',
  },
  description: String,
  image: String,
  pricePerNight: { type: Number, required: true },
  rating: { type: Number, default: 0, min: 0, max: 5 },
  amenities: [String],
  rooms: {
    available: Number,
    total: Number,
  },
  contact: {
    phone: String,
    email: String,
  },
  createdAt: { type: Date, default: Date.now },
});

module.exports = mongoose.model('Hotel', hotelSchema);
