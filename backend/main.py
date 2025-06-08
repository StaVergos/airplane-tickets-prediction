from fastapi import FastAPI
from data_loader import stream_airline_csv_to_minio

app = FastAPI()


@app.get("/")
def root():
    return "Hey"


@app.get("/load-data")
def load_data():
    try:
        filename = stream_airline_csv_to_minio()
        return {"message": f"Data loaded successfully: {filename}"}
    except Exception as e:
        return {"error": str(e)}
