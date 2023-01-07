.SILENT:
.DEFAULT_GOAL := help

include makester/makefiles/makester.mk

_venv-init: py-venv-clear py-venv-init

# Install optional packages for development.
init-dev: py-venv-clear py-venv-init py-install-makester
	MAKESTER__PIP_INSTALL_EXTRAS=dev $(MAKE) py-install-extras

# Streamlined production packages.
init: _venv-init
	$(MAKE) py-install

MAKESTER__VERSION_FILE := $(MAKESTER__PYTHON_PROJECT_ROOT)/VERSION

TESTS := tests
tests:
	$(MAKESTER__PYTHON) -m pytest\
 --override-ini log_cli=true\
 --override-ini junit_family=xunit2\
 --log-cli-level=INFO -svv\
 --exitfirst\
 --cov-config tests/.coveragerc\
 --pythonwarnings ignore\
 --cov src\
 --junitxml junit.xml $(TESTS)

docs:
	$(shell which sphinx-build) -b html doc/source doc/build

help: makester-help
	@echo "(Makefile)\n\
  docs                 Build the Sphinx-style documentation\n\
  init                 Build the local Python-based virtual environment\n"

.PHONY: tests
