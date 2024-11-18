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


@dataclass
class ModelTrainerConfig:
    dir:Path
    data_path: Path
    model: str
    num_train_epochs: int
    warmup_steps: int
    per_device_train_batch_size: int
    weight_decay: float
    logging_steps: int
    eval_steps: int
    save_steps: float
    gradient_accumulation_steps: int
    