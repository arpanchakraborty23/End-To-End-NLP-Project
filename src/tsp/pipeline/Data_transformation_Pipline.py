import os,sys

from src.tsp.logging.logger import logging
from src.tsp.exception.exception import CustomException
from src.tsp.component.Data_Transformation import DataTransformation
from src.tsp.config.config_manager import ConfiManager

class DataTransformationPipline:
    def __init__(self) -> None:
       pass
     
    def TransformationPipline(self):
        try:
            data_Transformation_config_manager=ConfiManager()

            data_Transformation_config=data_Transformation_config_manager.get_data_transformation_config()
            data_Transformation=DataTransformation(config=data_Transformation_config)
            data_Transformation.initiate_data_transformation()
        except Exception as e:
                logging.info(f'Error in download Data {str(e)}')
                raise CustomException(e,sys)
    
if __name__=='__main__':
    try:
        logging.info(f'<<<<<<<<<<<<<<<<<<<<< Data Transformation Started >>>>>>>>>>>>>>>>>>>>>>>')
        object=DataTransformationPipline()
        object.TransformationPipline()
        logging.info(f'<<<<<<<<<<<<<<<<<<<<<<< Data Transformation completed >>>>>>>>>>>>>>>>>>')
    except Exception as e:
            logging.info(f' Error occured {str(e)}')
            raise e