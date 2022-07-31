ifeq ($(ISPROD), 1)
	DOCKER_LOCAL := docker-compose -f production.yml
else
	DOCKER_LOCAL := docker-compose -f local.yml
endif

INSTANCE := preprod

DOCKER_TUXBOT := $(DOCKER_LOCAL) run --rm tuxbot
VIRTUAL_ENV := venv
PYTHON_PATH := $(VIRTUAL_ENV)/bin/python

XGETTEXT_FLAGS := --no-wrap --language='python' --keyword=_ --from-code='UTF-8' --msgid-bugs-address='rick@gnous.eu' --width=79 --package-name='Tuxbot-bot'


########################################################################################################################
# Init
########################################################################################################################

.PHONY: main
main:
	$(VIRTUAL_ENV)/bin/pip install -U pip setuptools

.PHONY: install
install:
	$(VIRTUAL_ENV)/bin/pip install .

.PHONY: install-dev
install-dev:
	$(VIRTUAL_ENV)/bin/pip install -r requirements/local.txt

.PHONY: soft-update
soft-update:
	$(VIRTUAL_ENV)/bin/pip install .

.PHONY: update
update:
	$(VIRTUAL_ENV)/bin/pip install --upgrade .

.PHONY: update-all
update-all:
	$(VIRTUAL_ENV)/bin/pip install --upgrade --force-reinstall .


########################################################################################################################
# Style
########################################################################################################################

.PHONY: lint
lint:
	$(PYTHON_PATH) -m pylint tuxbot

.PHONY: black
black:
	$(PYTHON_PATH) -m black tuxbot

.PHONY: type
type:
	$(PYTHON_PATH) -m mypy tuxbot

.PHONY: style
style: black type lint

.PHONY: pre_commit
pre_commit:
	./$(VIRTUAL_ENV)/bin/pre-commit run --all-files


########################################################################################################################
# Rewrite
########################################################################################################################

.PHONY: dev
dev: pre_commit update-all run

.PHONY: run
run:
	cd tuxbot && \
	PYTHON_ENV=development \
	STATSD_HOST="192.168.1.175" \
	DD_AGENT_HOST="192.168.1.175" \
	DD_ENV="Tuxbot-dev" \
	CLUSTER_ID=1 \
	CLUSTER_COUNT=1 \
	SHARD_ID=0 \
	SHARD_COUNT=1 \
	FIRST_SHARD_ID=0 \
	LAST_SHARD_ID=0 \
	python start.py
