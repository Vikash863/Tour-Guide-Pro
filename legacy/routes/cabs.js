const express = require('express');
const router = express.Router();
const {
  getAllCabs,
  getCabById,
  filterCabs,
  createCab,
  updateCab,
  deleteCab,
} = require('../controllers/cabController');

router.get('/', getAllCabs);
router.get('/filter', filterCabs);
router.get('/:id', getCabById);
router.post('/', createCab);
router.put('/:id', updateCab);
router.delete('/:id', deleteCab);

module.exports = router;
