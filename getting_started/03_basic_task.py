from typing import Tuple

import pandas as pd
from prefect import flow, get_run_logger, task
from pytrends.request import TrendReq


@task
def get_pytrends(keywords: Tuple[str, str]):
    pytrends = TrendReq(hl="en-US", tz=360)
    pytrends.build_payload(keywords)
    return pytrends


@task
def get_interest_overtime(pytrends: TrendReq, start_date: str):
    interest = pytrends.interest_over_time().loc[start_date:]
    return interest


@task
def get_difference(data: pd.DataFrame):
    data["difference"] = data.diff(axis=1).iloc[:, -1].abs().values
    return data


@task
def get_difference_by_year(data: pd.DataFrame, keywords: Tuple[str, str]):
    mean_diff = data.groupby(data.index.year)["difference"].mean()
    logger = get_run_logger()
    logger.info(
        f"The mean difference in the number of interests by year between the keywords {keywords[0]} and {keywords[1]} is:"
    )
    logger.info(mean_diff)
    return mean_diff


@flow
def compare_two_keywords(keywords: list, start_date: str):
    pytrends = get_pytrends(keywords)
    interest = get_interest_overtime(pytrends, start_date)
    difference = get_difference(interest)
    mean_difference = get_difference_by_year(difference, keywords)
    return mean_difference


if __name__ == "__main__":
    keywords = ("data engineer", "data scientist")
    start_date = "2020-01-01"
    mean_difference = compare_two_keywords(
        keywords=keywords, start_date=start_date
    )
