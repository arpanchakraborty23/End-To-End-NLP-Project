import os,sys

from src.tsp.logging.logger import logging
from src.tsp.exception.exception import CustomException
from src.tsp.component.Model_trainer import ModelTrainer
from src.tsp.config.config_manager import ConfiManager

class ModelTrainerPipline:
    def __init__(self) -> None:
       pass
     
    def TransformationPipline(self):
        try:
            model_trainer_config_manager=ConfiManager()

            model_trainer_config=model_trainer_config_manager.get_model_config()
            model_trainer=ModelTrainer(config=model_trainer_config)
            model_trainer.initiate_model_trainer()
        except Exception as e:
                logging.info(f'Error in download Data {str(e)}')
                raise CustomException(e,sys)
    
if __name__=='__main__':
    try:
        logging.info(f'<<<<<<<<<<<<<<<<<<<<< Model Trainer Started >>>>>>>>>>>>>>>>>>>>>>>')
        object=ModelTrainerPipline()
        object.TransformationPipline()
        logging.info(f'<<<<<<<<<<<<<<<<<<<<<<< Model Trainer completed >>>>>>>>>>>>>>>>>>')
    except Exception as e:
            logging.info(f' Error occured {str(e)}')
            raise e