.PHONY: setup install dev-install test build clean help

# Variables
PIP ?= pip
LLM ?= llm
PYTHON ?= python

# Default target
help:
	@echo "Available targets:"
	@echo "  make setup        - Install dependencies"
	@echo "  make install      - Install package in production mode"
	@echo "  make dev-install  - Install package in development mode"
	@echo "  make test         - Run tests (if any exist)"
	@echo "  make build        - Build distribution files"
	@echo "  make clean        - Clean build artifacts"
	@echo "  make help         - Show this help"

setup:
	@echo "Setting up development environment..."
	$(PIP) install -e .
	$(PIP) install llm httpx

install:
	@echo "Installing llm-iaedu..."
	$(PIP) install .

dev-install:
	@echo "Installing llm-iaedu in development mode..."
	$(PIP) install -e .

test:
	@echo "No tests implemented yet. Add tests to test/ directory and update this target."
	@echo "Example: $(PYTHON) -m pytest test/"

build:
	@echo "Building distribution files..."
	$(PYTHON) -m build

clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/ dist/ *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete

# Verify installation
verify:
	@echo "Verifying installation..."
	$(LLM) plugins | grep iaedu || echo "Plugin not found in llm plugins list"
	@echo "To use the plugin:"
	@echo "  1. Set your IAEDU API key: llm keys set iaedu"
	@echo "  2. Ensure iaedu-adapter is running (default: http://localhost:4000)"
	@echo "  3. Run: llm -m iaedu \"Your question here\""