const Booking = require('../models/Booking');

// Get all bookings for user
exports.getUserBookings = async (req, res) => {
  try {
    const bookings = await Booking.find({ userId: req.userId })
      .populate('hotelId')
      .populate('cabId')
      .populate('destinationId');

    res.status(200).json({ bookings });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// Get booking by ID
exports.getBookingById = async (req, res) => {
  try {
    const booking = await Booking.findById(req.params.id)
      .populate('hotelId')
      .populate('cabId')
      .populate('destinationId');

    if (!booking) {
      return res.status(404).json({ message: 'Booking not found' });
    }

    // Check if user owns this booking
    if (booking.userId.toString() !== req.userId && req.userRole !== 'admin') {
      return res.status(403).json({ message: 'Not authorized' });
    }

    res.status(200).json({ booking });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// Create booking
exports.createBooking = async (req, res) => {
  try {
    const { bookingType, hotelId, cabId, destinationId, checkInDate, checkOutDate, numberOfGuests, numberOfRooms, totalPrice } = req.body;

    const booking = new Booking({
      userId: req.userId,
      bookingType,
      hotelId: bookingType === 'hotel' ? hotelId : undefined,
      cabId: bookingType === 'cab' ? cabId : undefined,
      destinationId: bookingType === 'destination' ? destinationId : undefined,
      checkInDate,
      checkOutDate,
      numberOfGuests,
      numberOfRooms,
      totalPrice,
    });

    await booking.save();
    res.status(201).json({ message: 'Booking created successfully', booking });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// Update booking
exports.updateBooking = async (req, res) => {
  try {
    let booking = await Booking.findById(req.params.id);
    if (!booking) {
      return res.status(404).json({ message: 'Booking not found' });
    }

    if (booking.userId.toString() !== req.userId && req.userRole !== 'admin') {
      return res.status(403).json({ message: 'Not authorized' });
    }

    booking = await Booking.findByIdAndUpdate(req.params.id, req.body, {
      new: true,
      runValidators: true,
    });

    res.status(200).json({ message: 'Booking updated', booking });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// Cancel booking
exports.cancelBooking = async (req, res) => {
  try {
    const booking = await Booking.findById(req.params.id);
    if (!booking) {
      return res.status(404).json({ message: 'Booking not found' });
    }

    if (booking.userId.toString() !== req.userId && req.userRole !== 'admin') {
      return res.status(403).json({ message: 'Not authorized' });
    }

    booking.bookingStatus = 'cancelled';
    await booking.save();

    res.status(200).json({ message: 'Booking cancelled', booking });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};
