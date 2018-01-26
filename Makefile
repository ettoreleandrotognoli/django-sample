PYTHON ?= python3
PYENV ?= venv/bin/python
PORT ?= 8000
ADDRESS ?= 0.0.0.0


init:
	test -d "$(PYENV)" || $(PYTHON) -m venv venv
	$(PYENV) -m pip install -U pip
	$(PYENV) -m pip install -Ur requirements.txt

db:
	$(PYENV) manage.py makemigrations
	$(PYENV) manage.py migrate

run:
	$(PYENV) manage.py runserver $(ADDRESS):$(PORT)