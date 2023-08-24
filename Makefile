###############################################################################
# Compile
###############################################################################

.PHONY: compile_base_deps
compile_base_deps:
	pip-compile --allow-unsafe --output-file=requirements/base.txt --resolver=backtracking --strip-extras requirements/base.in

.PHONY: compile_local_deps
compile_local_deps:
	pip-compile --allow-unsafe --output-file=requirements/local.txt --resolver=backtracking --strip-extras requirements/local.in

.PHONY: compile_production_deps
compile_production_deps:
	pip-compile --allow-unsafe --output-file=requirements/production.txt --resolver=backtracking --strip-extras requirements/production.in

.PHONY: compile_deps
compile_deps: compile_local_deps compile_production_deps

###############################################################################
# Style
###############################################################################

.PHONY: pre_commit
pre_commit:
	pre-commit run --all-files


###############################################################################
# Rewrite
###############################################################################

.PHONY: build
build:
	poetry build

.PHONY: dev
dev: pre_commit build run

.PHONY: run
run:
	poetry run start
