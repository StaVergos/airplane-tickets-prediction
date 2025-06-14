import dotenv

import os

dotenv.load_dotenv()


KAGGLE_USERNAME = os.getenv("KAGGLE_USERNAME")
KAGGLE_KEY = os.getenv("KAGGLE_KEY")
FILENAME = "US Airline Flight Routes and Fares 1993-2024.csv"
MODEL_FILENAME = "random_forest_regressor_model.pkl"
MINIO_ENDPOINT = "http://minio:9000"
ACCESS_KEY = "minioadmin"
SECRET_KEY = "minioadmin"
BUCKET_NAME = "airplane-tickets"
REGION_NAME = "us-east-1"
SIGNATURE_VERSION = "s3v4"
DATASET_URL = (
    "https://www.kaggle.com/api/v1/datasets/download/"
    "bhavikjikadara/us-airline-flight-routes-and-fares-1993-2024"
    "?datasetVersionNumber=1"
)
