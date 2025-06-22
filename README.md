# Airplane Tickets Prediction

Predict future airplane ticket prices using machine learning. This project helps users estimate ticket costs based on historical data and relevant features.

## Features

- Automated data preprocessing and feature engineering
- Robust model training and evaluation pipeline
- Real-time price prediction for user queries

## Tech Stack

### Backend

- **FastAPI**  
    Serves as the backend framework, providing high-performance RESTful API endpoints for serving ML models and data operations. FastAPI is chosen for being an async Python framework, having an automatic OpenAPI documentation, and providing a seamless integration with Python-based ML workflows.

- **Scikit-learn**  
    Utilized for machine learning tasks, specifically employing the Random Forest Regressor algorithm. The project uses Scikit-learn's pipelines for streamlined data preprocessing, feature engineering, model training, and evaluation.

- **MinIO**  
    Acts as an S3/Azure blob alternative object storage solution for managing datasets and model artifacts. MinIO enables efficient storage and retrieval of large files, such as datasets downloaded from Kaggle and trained model binaries.

### Frontend

- **React**  
    The user interface is built with React, using TypeScript for type safety and maintainability.

- **Shadcn UI & Tailwind CSS**  
    UI components are styled using Shadcn UI and Tailwind CSS, providing a modern, responsive, and customizable design system.

### DevOps & Infrastructure

- **Docker**  
    The entire application stack is containerized with Docker, ensuring consistent development and deployment environments across different systems.

- **Docker Compose**  
    Used to orchestrate multi-container setups, simplifying the process of running the backend, frontend, and MinIO services together.

### Data & Integrations

- **Kaggle API**  
    Integrates with the Kaggle API to automate dataset downloads, streamlining the data acquisition process for model training.

## Getting Started

### Prerequisites

1. **Docker**: Ensure Docker is installed. [Installation Guide](https://www.docker.com/get-started/)
2. **Kaggle API Key**: Download your Kaggle API key. [Instructions](https://www.kaggle.com/docs/api#:~:text=In%20order%20to%20use%20the%20Kaggle%E2%80%99s%20public%20API%2C%20you%20must%20first%20authenticate%20using%20an%20API%20token.%20Go%20to%20the%20%27Account%27%20tab%20of%20your%20user%20profile%20and%20select%20%27Create%20New%20Token%27.%20This%20will%20trigger%20the%20download%20of%20kaggle.json%2C%20a%20file%20containing%20your%20API%20credentials.)
3. **Environment Variables**: Copy `.env.example` to `.env` in the `backend` directory and add your Kaggle credentials.

### Installation

```bash
git clone git@github.com:StaVergos/airplane-tickets-prediction.git
cd airplane-tickets-prediction
```

### Usage

1. **Build Docker images:**
    ```bash
    docker compose build --no-cache
    ```
2. **Start the services:**
    ```bash
    docker compose up -d
    ```

## Project Structure

### Backend

- `src/config/` — Configuration, constants, and secrets
- `src/model_trainer/` — Data preprocessing, model training, and prediction logic
- `src/data_loader/` — Dataset download, transformation, and storage
- `src/minio/` — Blob storage integration
- `main/` — FastAPI application and API endpoints

### Frontend

- `src/App.tsx` — Main React application
- `src/components/AirportDropdown.tsx` — Airport selection dropdown component

## Workflow

![Workflow Diagram](docs/graph.png)


## Project Overview

This project delivers an end-to-end solution for predicting airplane ticket prices using machine learning. It uses historical flight data and a variety of relevant features such as departure/arrival airports, dates, and airline carriers. The system enables users to estimate future ticket costs with a high degree of accuracy. The backend, implemented using FastAPI and Scikit-learn, automates the entire machine learning workflow, from data ingestion and preprocessing to model training, evaluation, and real-time inference. The integration with MinIO ensures scalable and reliable storage of large datasets and model artifacts, while the Kaggle API streamlines data acquisition.

On the frontend, a React application provides an intuitive interface for users to input their travel details and receive instant price predictions. The use of Shadcn UI and Tailwind CSS ensures a responsive and visually appealing user experience. The entire stack is containerized with Docker and orchestrated via Docker Compose, making it easy to deploy and manage across different environments.


## License

This project is licensed under the MIT License.