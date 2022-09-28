import random

from prefect import flow, task


@task(name="May Fail", retries=3, retry_delay_seconds=5)
def may_fail():
    outcome = random.choice([0, 1])
    if outcome == 0:
        raise ValueError("The outcome can't be 0.")
    return outcome


@flow(name="Retries flow")
def main():
    return may_fail()


if __name__ == "__main__":
    main()
