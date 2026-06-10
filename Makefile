# Variables
VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
FLASK = $(VENV)/bin/flask
APP = app.py
PORT = 4000

.PHONY: help venv install run dev db clean freeze

help:
	@echo "Available commands:"
	@echo "  make venv      Create virtual environment"
	@echo "  make install   Install dependencies"
	@echo "  make run       Run the app"
	@echo "  make db        Create database tables"
	@echo "  make clean     Remove venv and cache"
	@echo "  make freeze    Freeze dependencies to requirements.txt"
	@echo "  make migrate   Create a new migration"
	@echo "  make upgrade   Apply migrations to the database"
	@echo "  make init-db   Initialize the migration directory"
	@echo "  make help      Show this help message"
	
# Create virtual environment
venv:
	python3 -m venv $(VENV)

# Install dependencies
install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

# Run app normally
run:
	$(PYTHON) $(APP)

# Cleanup
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