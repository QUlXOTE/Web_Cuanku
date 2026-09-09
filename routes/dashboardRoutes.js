const express = require('express');
const router = express.Router();
const { getPredictionTrend } = require('../controllers/mlcontroller');

router.post('/predict-revenue', getPredictionTrend);

module.exports = router;