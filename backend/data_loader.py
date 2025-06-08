import io
import os
import zipfile

import requests
from dotenv import load_dotenv
from minio import MinioClient


def stream_airline_csv_to_minio() -> str:
    load_dotenv()
    user = os.getenv("KAGGLE_USERNAME")
    
    key = os.getenv("KAGGLE_KEY")
    if not user or not key:
        raise EnvironmentError("Missing KAGGLE_USERNAME or KAGGLE_KEY in environment")

    client = MinioClient()
    client.create_bucket()

    dataset = "orvile/airline-market-fare-prediction-data"
    url = f"https://www.kaggle.com/api/v1/datasets/download/{dataset}"
    resp = requests.get(url, auth=(user, key), stream=True)
    resp.raise_for_status()

    buf = io.BytesIO()
    for chunk in resp.iter_content(chunk_size=4 * 1024 * 1024):
        buf.write(chunk)
    buf.seek(0)

    with zipfile.ZipFile(buf) as z:
        for name in z.namelist():
            if name.lower().endswith(".csv"):
                with z.open(name) as csvfile:
                    client.upload_fileobj(csvfile, name)
                    print(f"Uploaded '{name}' to bucket '{client.bucket_name}'.")
                    return name

    raise RuntimeError("No CSV file found in the downloaded dataset.")
