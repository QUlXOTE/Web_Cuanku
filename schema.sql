-- schema.sql
--
-- Dibuat berdasarkan kolom yang benar-benar dipakai di
-- controllers/authcontroller.js dan controllers/transaksicontroller.js,
-- supaya bisa langsung dipakai tanpa ubah kode backend.
--
-- Cara pakai:
--   mysql -u root -p db_cuanku < schema.sql

CREATE TABLE IF NOT EXISTS users (
    id_user      INT AUTO_INCREMENT PRIMARY KEY,
    nama_UMKM    VARCHAR(100) NOT NULL,
    email        VARCHAR(100) NOT NULL UNIQUE,
    password     VARCHAR(255) NOT NULL,
    dibuat_pada  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS produk (
    id_produk    INT AUTO_INCREMENT PRIMARY KEY,
    nama_produk  VARCHAR(100) NOT NULL,
    sisa_stok    INT NOT NULL DEFAULT 0,
    harga_beli   DECIMAL(12, 2) NOT NULL,
    harga_jual   DECIMAL(12, 2) NOT NULL,
    dibuat_pada  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS transaksi (
    id_transaksi     INT AUTO_INCREMENT PRIMARY KEY,
    jenis_transaksi  ENUM('Pemasukan', 'Pengeluaran') NOT NULL,
    kategori         VARCHAR(50) NOT NULL,
    jumlah           DECIMAL(12, 2) NOT NULL,
    keterangan       VARCHAR(255),
    tanggal          DATE NOT NULL,
    dibuat_pada      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_transaksi_tanggal ON transaksi (tanggal);
CREATE INDEX idx_transaksi_kategori ON transaksi (kategori);
