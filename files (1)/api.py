"""
api.py

Membungkus predict_trend() (buatan tim ML) jadi layanan HTTP kecil,
supaya bisa dipanggil dari backend Express (Node.js) lewat HTTP,
tanpa perlu Express menjalankan Python secara langsung.

Cara pakai:
    pip install fastapi uvicorn prophet pandas
    uvicorn api:app --reload --port 8001

Setelah jalan, coba buka di browser atau curl:
    http://localhost:8001/health
    http://localhost:8001/prediksi-tren?n_hari=7
"""

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
    """
    Endpoint ini cocok dengan yang dipanggil backend Express
    (controllers/mlcontroller.js): POST, body {"n_hari": <angka>}.
    """
    try:
        hasil = predict_trend(payload.n_hari)
    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail="Model belum ditemukan. Pastikan models/prophet_model.json ada di folder yang benar.",
        )
    return {"n_hari": payload.n_hari, "data": hasil}
