import logging
import os
from pathlib import Path
from typing import Callable, Union, Dict, List

from babel.messages.pofile import read_po

log = logging.getLogger("tuxbot.core.i18n")

_translators = []

_current_locale = "en-US"
_locale_key_value: Dict[str, List[str]] = {
    "en": ["english", "anglais", "en", "us"],
    "fr": ["français", "francais", "french", "fr", "be"],
}
_available_locales: Dict[str, str] = {"en": "en-US", "fr": "fr-FR"}


def get_locale() -> str:
    return _current_locale


def find_locale(locale: str) -> str:
    """We suppose `locale` is in `_locale_key_value.values()`"""

    for key, val in _locale_key_value.items():
        if locale in val:
            return key


def set_locale(locale: str) -> None:
    if not any(locale in values for values in _locale_key_value.values()):
        raise NotImplementedError("This locale isn't implemented")
    else:
        global _current_locale
        _current_locale = _available_locales.get(find_locale(locale))
        reload_locales()


def reload_locales() -> None:
    for translator in _translators:
        translator.load_translations()


class Translator(Callable[[str], str]):
    """Class to load texts at init."""

    def __init__(self, name: str, file_location: Union[str, Path, os.PathLike]):
        """Initializes the Translator object.

        Parameters
        ----------
        name : str
            The cog name.
        file_location:str|Path|os.PathLike
            File path for the required extension.

        """
        self.cog_folder = Path(file_location).resolve().parent
        self.cog_name = name
        self.translations = {}

        _translators.append(self)

        self.load_translations()

    def __call__(self, untranslated: str) -> str:
        try:
            return self.translations[untranslated]
        except KeyError:
            return untranslated

    def __repr__(self):
        return "<Translator, name=%s, file_location=%s>" % (
            self.cog_name,
            self.cog_folder,
        )

    def load_translations(self):
        """Loads the current translations.

        """
        self.translations = {}
        locale_path = self.cog_folder / "locales" / f"{get_locale()}.po"

        with locale_path.open("r") as f:
            catalog = read_po(f)

        for message in catalog:
            if message.id:
                self._add_translation(message.id, message.string)

    def _add_translation(self, untranslated, translated):
        if translated:
            self.translations[untranslated] = translated
