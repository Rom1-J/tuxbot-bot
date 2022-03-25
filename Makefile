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

.PHONY: dev
dev: style update
	$(VIRTUAL_ENV)/bin/tuxbot

.PHONY: speed_dev
speed_dev: update
	$(VIRTUAL_ENV)/bin/tuxbot


########################################################################################################################
# Blackify code
########################################################################################################################

.PHONY: lint
lint:
	$(PYTHON_PATH) -m pylint tuxbot --verbose --output-format=colorized

.PHONY: type
type:
	$(PYTHON_PATH) -m mypy tuxbot

.PHONY: flake8
flake8:
	$(PYTHON_PATH) -m flake8 tuxbot

.PHONY: isort
isort:
	$(PYTHON_PATH) -m isort tuxbot

.PHONY: pre_commit
pre_commit:
	./$(VIRTUAL_ENV)/bin/pre-commit run --all-files

.PHONY: style
style: isort lint type flake8

########################################################################################################################
# Rewrite
########################################################################################################################

.PHONY: rewrite
rewrite: update
	cd tuxbot && \
	PYTHON_ENV=development \
	STATSD_HOST="192.168.1.195" \
	DD_AGENT_HOST="192.168.1.195" \
	DD_ENV="Tuxbot-dev" \
	CLUSTER_ID=1 \
	CLUSTER_COUNT=1 \
	SHARD_ID=0 \
	SHARD_COUNT=1 \
	FIRST_SHARD_ID=0 \
	LAST_SHARD_ID=0 \
	python start.py

.PHONY: soft-rewrite
soft-rewrite: soft-update
	cd tuxbot && \
	PYTHON_ENV=development \
	STATSD_HOST="192.168.1.195" \
	CLUSTER_ID=1 \
	CLUSTER_COUNT=1 \
	SHARD_ID=0 \
	SHARD_COUNT=1 \
	FIRST_SHARD_ID=0 \
	LAST_SHARD_ID=0 \
	python start.py
