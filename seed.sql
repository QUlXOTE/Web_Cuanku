-- seed.sql
--
-- Data contoh buat testing lewat Postman, biar tabel enggak kosong.
-- Cara pakai: mysql -u root -p db_cuanku < seed.sql

INSERT INTO users (nama_UMKM, email, password) VALUES
('Kedai Kopi Melati', 'test@cuanku.com', 'password123');

INSERT INTO produk (nama_produk, sisa_stok, harga_beli, harga_jual) VALUES
('Kopi Susu', 40, 6000, 12000),
('Es Teh', 55, 2000, 5000),
('Roti Bakar', 20, 5000, 10000);

INSERT INTO transaksi (jenis_transaksi, kategori, jumlah, keterangan, tanggal) VALUES
('Pemasukan', 'Penjualan Produk', 180000, 'Penjualan harian', '2026-09-08'),
('Pemasukan', 'Penjualan Produk', 220000, 'Penjualan harian', '2026-09-09'),
('Pengeluaran', 'Biaya Bahan Baku', 90000, 'Beli bahan baku kopi', '2026-09-08'),
('Pengeluaran', 'Biaya Operasional', 50000, 'Listrik dan air', '2026-09-09');
