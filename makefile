default: all

install:
	pip3 install -r requirements/requirements.txt
		
train:
	python3 ./bikeshare_model/train_pipeline.py

format-check:
	-black --check ./bikeshare_model

format:
	black ./bikeshare_model
	
lint:
	pylint --disable=R,C ./bikeshare_model/*.py

test:
	python3 -m pytest tests/test_*.py

all : install lint train test format-check