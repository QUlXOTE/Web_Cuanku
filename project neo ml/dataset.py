import os
import pandas as pd
import numpy as np


SEED = 42                      
START_DATE = "2026-06-01"     
N_DAYS = 90                   
TREND_PER_DAY = 0.0035         
WEEKEND_MULTIPLIER = 1.4     
PROMO_DAYS = range(44, 46)     
PROMO_MULTIPLIER = 1.6
RESTOCK_EVERY_N_DAYS = 5      
OUTPUT_DIR = "data"

PRODUCTS = [
    {"produk_id": "P1", "nama_produk": "Kopi Susu",   "harga_beli": 6000, "harga_jual": 12000, "stok_awal": 220, "base_qty": 18},
    {"produk_id": "P2", "nama_produk": "Es Teh",      "harga_beli": 2000, "harga_jual": 5000,  "stok_awal": 260, "base_qty": 22},
    {"produk_id": "P3", "nama_produk": "Roti Bakar",  "harga_beli": 5000, "harga_jual": 10000, "stok_awal": 130, "base_qty": 10},
    {"produk_id": "P4", "nama_produk": "Nasi Goreng", "harga_beli": 8000, "harga_jual": 15000, "stok_awal": 150, "base_qty": 12},
    {"produk_id": "P5", "nama_produk": "Cireng",      "harga_beli": 3000, "harga_jual": 7000,  "stok_awal": 170, "base_qty": 14},
]


def generate():
    np.random.seed(SEED)
    dates = [pd.Timestamp(START_DATE) + pd.Timedelta(days=i) for i in range(N_DAYS)]
    stok_current = {p["produk_id"]: p["stok_awal"] for p in PRODUCTS}
    rows = []

    for i, date in enumerate(dates):
        weekday = date.weekday()  
        weekend_mult = WEEKEND_MULTIPLIER if weekday >= 5 else 1.0
        trend_mult = 1 + TREND_PER_DAY * i
        promo_mult = PROMO_MULTIPLIER if i in PROMO_DAYS else 1.0

        for p in PRODUCTS:
            noise = np.random.normal(0, 0.15)
            qty = p["base_qty"] * weekend_mult * trend_mult * promo_mult * (1 + noise)
            qty = max(0, round(qty))
            qty = min(qty, stok_current[p["produk_id"]])  # enggak bisa jual melebihi stok
            if qty > 0:
                stok_current[p["produk_id"]] -= qty
                rows.append({
                    "tanggal": date.strftime("%Y-%m-%d"),
                    "jenis": "Pemasukan",
                    "kategori": "Penjualan Produk",
                    "deskripsi": f"Penjualan {p['nama_produk']}",
                    "produk_id": p["produk_id"],
                    "jumlah_unit": qty,
                    "jumlah_rp": qty * p["harga_jual"],
                })

        if i % RESTOCK_EVERY_N_DAYS == 0 and i > 0:
            for p in PRODUCTS:
                restock_qty = round(p["base_qty"] * RESTOCK_EVERY_N_DAYS * np.random.uniform(0.95, 1.25))
                stok_current[p["produk_id"]] += restock_qty
                rows.append({
                    "tanggal": date.strftime("%Y-%m-%d"),
                    "jenis": "Pengeluaran",
                    "kategori": "Biaya Bahan Baku",
                    "deskripsi": f"Pembelian bahan baku {p['nama_produk']}",
                    "produk_id": p["produk_id"],
                    "jumlah_unit": restock_qty,
                    "jumlah_rp": restock_qty * p["harga_beli"],
                })

        op_cost = max(0, np.random.normal(50000, 8000))
        rows.append({
            "tanggal": date.strftime("%Y-%m-%d"),
            "jenis": "Pengeluaran",
            "kategori": "Biaya Operasional",
            "deskripsi": "Listrik, air, dan operasional harian",
            "produk_id": None,
            "jumlah_unit": None,
            "jumlah_rp": round(op_cost),
        })

      
        if date.day == 1:
            rows.append({
                "tanggal": date.strftime("%Y-%m-%d"),
                "jenis": "Pengeluaran",
                "kategori": "Lainnya",
                "deskripsi": "Sewa tempat bulanan",
                "produk_id": None,
                "jumlah_unit": None,
                "jumlah_rp": 1500000,
            })

    transaksi_df = pd.DataFrame(rows)
    produk_df = pd.DataFrame(PRODUCTS)[["produk_id", "nama_produk", "harga_beli", "harga_jual", "stok_awal"]]

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    transaksi_df.to_csv(os.path.join(OUTPUT_DIR, "transaksi.csv"), index=False)
    produk_df.to_csv(os.path.join(OUTPUT_DIR, "produk.csv"), index=False)

    print(f"Selesai. {len(transaksi_df)} baris transaksi disimpan di {OUTPUT_DIR}/transaksi.csv")
    print(f"Master {len(produk_df)} produk disimpan di {OUTPUT_DIR}/produk.csv")
    print(f"Rentang tanggal: {transaksi_df.tanggal.min()} sampai {transaksi_df.tanggal.max()}")


if __name__ == "__main__":
    generate()