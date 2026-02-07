const Destination = require('../models/Destination');

// Get all destinations
exports.getAllDestinations = async (req, res) => {
  try {
    const destinations = await Destination.find();
    res.status(200).json({ destinations });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// Get destination by ID
exports.getDestinationById = async (req, res) => {
  try {
    const destination = await Destination.findById(req.params.id);
    if (!destination) {
      return res.status(404).json({ message: 'Destination not found' });
    }
    res.status(200).json({ destination });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// Get destination by name
exports.searchDestination = async (req, res) => {
  try {
    const { name } = req.query;
    if (!name) {
      return res.status(400).json({ message: 'Please provide a destination name' });
    }

    const destination = await Destination.findOne({
      name: new RegExp(name, 'i'),
    });

    if (!destination) {
      return res.status(404).json({ message: 'Destination not found' });
    }

    res.status(200).json({ destination });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// Create destination (Admin)
exports.createDestination = async (req, res) => {
  try {
    const { name, description, image, location, bestTimeToVisit, attractions } = req.body;

    const destination = new Destination({
      name,
      description,
      image,
      location,
      bestTimeToVisit,
      attractions,
    });

    await destination.save();
    res.status(201).json({ message: 'Destination created', destination });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// Update destination
exports.updateDestination = async (req, res) => {
  try {
    let destination = await Destination.findById(req.params.id);
    if (!destination) {
      return res.status(404).json({ message: 'Destination not found' });
    }

    destination = await Destination.findByIdAndUpdate(req.params.id, req.body, {
      new: true,
      runValidators: true,
    });

    res.status(200).json({ message: 'Destination updated', destination });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// Delete destination
exports.deleteDestination = async (req, res) => {
  try {
    const destination = await Destination.findByIdAndDelete(req.params.id);
    if (!destination) {
      return res.status(404).json({ message: 'Destination not found' });
    }
    res.status(200).json({ message: 'Destination deleted' });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};
