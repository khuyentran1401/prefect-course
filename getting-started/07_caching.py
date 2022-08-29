import pandas as pd

# Imports for loading configuration
from omegaconf import DictConfig
from hydra import compose, initialize
from prefect import flow, task  
import gdown 
from prefect.tasks import task_input_hash
from datetime import timedelta

@task 
def load_config():
    with initialize(version_base=None, config_path="../config"):
        config = compose(config_name="main")
    return config

@task
def get_data(config: DictConfig):
    gdown.download(config.data.url, config.data.raw, quiet=False)
    return pd.read_csv(config.data.raw)

@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1)) 
def fill_missing_description(data: pd.DataFrame):
    data["Description"] = data["Description"].fillna("")
    return data

@task 
def get_desc_length(data: pd.DataFrame):
    data["desc_length"] = data["Description"].str.len()
    return data

@flow
def process_data():
    config = load_config()
    data = get_data(config)
    na_processed = fill_missing_description(data)
    feature_added = get_desc_length(na_processed)


if __name__ == "__main__":
    process_data()