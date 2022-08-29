import pandas as pd

# Imports for loading configuration
from omegaconf import DictConfig
from hydra import compose, initialize
from prefect import flow, task  
import os  
import gdown 

@task(name="Load config") 
def load_config():
    with initialize(version_base=None, config_path="../config"):
        config = compose(config_name="main")
    return config

@task(name="Get data")  
def get_data(config: DictConfig):
    gdown.download(config.data.url, config.data.raw, quiet=False)
    return pd.read_csv(config.data.raw)

@task(name="Fill missing descriptions")
def fill_missing_description(data: pd.DataFrame):
    data["Description"] = data["Description"].fillna("")
    return data

@task(name="Get description length")
def get_desc_length(data: pd.DataFrame):
    data["desc_length"] = data["Description"].str.len()
    return data

# @flow(name="Process data", version="experimental")
@flow(name="Process data", version=os.getenv("GIT_COMMIT_SHA"))
def process_data():
    config = load_config()
    data = get_data(config)
    na_processed = fill_missing_description(data)
    feature_added = get_desc_length(na_processed)


if __name__ == "__main__":
    process_data()