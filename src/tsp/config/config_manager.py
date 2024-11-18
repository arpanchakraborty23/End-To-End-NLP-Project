import os
import sys

from src.tsp.utils.main_utils import read_yaml,create_dir
from src.tsp.logging.logger import logging
from src.tsp.exception.exception import CustomException
from src.tsp.entity.config_entity import DataIngestionConfig,DataTransformationConfig,ModelTrainerConfig
from src.tsp.constants import *

class ConfiManager:
    def __init__(self,config_file_path=Config_file_path,
                 params_file_path=Params_file_path) -> None:
        self.config=read_yaml(config_file_path)
        self.params=read_yaml(params_file_path)

        create_dir([self.config.artifacts_root])

    def get_data_ingestion_config(self):
        try:
            config = self.config.Data_Ingestion
          
            data_ingestion_config = DataIngestionConfig(
                dir=config.dir,
                url=config.url,
                local_dir=config.local_dir,
                unzip_dir=config.unzip_dir
            )
            
            return data_ingestion_config
        except Exception as e:
            logging.info(f'Error in Data Ingestion Config {str(e)}')
            raise CustomException(e,sys)

    def get_data_transformation_config(self):
        try:
            config=self.config.Data_Transformation
            data_transformation_config=DataTransformationConfig(
                dir=config.dir,
                data_path=config.data_path,
                tokenizer=config.tokenizer
            )
            return data_transformation_config
        
        except Exception as e:
            logging.info(f' erorr in data transfom config {str(e)}')
            raise CustomException(e,sys)
        
    def get_model_config(self):
        try:
            config=self.config.Model_Trainer
            params=self.params.TraningArguments

            model_train_config=ModelTrainerConfig(
                dir=config.dir,
                data_path=config.data_path,
                model=config.model,
                num_train_epochs = params.num_train_epochs,
                warmup_steps = params.warmup_steps,
                per_device_train_batch_size = params.per_device_train_batch_size,
                weight_decay = params.weight_decay,
                logging_steps = params.logging_steps,
                eval_steps = params.eval_steps,
                save_steps = params.save_steps,
                gradient_accumulation_steps = params.gradient_accumlation_steps
            )
            
            return model_train_config
        except Exception as e:
            logging.info(f' erorr in model train config {str(e)}')
            raise CustomException(e,sys)
    