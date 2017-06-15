.PHONY: test install requirements release release-test
test:
	pytest -v

release-test:
	python setup.py sdist bdist_wheel upload -r pypitest

release:
	python setup.py sdist bdist_wheel upload

install: requirements

requirements: .requirements.txt

.requirements.txt: requirements.txt
	pip install -r requirements.txt
	pip freeze > .requirements.txt
