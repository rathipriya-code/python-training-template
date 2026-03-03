.PHONY: help install test test-day coverage lint format type-check clean

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install all dependencies
	pip install -e ".[dev]"
	pre-commit install

test: ## Run all tests with coverage
	pytest

test-day: ## Run tests for a specific day (e.g., make test-day DAY=01)
	@if [ -z "$(DAY)" ]; then \
		echo "Error: Please specify DAY (e.g., make test-day DAY=01)"; \
		exit 1; \
	fi
	pytest days/day_$(DAY)_* -v

coverage: ## Generate HTML coverage report
	pytest --cov-report=html
	@echo "Coverage report generated in htmlcov/index.html"

lint: ## Run linter (ruff)
	ruff check days/

format: ## Format code with black
	black days/

type-check: ## Run type checker (mypy)
	mypy days/

clean: ## Clean up generated files
	rm -rf __pycache__ .pytest_cache .coverage htmlcov .mypy_cache .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

check-all: lint type-check test ## Run all checks (lint, type-check, test)
