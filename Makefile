PYTHON = python
VENV = ~/tuxvenv

# Init
main:
	$(PYTHON) -m venv --clear $(VENV)
	$(VENV)/bin/pip install -U pip setuptools
install:
	$(VENV)/bin/pip install .
update:
	$(VENV)/bin/pip install -U .

# Blackify code
reformat:
	$(PYTHON) -m black `git ls-files "*.py"`