import io
import zipfile
import requests
import logging

from src.config import KAGGLE_USERNAME, KAGGLE_KEY, DATASET_URL
from src.minio import MinioClient

logging.basicConfig(level=logging.INFO)


def stream_airline_csv_to_minio() -> str:
    user = KAGGLE_USERNAME
    key = KAGGLE_KEY
    if not user or not key:
        raise EnvironmentError("Missing KAGGLE_USERNAME or KAGGLE_KEY in environment")

    client = MinioClient()
    client.create_bucket()

    dataset_url = DATASET_URL
    resp = requests.get(dataset_url, auth=(user, key), stream=True)
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
                    return name

    raise RuntimeError("No CSV file found in the downloaded dataset.")
