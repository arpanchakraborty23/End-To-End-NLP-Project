import yaml
import os
import json
import pickle


from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any




@ensure_annotations
def read_yaml(file_path:Path):
    try:
        with open(file_path) as f:
            file=yaml.safe_load(f)
            logging.info(f'Yaml file {file_path} created')
        return ConfigBox(file)
    except Exception as e:
        logging.info(f' ymal file is empty: {str(e)}')
        raise e
    
@ensure_annotations   
def create_dir(file_path:list,verbose=True):
    try:
        for path in file_path:
            os.makedirs(path,exist_ok=True)
            if verbose:
                logging.info(f"created directory at: {path}")    
    except Exception as e:
        raise e 
    
    
def save_obj(file_path,obj):
    with open(file_path,'wb') as f:
        pickle.dump(obj,f)
  
def load_obj(file_path):
    with open(file_path,'rb') as f:
        data=pickle.load(f)

    return data

def save_json(data,filename):
  
        with open(filename,'w') as j:
            json.dump(data,j,indent=4)

@ensure_annotations
def load_bin(path:Path):
    data=joblib.load(path)
    logging.info(f'binary file load at {path}')
    return data
        