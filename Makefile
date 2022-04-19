.PHONY: clean test build coverage install requirements release

clean:
	rm -rf dist build

coverage:
	pytest -v --cov
	coverage html

test:
	pytest -v

build:
	python -m build

release:
	python -m twine upload dist/*

install: requirements

requirements: .requirements.txt

.requirements.txt: requirements.txt
	python -m pip install --upgrade pip setuptools
	python -m pip install -r requirements.txt
	python -m pip freeze > .requirements.txt
