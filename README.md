# End-to-End Text Summarization Project
This project implements an end-to-end pipeline for text summarization using state-of-the-art NLP models. The system includes data ingestion, data transform model training, evaluation, and a FastAPI-based frontend for real-time summarization.

## Key Features
End-to-end modular architecture.
Pretrained models like Pegasus for high-quality summarization.
Real-time API using FastAPI.
Easily configurable through YAML files.
Comprehensive evaluation using metrics like ROUGE.
Future Enhancements
Integrate additional pre-trained models (e.g., BART, GPT).
Add support for multilingual text summarization.
Deploy the FastAPI app with Docker and Kubernetes.
Contributors


## Workflows
The project is divided into the following major components and workflows:

1. Configurations
config/config.yaml: Defines project-specific configurations such as paths, model parameters, and batch sizes.
params.yaml: Stores hyperparameters like learning rate, epochs, etc., used during model training.
2. Configuration Management
config entity: Contains Python classes defining structured configurations for different stages of the pipeline.
config manager: Dynamically manages and loads configurations from YAML files.
3. Components
The project consists of three main components:

### Data Ingestion:
Loads raw datasets from specified sources.
Validates and stores data for transformation.

### Data Transformation:
Tokenizes and preprocesses text data (e.g., truncation, padding).
Splits data into training, validation, and testing subsets.
### Model Training:
Fine-tunes pre-trained Seq2Seq models (e.g., Pegasus, T5).
###  Evaluates model performance using ROUGE and other metrics.
###  Pipelines
Training Pipeline:
Executes the complete training workflow: ingestion → transformation → model training → evaluation.
Prediction Pipeline:
Generates summaries for new input text using the trained model.
###  Frontend UI
Web API (FastAPI):
A RESTful interface for text summarization.
Allows users to input text and retrieve summarized results in real time.
Includes Swagger documentation for ease of use.

## Setup Instructions
### 1. Clone the Repository
```bash
git clone <repository_url>
cd text-summarization-project
```
### 2. Install Dependencies
```bash

pip install -r requirements.txt
```
### 3. Prepare Configurations
```
Update config/config.yaml and params.yaml with paths and hyperparameters.
```
### 4. Run Training Pipeline
```bash
python main.py
```
### 5. Start FastAPI Application
``` bash
uvicorn src.frontend.app:app --reload
Access the API at http://127.0.0.1:8000/docs for Swagger documentation.
```








