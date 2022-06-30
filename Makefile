.PHONY: clean test build coverage install release

coverage:
	pytest -v --cov
	coverage html

test:
	pytest -v

clean:
	rm -rf dist build

build:
	python -m build

release:
	python -m twine upload dist/*

install: requirements

requirements: requirements.txt
	python -m pip install --upgrade pip setuptools
	python -m pip install -r requirements.txt
	python -m pip freeze > .requirements.txt

dev-requirements: requirements-dev.txt
	python -m pip install --upgrade pip setuptools
	python -m pip install -r requirements-dev.txt
	python -m pip freeze > .requirements-dev.txt