# Airplane Tickets Prediction

This project predicts airplane ticket prices using machine learning. It aims to help users estimate future ticket costs based on historical data and various features.

## Features

- Data preprocessing and feature engineering
- Model training and evaluation
- Price prediction for new queries

## Workflow

![Workflow Diagram](docs/graph.png)

## Installation

```bash
git clone https://github.com/yourusername/airplane-tickets-prediction.git
cd airplane-tickets-prediction
pip install -r requirements.txt
```

## Usage

1. Download and install Docker.
2. Build the docker image:
    ```bash
    docker compose build --no-cache
    ```
3. Run the images:
    ```bash
    docker compose up -d
    ```

## Project Structure

### Backend

- `src/config` - Constants and secrets management
- `src/model_trainer` - Source code for preprocessing, modeling, and prediction
- `src/data_loader` - Handler of downloading dataset, transforming it and saving it into the store.
- `src/minio` - Blob store service
- `main` - FastAPI app and endpoints

## Contributing

Contributions are welcome! Please open issues or submit pull requests.

## License

This project is licensed under the MIT License.