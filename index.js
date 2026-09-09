const express = require('express');
const cors = require('cors');
require('dotenv').config();

// memanggil semua file yg sudah dibuat
const dashboardRoutes = require('./routes/dashboardRoutes');
const authRoutes = require('./routes/authRoutes');
const transaksiRoutes = require('./routes/transaksiRoutes');

const app = express();

app.use(cors());
app.use(express.json());

// mendaftarkan semua jalur api untuk frontend
app.use('/api/dashboard', dashboardRoutes);
app.use('/api/auth', authRoutes);
app.use('/api/transaksi', transaksiRoutes);

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server jalan di http://localhost:${PORT}`);
});