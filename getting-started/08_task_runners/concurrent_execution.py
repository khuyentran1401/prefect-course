import time

from prefect import flow, task

@task
def shout(number):
    time.sleep(0.5)
    print(f"#{number}")

@flow
def count_to(highest_number):
    for number in range(highest_number):
        shout.submit(number)

if __name__ == "__main__":
    count_to(10)