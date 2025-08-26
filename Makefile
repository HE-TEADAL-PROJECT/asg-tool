PYTHON = python
PIP = $(PYTHON) -m pip
ROOT_DIR = .

# Check if tools are installed
RUFF := $(shell command -v ruff 2>nul || which ruff 2>/dev/null)
BLACK := $(shell command -v black 2>nul || which black 2>/dev/null)
MYPY := $(shell command -v mypy 2>nul || which mypy 2>/dev/null)

# The default target (help)
.DEFAULT_GOAL := help

.PHONY: help
help:  ## Show this help message
	@echo
	@echo "Available make targets:"
	@echo
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
# 	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'


-----DEV-----: ## ----

.PHONY: ruff
ruff:  ## Run ruff check
ifeq ($(RUFF),)
	@echo "Error: 'ruff' is not installed or not in PATH."
	@echo "Install it with: pip install ruff"
	@exit 1
else
	@echo "Checking with ruff..."
	@$(RUFF) check src
endif

.PHONY: black
black:  ## Run black --check
ifeq ($(BLACK),)
	@echo "Error: 'black' is not installed or not in PATH."
	@echo "Install it with: pip install black"
	@exit 1
else
	@echo "Checking with black..."
	@$(BLACK) --check src
endif

.PHONY: check
check:  ruff black ## Run ruff, black (check only), and mypy
ifeq ($(MYPY),)
	@echo "Error: 'mypy' is not installed or not in PATH."
	@echo "Install it with: pip install mypy"
	@exit 1
else
	@echo "Runing mypy..."
	$(MYPY) src
endif

.PHONY: fmt
fmt:  ## Format code with black and auto-fix lint with ruff
	black src
	ruff check src --fix


.PHONY: clean
clean: ## Clean up generated files
	find $(ROOT_DIR) -type d -name '__pycache__' -exec rm -rf {} \;
	find $(ROOT_DIR) -type d -name '*.egg-info' -exec rm -rf {} \;
	find $(ROOT_DIR) -type f -name '*.pyc' -delete
	rm -fr $(ROOT_DIR)/.pytest_cache $(ROOT_DIR)/.mypy_cache $(ROOT_DIR)/.ruff_cache
	rm -rf $(ROOT_DIR)/build $(ROOT_DIR)/dist
	@echo "Clean complete."


.PHONY: clean-all
clean-all: clean ## Clean up generated files and virtual environment
	rm -rf .venv

.PHONY: install
install: ## Install the project locally, in use mode
	$(PIP) install --upgrade pip
	$(PIP) install -e .

.PHONY: install-dev
install-dev: ## Install the project locally, in dev mode
	$(PIP) install -e .[dev]

