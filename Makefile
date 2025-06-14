# Makefile for AI Data Analyst Agent

.PHONY: help install install-dev test test-cov lint format clean build docs run docker-build docker-run

# Default target
help:
	@echo "Available commands:"
	@echo "  install        Install production dependencies"
	@echo "  install-dev    Install development dependencies"
	@echo "  test           Run tests"
	@echo "  test-cov       Run tests with coverage"
	@echo "  lint           Run linting checks"
	@echo "  format         Format code with black and isort"
	@echo "  clean          Clean up build artifacts"
	@echo "  build          Build distribution packages"
	@echo "  docs           Build documentation"
	@echo "  run            Run the application"
	@echo "  docker-build   Build Docker image"
	@echo "  docker-run     Run Docker container"

# Installation
install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt
	pre-commit install

# Testing
test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=. --cov-report=html --cov-report=term-missing

# Code quality
lint:
	flake8 .
	black --check .
	isort --check-only .
	mypy .
	bandit -r . -f json -o bandit-report.json

format:
	black .
	isort .

# Security
security:
	bandit -r . -f json -o bandit-report.json
	safety check

# Cleanup
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Build
build: clean
	python -m build

# Documentation
docs:
	cd docs && make html

# Run application
run:
	python main.py

run-gradio:
	python main.py --interface gradio

run-cloud:
	python main.py --backend cloud

# Docker
docker-build:
	docker build -t ai-data-analyst .

docker-run:
	docker run -p 8501:8501 ai-data-analyst

docker-compose-up:
	docker-compose up -d

docker-compose-down:
	docker-compose down

# Development
dev-setup: install-dev
	@echo "Development environment setup complete!"
	@echo "Run 'make test' to verify everything works"

# Pre-commit hooks
pre-commit:
	pre-commit run --all-files

# Example usage
example:
	python examples/basic_usage.py
