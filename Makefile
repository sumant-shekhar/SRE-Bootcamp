VERSION ?= 1.0.0
IMAGE_NAME := rest-api
CONTAINER_NAME := rest-api-app

VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
FLASK := $(VENV)/bin/flask

APP := app.py
PORT := 4000

.PHONY: help venv install run test clean \
	init-db migrate upgrade \
	docker-build docker-run docker-stop

help:
	@echo "Available commands:"
	@echo "  make install       Install dependencies"
	@echo "  make run           Run application"
	@echo "  make test          Run tests"
	@echo "  make clean         Remove virtual environment"
	@echo "  make init-db       Initialize migrations"
	@echo "  make migrate       Create migration"
	@echo "  make upgrade       Apply migrations"
	@echo "  make docker-build  Build Docker image"
	@echo "  make docker-run    Run Docker container"
	@echo "  make docker-stop   Stop Docker container"
	@echo "  make docker-compose up   Build Docker containers"
	@echo "  make docker-compose down   Destroy Docker containers"
	@echo "  make docker-compose start   Start Docker containers"
	@echo "  make docker-compose stop   Stop Docker containers"

venv:
	python3 -m venv $(VENV)

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) $(APP)

test:
	$(VENV)/bin/pytest -v

init-db:
	FLASK_APP=$(APP) $(FLASK) db init

migrate:
	FLASK_APP=$(APP) $(FLASK) db migrate -m "auto migration"

upgrade:
	FLASK_APP=$(APP) $(FLASK) db upgrade

clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docker-build:
	docker build -t $(IMAGE_NAME):$(VERSION) .

docker-run:
	docker run -d \
		--name $(CONTAINER_NAME) \
		-p $(PORT):$(PORT) \
		--env-file .env \
		$(IMAGE_NAME):$(VERSION)

docker-stop:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true

docker-compose up:
	docker-compose up -d --build

docker-compose down:
	docker-compose down -v

docker-compose start:
	docker-compose start

docker-compose stop:
	docker-compose stop