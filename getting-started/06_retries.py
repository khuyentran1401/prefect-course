import gdown
import pandas as pd
from hydra import compose, initialize
# Imports for loading configuration
from omegaconf import DictConfig
from prefect import flow, task


@task
def load_config():
    with initialize(version_base=None, config_path="../config"):
        config = compose(config_name="main")
    return config


@task(retries=3, retry_delay_seconds=5)
def get_data(config: DictConfig):
    gdown.download(config.data.url, config.data.raw, quiet=False)
    return pd.read_csv(config.data.raw)


@task
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
