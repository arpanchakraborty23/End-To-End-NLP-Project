import os
import sys
from transformers import AutoTokenizer
from datasets import load_from_disk
from nltk.tokenize import sent_tokenize
import nltk
# nltk.download('punkt')

from src.tsp.logging.logger import logging
from src.tsp.exception.exception import CustomException
from src.tsp.entity.config_entity import DataTransformationConfig


class DataTransformation:
    def __init__(self, config: DataTransformationConfig) -> None:
        self.config = config
        self.tokenizer = AutoTokenizer.from_pretrained(config.tokenizer)
        logging.info("Tokenizer initialized successfully.")

    def read_data(self, data_path: str):
        try:
            dataset = load_from_disk(dataset_path=data_path)
            logging.info("Dataset loaded successfully.")
            return dataset
        except Exception as e:
            logging.error(f"Error loading dataset: {str(e)}")
            raise CustomException(e, sys)

    def convert_examples_to_features(self, example_batch: dict) -> dict:
        try:
            input_encodings = self.tokenizer(
                example_batch["dialogue"],
                max_length=1024,
                truncation=True,
                padding="max_length",  #  uniform length for all sequences
            )

            # Tokenize target/summary
            target_encodings = self.tokenizer(
                example_batch["summary"],
                max_length=128,
                truncation=True,
                padding="max_length",
                return_tensors=None,  #  outputs are lists, not tensors
            )

            return {
                "input_ids": input_encodings["input_ids"],
                "attention_mask": input_encodings["attention_mask"],
                "labels": target_encodings["input_ids"],
            }
        except KeyError as e:
            logging.error(f"Missing required keys in dataset: {str(e)}")
            raise CustomException(e, sys)

    def initiate_data_transformation(self) -> dict:
        try:
            # Load data
            logging.info("Starting data transformation process.")
            dataset = self.read_data(self.config.data_path)

            # Tokenize and convert to features
            logging.info("Tokenizing dataset...")
            dataset_pt = dataset.map(self.convert_examples_to_features, batched=True)
            logging.info("Tokenization completed.")

            # Save transformed data
            save_path = os.path.join(self.config.transform_data, "transform")
            dataset_pt.save_to_disk(save_path)
            logging.info(f"Transformed data saved successfully at {save_path}.")

            return save_path

        except Exception as e:
            logging.error(f"Error in data transformation: {str(e)}")
            raise CustomException(e, sys)
