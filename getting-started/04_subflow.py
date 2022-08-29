from prefect import flow

@flow 
def prepare_for_training():
	...

@flow
def train():
	...

@flow
def development():
    prepare_for_training()
    train()