import os
import sys
import requests
import zipfile
import pandas as pd

from src.tsp.logging.logger import logging
from src.tsp.exception.exception import CustomException
from src.tsp.entity.config_entity import DataIngestionConfig


class DataIngestion:
    def __init__(self, config=DataIngestionConfig) -> None:
        self.config = config
       

    def download_data(self, url, download_dir):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                logging.info('Request response successfully')
                os.makedirs(os.path.dirname(download_dir), exist_ok=True)
                
                with open(download_dir, 'wb') as file:
                    file.write(response.content)
                logging.info('Data downloaded successfully')
            else:
                logging.error('Error in response')
                raise CustomException("Failed to download data. Status code: " + str(response.status_code), sys)

        except Exception as e:
            logging.error(f'Error in download data: {str(e)}')
            raise CustomException(e, sys)
        
    def extract_data(self, download_dir, unzip_dir):
        try:
            os.makedirs(unzip_dir, exist_ok=True)

            with zipfile.ZipFile(download_dir, 'r') as zip_ref:
                zip_ref.extractall(unzip_dir)

            logging.info('Data extraction completed')
        except Exception as e:
            logging.error(f'Error in data extraction: {str(e)}')
            raise CustomException(e, sys)

    def initiate_data_ingestion(self)-> pd.DataFrame:
        try:
            url = self.config.url
            download_dir = self.config.local_dir
            unzip_dir = self.config.unzip_dir
            

            self.download_data(url=url, download_dir=download_dir)
            self.extract_data(download_dir=download_dir, unzip_dir=unzip_dir)

            
            

        except Exception as e:
            logging.error(f'Error in data ingestion: {str(e)}')
            raise CustomException(e, sys)