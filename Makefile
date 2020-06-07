PYTHON = python

# Blackify code
reformat:
	$(PYTHON) -m black `git ls-files "*.py"`