const Cab = require('../models/Cab');

// Get all cabs
exports.getAllCabs = async (req, res) => {
  try {
    const cabs = await Cab.find();
    res.status(200).json({ cabs });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// Get cab by ID
exports.getCabById = async (req, res) => {
  try {
    const cab = await Cab.findById(req.params.id);
    if (!cab) {
      return res.status(404).json({ message: 'Cab not found' });
    }
    res.status(200).json({ cab });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// Filter cabs by vehicle type
exports.filterCabs = async (req, res) => {
  try {
    const { vehicleType, minPrice, maxPrice } = req.query;
    const filter = {};

    if (vehicleType) {
      filter.vehicleType = vehicleType;
    }
    if (minPrice || maxPrice) {
      filter.pricePerKm = {};
      if (minPrice) filter.pricePerKm.$gte = minPrice;
      if (maxPrice) filter.pricePerKm.$lte = maxPrice;
    }

    const cabs = await Cab.find(filter);
    res.status(200).json({ cabs });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// Create cab (Admin)
exports.createCab = async (req, res) => {
  try {
    const { companyName, vehicleType, pricePerKm, pricePerHour, capacity, description, contact } = req.body;

    const cab = new Cab({
      companyName,
      vehicleType,
      pricePerKm,
      pricePerHour,
      capacity,
      description,
      contact,
    });

    await cab.save();
    res.status(201).json({ message: 'Cab created', cab });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// Update cab
exports.updateCab = async (req, res) => {
  try {
    let cab = await Cab.findById(req.params.id);
    if (!cab) {
      return res.status(404).json({ message: 'Cab not found' });
    }

    cab = await Cab.findByIdAndUpdate(req.params.id, req.body, {
      new: true,
      runValidators: true,
    });

    res.status(200).json({ message: 'Cab updated', cab });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// Delete cab
exports.deleteCab = async (req, res) => {
  try {
    const cab = await Cab.findByIdAndDelete(req.params.id);
    if (!cab) {
      return res.status(404).json({ message: 'Cab not found' });
    }
    res.status(200).json({ message: 'Cab deleted' });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};
