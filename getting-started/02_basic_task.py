import pandas as pd

# Imports for loading configuration
from omegaconf import DictConfig
from hydra import compose, initialize
from sqlalchemy import create_engine
from prefect import flow, task  

@task 
def load_config():
    with initialize(version_base=None, config_path="../config"):
        config = compose(config_name="main")
    return config

@task 
def get_data(config: DictConfig):
    connection = config.connection
    engine = create_engine(
        f"postgresql://{connection.user}:{connection.password}@{connection.host}/{connection.database}",
    )
    query = f'SELECT * FROM "{config.data.raw}"'
    df = pd.read_sql(query, con=engine)
    return df

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