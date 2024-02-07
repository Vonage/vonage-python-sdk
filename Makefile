.PHONY: test coverage

test:
	pants test ::

coverage:
	pants test --use-coverage --open-coverage ::