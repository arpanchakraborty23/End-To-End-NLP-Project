import os
import sys
import torch
from transformers import Phi3Config,Phi3Model,AutoTokenizer,Seq2SeqTrainer
from transformers import Trainer,TrainingArguments
from transformers import DataCollatorForSeq2Seq
from datasets import load_from_disk


from src.tsp.logging.logger import logging
from src.tsp.exception.exception import CustomException
from src.tsp.entity.config_entity import ModelTrainerConfig

class ModelTrainer:
    def __init__(self,config:ModelTrainerConfig) -> None:
        self.config=config
    
    def read_data(self,data):
        data=load_from_disk(dataset_path=data)
        logging.info('data load successfully')
        return data
    
    def train(self,data):
        try:

            device='cuda' if torch.cuda.is_available() else 'cpu'
            tokenizer=AutoTokenizer.from_pretrained(self.config.model)
            phi_model=Phi3Model.from_pretrained(self.config.model).to(device)
            seq2seq_data_collector=DataCollatorForSeq2Seq(tokenizer=tokenizer,model=phi_model)

            # define trainng params
            traing_args=TrainingArguments(
                output_dir=self.config.dir,
                num_train_epochs=self.config.num_train_epochs,
                warmup_steps=self.config.warmup_steps,
                weight_decay=self.config.weight_decay,
                per_device_eval_batch_size=self.config.per_device_train_batch_size,
                per_device_train_batch_size=self.config.per_device_train_batch_size,
                logging_steps=self.config.logging_steps,
                eval_steps=self.config.eval_steps,
                save_steps=self.config.save_steps,
                gradient_accumulation_steps=self.config.gradient_accumulation_steps,
               
            )
            trainer=Trainer(
                model=phi_model,
                args=traing_args,
                tokenizer=tokenizer,
                data_collator=seq2seq_data_collector,
                train_dataset=data['test'],
                eval_dataset=data['validation']
            )
            trainer.train()
            logging.info(' Traning completed')
            return phi_model,tokenizer
        except Exception as e:
            logging.info(f' erorr in  trainer {str(e)}')
            raise CustomException(e,sys)


    def initate_model_trainer(self):
        try:
            data_path=self.config.data_path
            # load data
            dataset=self.read_data(data=data_path)

            # training
            phi_model,tokenizer=self.train(data=dataset)
            # save model
            phi_model.save_pretrained(os.path.join(self.config.dir,'Phi_model'))
            logging.info('phi model save successfully')
            # save tokenizer
            tokenizer.save_pretrained(os.path.join(self.config.dir,'tokenizer'))
            logging.info('tokenizer save successfully')

        except Exception as e:
            logging.info(f' erorr in model trainer {str(e)}')
            raise CustomException(e,sys)