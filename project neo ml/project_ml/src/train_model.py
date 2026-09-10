from pathlib import Path
import pandas as pd
from prophet import Prophet
from prophet.serialize import model_to_json

ROOT_DIR = Path(__file__).resolve().parent.parent
PROCESSED_PATH = ROOT_DIR / "data" / "processed" / "data_harian.csv"
MODEL_PATH = ROOT_DIR / "models" / "prophet_model.json"

TEST_DAYS = 14 


def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["ds"])
    return df


def split_train_test(df: pd.DataFrame, test_days: int):
    train = df.iloc[:-test_days].copy()
    test = df.iloc[-test_days:].copy()
    return train, test


def train_prophet(train: pd.DataFrame) -> Prophet:
    model = Prophet(
        weekly_seasonality=True,   
        yearly_seasonality=False, 
        daily_seasonality=False,
    )
    model.fit(train)
    return model


def evaluate(model: Prophet, test: pd.DataFrame) -> pd.DataFrame:
    future = model.make_future_dataframe(periods=len(test))
    forecast = model.predict(future)

    hasil = test.merge(forecast[["ds", "yhat"]], on="ds", how="left")
    hasil["selisih_absolut"] = (hasil["y"] - hasil["yhat"]).abs()
    hasil["persentase_error"] = hasil["selisih_absolut"] / hasil["y"].replace(0, pd.NA) * 100

    mae = hasil["selisih_absolut"].mean()
    mape = hasil["persentase_error"].mean()

    print("Hasil evaluasi pada", len(test), "hari terakhir (data yang disembunyikan dari training):")
    tampil = hasil[["ds", "y", "yhat", "selisih_absolut"]].copy()
    tampil[["y", "yhat", "selisih_absolut"]] = tampil[["y", "yhat", "selisih_absolut"]].round(0)
    print(tampil.to_string(index=False))
    print()
    print(f"MAE  (rata-rata selisih absolut) : Rp {mae:,.0f}")
    print(f"MAPE (rata-rata persentase error): {mape:.1f}%")
    return hasil


def save_model(model: Prophet, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        f.write(model_to_json(model))
    print(f"\nModel final disimpan di {path}")


def main() -> None:
    df = load_data(PROCESSED_PATH)
    train, test = split_train_test(df, TEST_DAYS)

    print(f"Data latih: {len(train)} hari, data uji: {len(test)} hari\n")

    model = train_prophet(train)
    evaluate(model, test)

    final_model = train_prophet(df)
    save_model(final_model, MODEL_PATH)


if __name__ == "__main__":
    main()