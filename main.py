import sys
from src.tsp.logging.logger import logging
from src.tsp.exception.exception import CustomException
from src.tsp.config.config_manager import ConfiManager
from src.tsp.component.Data_Ingestion import DataIngestion



class TrainPipline:
    def __init__(self) -> None:
        pass

    def pipline(self):
        try:
            logging.info('<<<<<<<<<<<<<<<< Data_Ingestion >>>>>>>>>>>>>>>>>>')
            config=ConfiManager()
            data_ingestion_config=config.get_data_ingestion_config()
            data_ingestion=DataIngestion(config=data_ingestion_config)
            data_ingestion.initiate_data_ingestion()
            logging.info('<<<<<<<<<<<<<<<< Data_Ingestion_completed >>>>>>>>>>>>>>>>>>')

            
        except Exception as e:
            logging.info(f'Error cooured {str(e)}')
            raise CustomException(sys,e)   
        

if __name__ == '__main__':
    try:
        logging.info(f'********************Train Pipline**********************')
        obj = TrainPipline()
        obj.pipline()
        logging.info('******************** Train Pipline Completed **********************')
    except Exception as e:
        logging.exception(e)
        raise e      