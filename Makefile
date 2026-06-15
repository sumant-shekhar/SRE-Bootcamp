# Variables
VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
FLASK = $(VENV)/bin/flask
APP = app.py
PORT = 4000

# Docker Milestone Additions 
VERSION ?= 1.0.0
IMAGE_NAME := rest-api-service
CONTAINER_NAME := rest-api-app

.PHONY: help venv install run dev clean freeze test migrate upgrade init-db docker-build docker-run docker-stop

help:
	@echo "Available commands:"
	@echo "  make venv         Create virtual environment"
	@echo "  make install      Install dependencies"
	@echo "  make run          Run the app"
	@echo "  make test         Run pytest"
	@echo "  make clean        Remove venv and cache"
	@echo "  make freeze       Freeze dependencies to requirements.txt"
	@echo "  make migrate      Create a new migration"
	@echo "  make upgrade      Apply migrations to the database"
	@echo "  make init-db      Initialize the migration directory"
	@echo "  make docker-build Build the multi-stage Docker image with SemVer"
	@echo "  make docker-run   Run container with environment variable injection"
	@echo "  make docker-stop  Stop and remove the running container"
	@echo "  make help         Show this help message"
	

venv:
	python3 -m venv $(VENV)

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) $(APP)

test:
	$(VENV)/bin/pytest

clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -f database.db

migrate:
	FLASK_APP=$(APP) $(FLASK) db migrate -m "auto migration"

upgrade:
	FLASK_APP=$(APP) $(FLASK) db upgrade

init-db:
	FLASK_APP=$(APP) $(FLASK) db init

docker-build:
	docker build -t $(IMAGE_NAME):$(VERSION) .

docker-run:
	docker run -d \
		--name $(CONTAINER_NAME) \
		-p $(PORT):$(PORT) \
		--env-file .env \
		-e FLASK_APP=$(APP) \
		$(IMAGE_NAME):$(VERSION)

docker-stop:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true
