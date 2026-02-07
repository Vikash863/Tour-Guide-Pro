const express = require('express');
const router = express.Router();
const {
  submitContactForm,
  getAllContacts,
  getContactById,
  markAsRead,
  deleteContact,
} = require('../controllers/contactController');

router.post('/', submitContactForm);
router.get('/', getAllContacts);
router.get('/:id', getContactById);
router.put('/:id/read', markAsRead);
router.delete('/:id', deleteContact);

module.exports = router;
