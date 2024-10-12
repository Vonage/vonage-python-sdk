.PHONY: test coverage

test:
	pants test ::

coverage:
	pants test --use-coverage ::

coverage-report:
	pants test --use-coverage --open-coverage ::

install:
	pip install -r requirements.txt