from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from predict import predict_trend

app = FastAPI(title="Layanan Prediksi Tren UKM")


class PrediksiRequest(BaseModel):
    n_hari: int = Field(7, ge=1, le=90, description="Jumlah hari ke depan yang diprediksi, 1-90")


@app.get("/health")
def health():
    """Buat cek cepat apakah layanan ini hidup, dipanggil Express saat startup kalau perlu."""
    return {"status": "ok"}


@app.get("/prediksi-tren")
def get_prediksi_tren(
    n_hari: int = Query(7, ge=1, le=90, description="Jumlah hari ke depan yang diprediksi, 1-90")
):
    try:
        hasil = predict_trend(n_hari)
    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail="Model belum ditemukan. Pastikan models/prophet_model.json ada di folder yang benar.",
        )
    return {"n_hari": n_hari, "data": hasil}


@app.post("/api/ml/predict-trend")
def post_prediksi_tren(payload: PrediksiRequest):
    try:
        hasil = predict_trend(payload.n_hari)
    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail="Model belum ditemukan. Pastikan models/prophet_model.json ada di folder yang benar.",
        )
    return {"n_hari": payload.n_hari, "data": hasil}