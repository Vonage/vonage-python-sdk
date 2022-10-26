.PHONY: clean test build coverage install requirements release

coverage:
	coverage run -m pytest -v
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

requirements: .requirements.txt

.requirements.txt: requirements.txt
	python -m pip install --upgrade pip setuptools
	python -m pip install -r requirements.txt
	python -m pip freeze > .requirements.txt
