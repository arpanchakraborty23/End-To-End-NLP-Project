import os
import sys
import requests
import zipfile

from textsummarizer.logging.logger import logging
from textsummarizer.exception.exception import CustomException
from textsummarizer.entity.config_entity import DataIngestionConfig


class DataIngestion:
    def __init__(self, config=DataIngestionConfig) -> None:
        self.config = config
        print('*' * 40, 'Data Ingestion', '*' * 40)

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

    def initiate_data_ingestion(self):
        try:
            url = self.config.dir
            download_dir = self.config.local_dir
            unzip_dir = self.config.unzip_dir

            self.download_data(url=url, download_dir=download_dir)
            self.extract_data(download_dir=download_dir, unzip_dir=unzip_dir)

            logging.info('Data Ingestion Completed')
            print('*' * 40, 'Data Ingestion Completed', '*' * 40)

        except Exception as e:
            logging.error(f'Error in data ingestion: {str(e)}')
            raise CustomException(e, sys)
