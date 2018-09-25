.PHONY: test install requirements release release-test

coverage:
	pytest -v --cov
	coverage html

test:
	pytest -v

dist:
	python setup.py sdist --formats zip,gztar bdist_wheel

release:
	twine upload dist/*

install: requirements

requirements: .requirements.txt

.requirements.txt: requirements.txt
	pip install --upgrade pip setuptools
	pip install -r requirements.txt
	pip freeze > .requirements.txt
