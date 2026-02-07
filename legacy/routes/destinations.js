const express = require('express');
const router = express.Router();
const {
  getAllDestinations,
  getDestinationById,
  searchDestination,
  createDestination,
  updateDestination,
  deleteDestination,
} = require('../controllers/destinationController');

router.get('/', getAllDestinations);
router.get('/search', searchDestination);
router.get('/:id', getDestinationById);
router.post('/', createDestination);
router.put('/:id', updateDestination);
router.delete('/:id', deleteDestination);

module.exports = router;
