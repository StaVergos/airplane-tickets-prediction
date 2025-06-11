import logging
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.config import MODEL_FILENAME
from src.minio import MinioClient
from src.model_trainer import train_and_store_model

logging.basicConfig(level=logging.INFO)
app = FastAPI()
model = None


class FareFeatures(BaseModel):
    Year: int
    Quarter: int
    Month: int
    Origin: int  # airport ID
    Dest: int  # airport ID
    Is_Holiday: int  # 0 or 1


@app.on_event("startup")
def load_model():
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

    df = pd.DataFrame([{"Origin": features.Origin, "Dest": features.Dest}])
    preds = model.predict(df)
    return {"predictions": preds.tolist()}
