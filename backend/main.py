import logging
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.config import MODEL_FILENAME
from src.minio import MinioClient
from src.model_trainer import train_and_store_model
from src.data_loader import stream_airline_csv_to_minio

logging.basicConfig(level=logging.INFO)
app = FastAPI()
model = None


class FareFeatures(BaseModel):
    origin: str
    dest: str
    month: int


@app.on_event("startup")
def load_model():
    stream_airline_csv_to_minio()
    train_and_store_model()

    client = MinioClient()
    buf = client.get_fileobj_in_memory(MODEL_FILENAME)
    global model
    model = joblib.load(buf)
    logging.info("Model pipeline loaded successfully.")


@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/predict")
def predict_fare(features: FareFeatures):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded.")

    # build DataFrame with exactly the three columns the pipeline expects:
    df = pd.DataFrame([features.dict()], columns=["origin", "dest", "month"])

    try:
        prediction = model.predict(df)[0]
        return {"fare": float(prediction)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
