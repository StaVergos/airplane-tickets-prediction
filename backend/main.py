import json
import logging

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.config import MODEL_FILENAME
from src.data_loader import stream_airline_csv_to_minio
from src.minio import MinioClient
from src.model_trainer import train_and_store_model

logging.basicConfig(level=logging.INFO)
client = MinioClient()
app = FastAPI()
model = None


class FareFeatures(BaseModel):
    origin: str
    dest: str
    month: int

    class Config:
        json_schema_extra = {"example": {"origin": "JFK", "dest": "LAX", "month": 6}}


class Airports(BaseModel):
    airports: list[str]

    class Config:
        json_schema_extra = {"example": {"airports": ["JFK", "LAX", "ORD", "DFW"]}}


@app.on_event("startup")
def load_model():
    stream_airline_csv_to_minio()
    train_and_store_model()
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

    df = pd.DataFrame([features.dict()], columns=["origin", "dest", "month"])

    try:
        prediction = model.predict(df)[0]
        return {"fare": float(prediction)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/airports", response_model=Airports)
def get_airports():
    try:
        buf = client.get_fileobj_in_memory("unique_airports.json")
        data = buf.read().decode("utf-8")
        if not data:
            raise HTTPException(status_code=404, detail="No airports data found.")
        # parse the JSON array string into a Python list
        airports_list = json.loads(data)
        return {"airports": airports_list}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
