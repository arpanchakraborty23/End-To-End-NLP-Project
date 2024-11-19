import os,sys

from src.tsp.logging.logger import logging
from src.tsp.exception.exception import CustomException
from src.tsp.component.model_evaluation import ModelEvaluation
from src.tsp.config.config_manager import ConfiManager

class ModelEvaluationPipline:
    def __init__(self) -> None:
       pass
     
    def TransformationPipline(self):
        try:
            model_evaluation_config_manager=ConfiManager()

            model_evaluation_config=model_evaluation_config_manager.get_model_eval_config()
            model_evaluation=ModelEvaluation(config=model_evaluation_config)
            model_evaluation.evaluate()
        except Exception as e:
                logging.info(f'Error in download Data {str(e)}')
                raise CustomException(e,sys)
    
if __name__=='__main__':
    try:
        logging.info(f'<<<<<<<<<<<<<<<<<<<<< Model Evaluation Started >>>>>>>>>>>>>>>>>>>>>>>')
        object=ModelEvaluationPipline()
        object.TransformationPipline()
        logging.info(f'<<<<<<<<<<<<<<<<<<<<<<< Model Evaluation completed >>>>>>>>>>>>>>>>>>')
    except Exception as e:
            logging.info(f' Error occured {str(e)}')
            raise e