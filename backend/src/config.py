import dotenv

import logging
import os

dotenv.load_dotenv()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

KAGGLE_USERNAME = os.getenv("KAGGLE_USERNAME")
KAGGLE_KEY = os.getenv("KAGGLE_KEY")
FILENAME = "Airline_Market_Fare_Prediction_Data/MarketFarePredictionData.csv"
MODEL_FILENAME = "random_forest_regressor_model.pkl"
MINIO_ENDPOINT = "http://minio:9000"
ACCESS_KEY = "minioadmin"
SECRET_KEY = "minioadmin"
BUCKET_NAME = "airplane-tickets"
REGION_NAME = "us-east-1"
SIGNATURE_VERSION = "s3v4"
DATASET_URL = "https://www.kaggle.com/api/v1/datasets/download/orvile/airline-market-fare-prediction-data"


logging.info(
    f"Configuration loaded successfully with {'KAGGLE_USERNAME' if KAGGLE_USERNAME else 'KAGGLE_KEY' if KAGGLE_KEY else 'no credentials'}"
)
