PYTHON = python
VENV = venv

XGETTEXT_FLAGS = --no-wrap --language='python' --keyword=_ --from-code='UTF-8' --msgid-bugs-address='rick@gnous.eu' --width=79 --package-name='Tuxbot-bot'

# Init
main:
	$(PYTHON) -m venv --clear $(VENV)
	$(VENV)/bin/pip install -U pip setuptools
install:
	$(VENV)/bin/pip install .
install-dev:
	$(VENV)/bin/pip install -r dev.requirements.txt
update:
	$(VENV)/bin/pip install --upgrade --force-reinstall .
update_soft:
	$(VENV)/bin/pip install --upgrade .

dev: reformat update_soft
	tuxbot dev

# Blackify code
reformat:
	$(PYTHON) -m black `git ls-files "*.py"` --line-length=79 && $(PYTHON) -m pylint tuxbot

# Translations
xgettext:
	for cog in tuxbot/cogs/*/; do \
		xgettext `find $$cog -type f -name '*.py'` --output=$$cog/locales/messages.pot $(XGETTEXT_FLAGS); \
  	done
msginit:
	for cog in tuxbot/cogs/*/; do \
		msginit --input=$$cog/locales/messages.pot --output=$$cog/locales/fr-FR.po --locale=fr_FR.UTF-8 --no-translator; \
		msginit --input=$$cog/locales/messages.pot --output=$$cog/locales/en-US.po --locale=en_US.UTF-8 --no-translator; \
  	done
msgmerge:
	for cog in tuxbot/cogs/*/; do \
		msgmerge --update $$cog/locales/fr-FR.po $$cog/locales/messages.pot; \
		msgmerge --update $$cog/locales/en-US.po $$cog/locales/messages.pot; \
  	done