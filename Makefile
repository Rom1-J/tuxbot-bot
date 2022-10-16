include .env.local
export

########################################################################################################################
# Style
########################################################################################################################

.PHONY: pre_commit
pre_commit:
	pre-commit run --all-files


########################################################################################################################
# Rewrite
########################################################################################################################

.PHONY: build
build:
	poetry build

.PHONY: dev
dev: pre_commit build run

.PHONY: run
run:
	poetry run start
