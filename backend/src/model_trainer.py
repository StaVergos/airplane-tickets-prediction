import io
import joblib
import logging
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

from src.minio import MinioClient
from src.config import FILENAME, MODEL_FILENAME
from src.data_loader import stream_airline_csv_to_minio

logger = logging.getLogger(__name__)


def train_and_store_model():
    stream_airline_csv_to_minio()
    client = MinioClient()
    if not client.bucket_exists():
        raise RuntimeError("MinIO bucket does not exist.")

    csv_file = client.get_fileobj_in_memory(FILENAME)
    if csv_file is None:
        raise FileNotFoundError(f"{FILENAME} not found in bucket")

    df = pd.read_csv(csv_file)
    df = df.drop_duplicates()
    df.columns = df.columns.str.strip().str.lower()
    logger.info(f"Columns in dataset: {df.columns.tolist()}")

    df = df.rename(
        columns={
            "originairportid": "Origin",
            "destairportid": "Dest",
        }
    )

    raw_features = ["Origin", "Dest"]
    missing = [c for c in raw_features if c not in df.columns]
    if missing:
        raise KeyError(f"Missing required columns in data for modeling: {missing}")

    X = df[raw_features]
    y = df["average_fare"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), raw_features),
        ],
        remainder="drop",
    )

    pipeline = Pipeline(
        steps=[
            ("preproc", preprocessor),
            ("model", RandomForestRegressor(random_state=42, n_jobs=-1)),
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    pipeline.fit(X_train, y_train)

    preds = pipeline.predict(X_test)
    mse = mean_squared_error(y_test, preds)
    r2 = r2_score(y_test, preds)
    logger.info(f"Model performance: MSE={mse:.4f}, R²={r2:.4f}")

    buf = io.BytesIO()
    joblib.dump(pipeline, buf)
    buf.seek(0)
    client.upload_fileobj(buf, MODEL_FILENAME)
    logger.info(f"Pipeline saved as {MODEL_FILENAME}")

    return {
        "model_filename": MODEL_FILENAME,
        "mse": mse,
        "r2": r2,
    }
