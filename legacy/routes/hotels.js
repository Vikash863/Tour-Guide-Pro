const express = require('express');
const router = express.Router();
const {
  getAllHotels,
  searchHotels,
  getHotelById,
  createHotel,
  updateHotel,
  deleteHotel,
} = require('../controllers/hotelController');

router.get('/', getAllHotels);
router.get('/search', searchHotels);
router.get('/:id', getHotelById);
router.post('/', createHotel);
router.put('/:id', updateHotel);
router.delete('/:id', deleteHotel);

module.exports = router;
