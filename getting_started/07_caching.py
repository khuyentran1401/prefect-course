import random
from datetime import timedelta
from time import sleep

from prefect import flow, task
from prefect.tasks import task_input_hash


@task(name="May Fail")
def may_fail():
    outcome = random.choice([0, 1, 2])
    if outcome == 0:
        raise ValueError("The outcome can't be 0.")
    return outcome


@task(
    name="Very Large Computation",
    cache_key_fn=task_input_hash,
    cache_expiration=timedelta(days=1),
)
def large_computation(outcome):
    sleep(5)
    return 2 / outcome


@task(name="Follows Large Computation")
def follows_large_computation(num):
    return num + 1


@flow(name="Cached flow")
def main():
    outcome = may_fail()
    num = large_computation(outcome)
    final = follows_large_computation(num)
    return final


if __name__ == "__main__":
    main()
