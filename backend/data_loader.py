import os
import io
import zipfile
import requests
from dotenv import load_dotenv


def stream_airline_csv_to_minio(minio) -> str:
    """
    Download the orvile/airline-market-fare-prediction-data zip from Kaggle
    into memory, extract its CSV, and upload that CSV to the configured
    MinIO bucket—without ever writing to disk.
    Returns the object name (i.e. the CSV filename) that was uploaded.
    """
    load_dotenv()
    user = os.getenv("KAGGLE_USERNAME")
    key = os.getenv("KAGGLE_KEY")
    if not user or not key:
        raise EnvironmentError("Missing KAGGLE_USERNAME or KAGGLE_KEY in environment")

    dataset = "orvile/airline-market-fare-prediction-data"
    url = f"https://www.kaggle.com/api/v1/datasets/download/{dataset}"
    resp = requests.get(url, auth=(user, key), stream=True)
    try:
        resp.raise_for_status()
    except Exception as e:
        code = getattr(e.response, "status_code", "?")
        raise RuntimeError(f"Kaggle download failed (HTTP {code})") from e

    buf = io.BytesIO()
    for chunk in resp.iter_content(chunk_size=4 * 1024 * 1024):
        buf.write(chunk)
    buf.seek(0)

    with zipfile.ZipFile(buf) as z:
        for name in z.namelist():
            if name.lower().endswith(".csv"):
                with z.open(name) as csvfile:
                    minio.s3.upload_fileobj(csvfile, minio.bucket_name, name)
                    print(f"Uploaded '{name}' to bucket '{minio.bucket_name}'.")
                    return name
