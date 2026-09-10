from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT_DIR = Path(__file__).resolve().parent.parent
RAW_PATH = ROOT_DIR / "data" / "raw" / "transaksi.csv"
PROCESSED_PATH = ROOT_DIR / "data" / "processed" / "data_harian.csv"
REPORT_PATH = ROOT_DIR / "reports" / "eda_trend.png"


def load_transaksi(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["tanggal"])
    return df


def aggregate_pemasukan_harian(df: pd.DataFrame) -> pd.DataFrame:
    pemasukan = df[df["jenis"] == "Pemasukan"]
    harian = (
        pemasukan.groupby("tanggal")["jumlah_rp"]
        .sum()
        .rename("y")
        .reset_index()
        .rename(columns={"tanggal": "ds"})
    )


    full_range = pd.date_range(harian["ds"].min(), harian["ds"].max(), freq="D")
    harian = (
        harian.set_index("ds")
        .reindex(full_range)
        .fillna(0)
        .rename_axis("ds")
        .reset_index()
    )
    return harian


def print_ringkasan(harian: pd.DataFrame) -> None:
    print("Jumlah hari:", len(harian))
    print("Rentang tanggal:", harian["ds"].min().date(), "-", harian["ds"].max().date())
    print("Hari tanpa transaksi (y=0):", (harian["y"] == 0).sum())
    print()
    print("Statistik pendapatan harian (Rp):")
    print(harian["y"].describe().round(0))
    print()
    print("Rata-rata 7 hari terakhir vs 7 hari sebelumnya:")
    print("  7 hari terakhir :", round(harian["y"].tail(7).mean()))
    print("  7 hari sebelumnya:", round(harian["y"].tail(14).head(7).mean()))


def simpan_grafik(harian: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(10, 4))
    plt.plot(harian["ds"], harian["y"], label="Pendapatan harian")
    plt.plot(harian["ds"], harian["y"].rolling(7).mean(), label="Rata-rata 7 hari", linewidth=2)
    plt.title("Tren pemasukan harian")
    plt.xlabel("Tanggal")
    plt.ylabel("Rupiah")
    plt.legend()
    plt.tight_layout()
    plt.savefig(path)
    print(f"\nGrafik tren disimpan di {path}")


def main() -> None:
    df = load_transaksi(RAW_PATH)
    harian = aggregate_pemasukan_harian(df)

    print_ringkasan(harian)
    simpan_grafik(harian, REPORT_PATH)

    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    harian.to_csv(PROCESSED_PATH, index=False)
    print(f"Data harian siap pakai disimpan di {PROCESSED_PATH}")


if __name__ == "__main__":
    main()