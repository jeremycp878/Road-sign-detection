const mongoose = require('mongoose');

const detectionSchema = new mongoose.Schema({
  sign: String,
  confidence: Number,
  latitude: Number,
  longitude: Number,
  timestamp: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Detection', detectionSchema);