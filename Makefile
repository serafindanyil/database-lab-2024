.PHONY: install venv run dev gunicorn db-init db-migrate db-upgrade db-downgrade db-current seed clean

VENV ?= venv
PYTHON := $(VENV)/bin/python
PIP := $(PYTHON) -m pip

FLASK_APP ?= app:create_app
FLASK_ENV ?= development
FLASK_RUN_HOST ?= 127.0.0.1
FLASK_RUN_PORT ?= 5000

venv:
	@if [ ! -d "$(VENV)" ]; then \
		python3 -m venv $(VENV); \
	fi
	$(PIP) install --upgrade pip

install: venv
	$(PIP) install -r requirements.txt

run: install
	FLASK_APP=$(FLASK_APP) FLASK_ENV=$(FLASK_ENV) FLASK_RUN_HOST=$(FLASK_RUN_HOST) FLASK_RUN_PORT=$(FLASK_RUN_PORT) $(PYTHON) -m flask run --debug

dev: run

gunicorn: install
	$(VENV)/bin/gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app

db-init: install
	FLASK_APP=$(FLASK_APP) $(PYTHON) -m flask db init || true

db-migrate: install
	@if [ -z "$(message)" ]; then \
		echo "Usage: make db-migrate message=\"<message>\""; \
		exit 1; \
	fi
	FLASK_APP=$(FLASK_APP) $(PYTHON) -m flask db migrate -m "$(message)"

db-upgrade: install
	FLASK_APP=$(FLASK_APP) $(PYTHON) -m flask db upgrade

db-downgrade: install
	FLASK_APP=$(FLASK_APP) $(PYTHON) -m flask db downgrade

db-current: install
	FLASK_APP=$(FLASK_APP) $(PYTHON) -m flask db current

seed: install
	FLASK_APP=$(FLASK_APP) $(PYTHON) -m flask seed

clean:
	rm -rf $(VENV)
	find . -name '__pycache__' -type d -prune -exec rm -rf {} +