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