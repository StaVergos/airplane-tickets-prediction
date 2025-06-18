import json
import logging

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.config import MODEL_FILENAME
from src.data_loader import stream_airline_csv_to_minio
from src.minio import MinioClient
from src.model_trainer import train_and_store_model

logging.basicConfig(level=logging.INFO)
client = MinioClient()
app = FastAPI()
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


model = None


class FareFeatures(BaseModel):
    origin: str
    dest: str
    month: int

    class Config:
        json_schema_extra = {"example": {"origin": "JFK", "dest": "LAX", "month": 6}}


class Airport(BaseModel):
    airport: str
    city: str

    class Config:
        json_schema_extra = {"example": {"airport": "JFK", "city": "New York"}}


class Airports(BaseModel):
    airports: list[Airport]

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


@app.get("/healthcheck")
def health_check():
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded.")
    return {"status": "ok", "model_loaded": True}


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
        airports_list = json.loads(data)
        return {"airports": airports_list}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
