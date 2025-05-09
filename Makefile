.PHONY: format test coverage coverage-report install

format:
	pants lint ::
	pants fix ::

test:
	pants test ::

coverage:
	pants test --use-coverage ::

coverage-report:
	pants test --use-coverage --open-coverage ::

install:
	pip install -r requirements.txt