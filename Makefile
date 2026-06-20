.PHONY: setup install dev-install test build clean help start \
        check lint format doctor metrics pre-commit

# Variables
PIP ?= pip
LLM ?= llm
PYTHON ?= python3

# Default target
help:
	@echo "llm-iaedu — Makefile"
	@echo ""
	@echo "Setup:"
	@echo "  make setup        Install dependencies (dev mode)"
	@echo "  make install      Install package in production mode"
	@echo "  make dev-install  Install package in development mode"
	@echo ""
	@echo "Usage:"
	@echo "  make start        Install + show usage instructions"
	@echo "  make check        Verify plugin is installed and configured"
	@echo ""
	@echo "Quality:"
	@echo "  make lint         Run ruff linter"
	@echo "  make format       Run ruff formatter"
	@echo "  make pre-commit   Run lint + format-check + build"
	@echo "  make test         Run tests (if any exist)"
	@echo "  make build        Build distribution files"
	@echo ""
	@echo "Diagnostics:"
	@echo "  make doctor       Check environment and config"
	@echo "  make metrics      Show project metrics"
	@echo ""
	@echo "Housekeeping:"
	@echo "  make clean        Clean build artifacts"

setup:
	@echo "Setting up development environment..."
	$(PIP) install -e .
	$(PIP) install ruff

install:
	@echo "Installing llm-iaedu..."
	$(PIP) install .

dev-install:
	@echo "Installing llm-iaedu in development mode..."
	$(PIP) install -e .

start:
	@echo "=== llm-iaedu ==="
	$(MAKE) install
	@echo ""
	$(MAKE) check

check:
	@echo "--- Installation ---"
	$(LLM) plugins 2>/dev/null | grep -q iaedu \
		&& echo "  [OK] Plugin registered in llm" \
		|| echo "  [FAIL] Plugin not found"
	@echo ""
	@echo "--- Configuration ---"
	@for var in IAEDU_API_KEY IAEDU_CHANNEL_ID IAEDU_AGENT_ID; do \
		val=$$(eval echo \$$\$$var); \
		if [ -n "$$val" ]; then \
			echo "  [OK] $$$$var is set"; \
		else \
			echo "  [WARN] $$$$var is not set (env var or .env)"; \
		fi; \
	done
	@$(LLM) keys list 2>/dev/null | grep -q iaedu \
		&& echo "  [OK] iaedu key is set in llm keys" \
		|| echo "  [WARN] iaedu key not set (run: llm keys set iaedu)"
	@echo ""
	@echo "--- Usage ---"
	@echo "  llm -m iaedu \"Your question\""
	@echo "  llm chat -m iaedu"
	@echo "  (set as default: llm models default iaedu)"

lint:
	@echo "Running ruff linter..."
	ruff check llm_iaedu.py

format:
	@echo "Running ruff formatter..."
	ruff format llm_iaedu.py

format-check:
	@echo "Checking formatting..."
	ruff format --check llm_iaedu.py

pre-commit:
	$(MAKE) lint
	$(MAKE) format-check
	$(MAKE) build

test:
	@if command -v pytest >/dev/null 2>&1; then \
		$(PYTHON) -m pytest test/ -v; \
	else \
		echo "pytest not installed. Install with: pip install pytest"; \
		echo "Then add tests to test/ directory."; \
	fi

build:
	@echo "Building distribution files..."
	$(PYTHON) -m build

doctor:
	@echo "=== Environment ==="
	@echo "Python: $$($(PYTHON) --version 2>&1)"
	@echo "Pip:    $$($(PIP) --version 2>&1)"
	@echo "LLM:    $$($(LLM) --version 2>&1)"
	@echo ""
	@echo "=== Installed Packages ==="
	$(PIP) list 2>/dev/null | grep -i -e llm -e httpx -e iaedu
	@echo ""
	@echo "=== Plugin Registration ==="
	$(LLM) plugins 2>/dev/null | grep -A1 iaedu \
		|| echo "  Plugin not found"
	@echo ""
	@echo "=== Config Files ==="
	@for f in ./.env ~/.config/iaedu/env ~/.iaedu.env; do \
		exp=$$(eval echo $$f); \
		if [ -f "$$exp" ]; then \
			echo "  [OK] $$exp"; \
		else \
			echo "  [--] $$exp (not found)"; \
		fi; \
	done
	@echo ""
	@echo "=== llm Keys ==="
	$(LLM) keys list 2>/dev/null | grep iaedu \
		|| echo "  No iaedu key set"

metrics:
	@echo "--- Project Metrics ---"
	@echo "Source lines: $$(wc -l < llm_iaedu.py)"
	@echo "  - Functions: $$(grep -c '^def ' llm_iaedu.py)"
	@echo "  - Classes:   $$(grep -c '^class ' llm_iaedu.py)"
	@echo ""
	@echo "Doc files: $$(ls docs/*.md 2>/dev/null | wc -l)"

clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/ dist/ *.egg-info .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete
