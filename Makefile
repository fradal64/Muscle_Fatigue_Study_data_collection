#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = Muscle_Fatigue_Study_data_collection
PYTHON_VERSION = 3.12.3
PYTHON_INTERPRETER = python

#################################################################################
# COMMANDS                                                                      #
#################################################################################


## Install Python Dependencies
.PHONY: requirements
requirements:
	$(PYTHON_INTERPRETER) -m pip install -U pip 
	$(PYTHON_INTERPRETER) -m pip freeze > requirements.txt
	# Remove -e git lines and replace them with -e .
	sed -i '/^-e git+/d' requirements.txt
	echo "-e ." >> requirements.txt
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt

	



## Delete all compiled Python files
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint using flake8 and black (use `make format` to do formatting)
.PHONY: lint
lint:
	flake8 src
	isort --check --diff --profile black src
	black --check --config pyproject.toml src


## Format source code with black and isort
.PHONY: format
format:
	isort --profile black src
	black --config pyproject.toml src




## Set up python interpreter environment
.PHONY: create_environment
create_environment:
	$(PYTHON_INTERPRETER) -m venv venv
	@echo ">>> New virtualenv created. Activate with:\nsource venv/bin/activate"

	


#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys; \
lines = '\n'.join([line for line in sys.stdin]); \
matches = re.findall(r'\n## (.*)\n[\s\S]+?\n([a-zA-Z_-]+):', lines); \
print('Available rules:\n'); \
print('\n'.join(['{:25}{}'.format(*reversed(match)) for match in matches]))
endef
export PRINT_HELP_PYSCRIPT

help:
	@$(PYTHON_INTERPRETER) -c "${PRINT_HELP_PYSCRIPT}" < $(MAKEFILE_LIST)