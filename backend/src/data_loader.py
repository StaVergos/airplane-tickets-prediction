import io
import logging
import zipfile

import pandas as pd
import requests
from src.config import DATASET_URL, KAGGLE_KEY, KAGGLE_USERNAME
from src.minio import MinioClient

logging.basicConfig(level=logging.INFO)


def stream_airline_csv_to_minio() -> str:
    user = KAGGLE_USERNAME
    key = KAGGLE_KEY
    if not user or not key:
        raise EnvironmentError("Missing Kaggle credentials")

    logging.info(f"Using Kaggle credentials: {user} : {key}")
    client = MinioClient()
    client.create_bucket()

    resp = requests.get(DATASET_URL, auth=(user, key), stream=True)
    resp.raise_for_status()
    zip_buf = io.BytesIO(resp.content)

    with zipfile.ZipFile(zip_buf) as z:
        csv_name = next((n for n in z.namelist() if n.lower().endswith(".csv")), None)
        if not csv_name:
            raise RuntimeError("No CSV file found in the downloaded dataset.")

        csv_bytes = z.read(csv_name)

    client.upload_fileobj(io.BytesIO(csv_bytes), csv_name)
    logging.info(f"Uploaded original CSV to MinIO: {csv_name}")

    df = pd.read_csv(io.BytesIO(csv_bytes), low_memory=False)
    df = df[df["Year"] >= 2020]
    unique_airports = sorted(df["airport_1"].unique())
    airports_json = pd.Series(unique_airports).to_json()

    client.upload_fileobj(
        io.BytesIO(airports_json.encode("utf-8")), "unique_airports.json"
    )
    logging.info("Uploaded unique airports JSON to MinIO")

    return csv_name
