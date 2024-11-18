import os
import sys
import nltk
from nltk.tokenize import sent_tokenize
from transformers import AutoTokenizer,BartTokenizer
from datasets import load_from_disk
nltk.download('punkt')

from src.tsp.logging.logger import logging
from src.tsp.exception.exception import CustomException
from src.tsp.entity.config_entity import DataTransformationConfig

class DataTransformation:
    def __init__(self,config:DataTransformationConfig) -> None:
        self.config=config
        self.tokenizer=AutoTokenizer.from_pretrained(self.config.tokenizer)

    
    def read_data(self,data):
        data=load_from_disk(dataset_path=data)
        logging.info('data load successfully')
        return data
    
    def convert_examples_to_features(self,example_batch):
       input_embadding=self.tokenizer(example_batch['dialogue'], max_length=1024 ,truncation=True)

       with self.tokenizer.as_target_tokenizer():
           target_embaddings=self.tokenizer(example_batch['summary'],max_length=1024,truncation= True)

       return {
            'input_id': input_embadding['input_ids'],
            'attention_mask': input_embadding['attention_mask'],
            'labels': target_embaddings['input_ids']
        }

    def initate_data_transformation(self)->dict:
        try:
            data_path=self.config.data_path
            # read data
            dataset=self.read_data(data_path)

            dataset_pt=dataset.map(self.convert_examples_to_features,batched= True)
            logging.info('data map completed')
            print(type(dataset_pt))

            dataset_pt.save_to_disk(os.path.join(self.config.transform_data,'transform'))
            logging.info('Transform data save successfully')
        except Exception as e:
            logging.info(f' erorr in data transfom {str(e)}')
            raise CustomException(e,sys)