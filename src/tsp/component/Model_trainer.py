import os
import sys
import torch
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    Trainer,
    TrainingArguments,
    DataCollatorForSeq2Seq,
)
from datasets import load_from_disk

from src.tsp.logging.logger import logging
from src.tsp.exception.exception import CustomException
from src.tsp.entity.config_entity import ModelTrainerConfig


class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig) -> None:
        self.config = config
        self._validate_config()
        logging.info("ModelTrainer initialized successfully.")

    def _validate_config(self):
        required_attrs = [
            "model",
            "data_path",
            "dir",
            "num_train_epochs",
            "per_device_train_batch_size",
        ]
        missing = [attr for attr in required_attrs if not getattr(self.config, attr, None)]
        if missing:
            raise ValueError(f"Missing required config attributes: {', '.join(missing)}")

    def read_data(self, data_path: str):
        try:
            dataset = load_from_disk(data_path)
            logging.info(f"Dataset loaded successfully from {data_path}.")
            return dataset
        except Exception as e:
            logging.error(f"Error loading dataset: {str(e)}")
            raise CustomException(e, sys)

    def train(self, dataset):
        try:
            # Check for device availability
            device = "cuda" if torch.cuda.is_available() else "cpu"
            logging.info(f"Training on device: {device}")

            # Load tokenizer and model
            tokenizer = AutoTokenizer.from_pretrained(self.config.model)
            pegasus_model = AutoModelForSeq2SeqLM.from_pretrained(self.config.model).to(device)

            # Data collator for seq2seq models
            data_collator = DataCollatorForSeq2Seq(tokenizer=tokenizer, model=pegasus_model)

            # Define training arguments
            training_args = TrainingArguments(
            output_dir=self.config.dir, 
            num_train_epochs=1, 
            warmup_steps=500,
            per_device_train_batch_size=1, 
            per_device_eval_batch_size=1,
            weight_decay=0.01, 
            logging_steps=10,
            evaluation_strategy='steps', 
            eval_steps=500, 
            save_steps=1e6,
            gradient_accumulation_steps=16
            ) 

            logging.info(f"Training arguments: {training_args}")

            # Initialize the trainer
            trainer = Trainer(
                model=pegasus_model,
                args=training_args,
                tokenizer=tokenizer,
                data_collator=data_collator,
                train_dataset=dataset["train"],
                eval_dataset=dataset["validation"],
            )

            # Train the model
            logging.info("Starting model training...")
            trainer.train()

            # Save the model and tokenizer
            model_path = os.path.join(self.config.dir, "pegasus_model")
            tokenizer_path = os.path.join(self.config.dir, "tokenizer")

            pegasus_model.save_pretrained(model_path)
            logging.info(f"Model saved successfully at {model_path}.")

            tokenizer.save_pretrained(tokenizer_path)
            logging.info("Training completed successfully.")

            return pegasus_model, tokenizer
        except Exception as e:
            logging.error(f"Error during training: {str(e)}")
            raise CustomException(e, sys)

    def initiate_model_trainer(self):
        try:
            logging.info("Starting the model training process...")

            # Load dataset
            dataset = self.read_data(self.config.data_path)

            # Train the model
            self.train(dataset)

        except Exception as e:
            logging.error(f"Error in model trainer: {str(e)}")
            raise CustomException(e, sys)
