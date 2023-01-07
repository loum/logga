.SILENT:
.DEFAULT_GOAL := help

include makester/makefiles/makester.mk

init: py-venv-clear py-venv-init py-install-makester
	$(MAKE) py-install

docs:
	$(shell which sphinx-build) -b html doc/source doc/build

help: makester-help
	@echo "(Makefile)\n\
  docs				   Build the Sphinx-style documentation\n\
  init                 Build the local Python-based virtual environment\n\"
