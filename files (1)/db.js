require('dotenv').config();
const mysql = require('mysql2');

const pool = mysql.createPool({
    host: process.env.DB_HOST || 'localhost',
    user: process.env.DB_USER || 'root',
    password: process.env.DB_PASSWORD || '',
    database: process.env.DB_NAME || 'db_cuanku',
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0
});

const db = pool.promise();

pool.getConnection((err, connection) => {
    if (err) {
        console.error('Koneksi database GAGAL:', err.message);
    } else {
        console.log('Koneksi ke database BERHASIL');
        connection.release();

    }
});

module.exports = db;