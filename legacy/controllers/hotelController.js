const Hotel = require('../models/Hotel');

// Get all hotels
exports.getAllHotels = async (req, res) => {
  try {
    const hotels = await Hotel.find().populate('destination');
    res.status(200).json({ hotels });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// Search hotels by location
exports.searchHotels = async (req, res) => {
  try {
    const { location } = req.query;
    if (!location) {
      return res.status(400).json({ message: 'Please provide a location' });
    }

    const hotels = await Hotel.find({
      location: new RegExp(location, 'i'),
    }).populate('destination');

    res.status(200).json({ hotels });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// Get hotel by ID
exports.getHotelById = async (req, res) => {
  try {
    const hotel = await Hotel.findById(req.params.id).populate('destination');
    if (!hotel) {
      return res.status(404).json({ message: 'Hotel not found' });
    }
    res.status(200).json({ hotel });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// Create hotel (Admin)
exports.createHotel = async (req, res) => {
  try {
    const { name, location, destination, description, image, pricePerNight, amenities, contact } = req.body;

    const hotel = new Hotel({
      name,
      location,
      destination,
      description,
      image,
      pricePerNight,
      amenities,
      contact,
    });

    await hotel.save();
    res.status(201).json({ message: 'Hotel created', hotel });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// Update hotel
exports.updateHotel = async (req, res) => {
  try {
    let hotel = await Hotel.findById(req.params.id);
    if (!hotel) {
      return res.status(404).json({ message: 'Hotel not found' });
    }

    hotel = await Hotel.findByIdAndUpdate(req.params.id, req.body, {
      new: true,
      runValidators: true,
    });

    res.status(200).json({ message: 'Hotel updated', hotel });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// Delete hotel
exports.deleteHotel = async (req, res) => {
  try {
    const hotel = await Hotel.findByIdAndDelete(req.params.id);
    if (!hotel) {
      return res.status(404).json({ message: 'Hotel not found' });
    }
    res.status(200).json({ message: 'Hotel deleted' });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};
