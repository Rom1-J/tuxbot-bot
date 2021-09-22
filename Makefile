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
	$(VIRTUAL_ENV)/bin/pip install -r requirements/dev.requirements.txt

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
# Docker
########################################################################################################################

.PHONY: docker
docker:
	$(DOCKER_LOCAL) build
	$(DOCKER_LOCAL) up -d

.PHONY: docker-start
docker-start:
	$(DOCKER_TUXBOT) tuxbot


########################################################################################################################
# Blackify code
########################################################################################################################

.PHONY: black
black:
	$(PYTHON_PATH) -m black `git ls-files "*.py"` --line-length=79

.PHONY: lint
lint:
	$(PYTHON_PATH) -m pylint tuxbot --verbose --output-format=colorized

.PHONY: type
type:
	$(PYTHON_PATH) -m mypy tuxbot

.PHONY: style
style: black lint type


########################################################################################################################
# Translations
########################################################################################################################

.PHONY: xgettext
xgettext:
	for cog in tuxbot/cogs/*/; do \
		xgettext `find $$cog -type f -name '*.py'` --output=$$cog/locales/messages.pot $(XGETTEXT_FLAGS); \
  	done

.PHONY: msginit
msginit:
	for cog in tuxbot/cogs/*/; do \
		msginit --input=$$cog/locales/messages.pot --output=$$cog/locales/fr-FR.po --locale=fr_FR.UTF-8 --no-translator; \
		msginit --input=$$cog/locales/messages.pot --output=$$cog/locales/en-US.po --locale=en_US.UTF-8 --no-translator; \
  	done

.PHONY: msgmerge
msgmerge:
	for cog in tuxbot/cogs/*/; do \
		msgmerge --update $$cog/locales/fr-FR.po $$cog/locales/messages.pot; \
		msgmerge --update $$cog/locales/en-US.po $$cog/locales/messages.pot; \
  	done


########################################################################################################################
# Misc
########################################################################################################################

.PHONY: cog
cog:
	$(PYTHON_PATH) tuxbot/core/utils/cli/cog_generator.py
