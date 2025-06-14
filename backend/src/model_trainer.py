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


logger = logging.getLogger(__name__)


def train_and_store_model():
    client = MinioClient()
    if not client.bucket_exists():
        raise RuntimeError("MinIO bucket does not exist.")

    csv_file = client.get_fileobj_in_memory(FILENAME)
    df = pd.read_csv(csv_file)
    df = df.drop_duplicates().reset_index(drop=True)
    df.columns = df.columns.str.strip().str.lower()

    df = df.rename(
        columns={
            "airport_1": "origin",
            "airport_2": "dest",
            "quarter": "month",
            "fare": "fare",
        }
    )

    if "year" in df.columns:
        df = df[df["year"] >= 2020]

    df = df[["origin", "dest", "month", "fare"]].dropna()

    X = df[["origin", "dest", "month"]]
    y = df["fare"]

    preproc = ColumnTransformer(
        transformers=[
            (
                "ohe_airports",
                OneHotEncoder(handle_unknown="ignore"),
                ["origin", "dest"],
            ),
        ],
        remainder="passthrough",
    )

    pipeline = Pipeline(
        [
            ("preproc", preproc),
            ("rfr", RandomForestRegressor(random_state=42, n_jobs=-1)),
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

    return {"model_filename": MODEL_FILENAME, "mse": mse, "r2": r2}
