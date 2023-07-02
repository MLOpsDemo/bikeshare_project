default: all

install:
	pip3 install -r requirements/requirements.txt
		
train:
	python ./bikeshare_model/train_pipeline.py

format-check:
	-black --check ./bikeshare_model

format:
	black ./bikeshare_model
	
lint:
	pylint --disable=R,C ./bikeshare_model

test:
	python -m pytest tests/test_*.py

all : install lint test format-check