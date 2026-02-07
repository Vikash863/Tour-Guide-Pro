const express = require('express');
const router = express.Router();
const auth = require('../middleware/auth');
const {
  getUserBookings,
  getBookingById,
  createBooking,
  updateBooking,
  cancelBooking,
} = require('../controllers/bookingController');

router.get('/', auth, getUserBookings);
router.get('/:id', auth, getBookingById);
router.post('/', auth, createBooking);
router.put('/:id', auth, updateBooking);
router.delete('/:id', auth, cancelBooking);

module.exports = router;
