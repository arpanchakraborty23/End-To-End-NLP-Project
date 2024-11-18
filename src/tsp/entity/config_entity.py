from dataclasses import dataclass
from pathlib import Path

@dataclass
class DataIngestionConfig:
    dir:Path
    url:str
    local_dir:Path
    unzip_dir:Path

@dataclass
class DataTransformationConfig:
    dir: Path
    data_path:Path
    tokenizer:str
    transform_data:Path
    