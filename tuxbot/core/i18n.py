import logging
import os
from pathlib import Path
from typing import Callable, Union

__all__ = [
    "get_locale",
    "set_locale",
    "reload_locales",
    "Translator",
]

log = logging.getLogger("tuxbot.core.i18n")

_translators = []
_current_locale = "en-US"


def get_locale() -> str:
    return _current_locale


def set_locale(locale: str) -> None:
    global _current_locale
    _current_locale = locale
    reload_locales()


def reload_locales() -> None:
    for translator in _translators:
        translator.load_translations()


class Translator(Callable[[str], str]):
    """Class to load locales at init."""

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

    def load_translations(self):
        """Loads the current translations.

        """
        self.translations = {}
        locale_path = self.cog_folder / "locales" / f"{get_locale()}.po"

        ...

    def _add_translation(self, untranslated, translated):
        if translated:
            self.translations[untranslated] = translated
