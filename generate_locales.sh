#!/bin/bash

BASEDIR=$(pwd)

cd "$BASEDIR/extras/locales/en/LC_MESSAGES"

for i in *.po ; do
  [[ -f "$i" ]] || continue
  /usr/lib/python3.8/Tools/i18n/msgfmt.py -o "${i%.po}.mo" "${i%.po}"
done

cd "$BASEDIR/extras/locales/fr/LC_MESSAGES"

for i in *.po ; do
  [[ -f "$i" ]] || continue
  /usr/lib/python3.8/Tools/i18n/msgfmt.py -o "${i%.po}.mo" "${i%.po}"
done