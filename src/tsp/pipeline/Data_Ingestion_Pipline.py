import os,sys

from src.tsp.logging.logger import logging
from src.tsp.exception.exception import CustomException
from src.tsp.component.Data_Ingestion import DataIngestion
from src.tsp.config.config_manager import ConfiManager

class DataIngestionPipline:
    def __init__(self) -> None:
       pass
     
    def IngestionPipline(self):
        try:
            data_ingestion_config_manager=ConfiManager()
            data_ingestion_config=data_ingestion_config_manager.get_data_ingestion_config()
            data_ingestion=DataIngestion(config=data_ingestion_config)
            data_ingestion.initiate_data_ingestion()
        except Exception as e:
                logging.info(f'Error in download Data {str(e)}')
                raise CustomException(e,sys)
    
if __name__=='__main__':
    try:
        logging.info(f'<<<<<<<<<<<<<<<<<<<<< Data Ingestion Started >>>>>>>>>>>>>>>>>>>>>>>')
        object=DataIngestionPipline()
        object.IngestionPipline()
        logging.info(f'<<<<<<<<<<<<<<<<<<<<<<< Data Ingestion completed >>>>>>>>>>>>>>>>>>')
    except Exception as e:
            logging.info(f' Error occured {str(e)}')
            raise e