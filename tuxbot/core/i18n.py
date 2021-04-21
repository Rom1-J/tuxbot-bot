import logging
import os
from pathlib import Path
from typing import Dict, NoReturn, Any, Tuple

from babel.messages.pofile import read_po

from tuxbot.core import Config
from tuxbot.core.config import search_for
from tuxbot.core.utils.functions.extra import ContextPlus

log = logging.getLogger("tuxbot.core.i18n")

_translators = []

available_locales: Dict[str, Tuple] = {
    "en-US": ("english", "anglais", "en", "us", "en-us"),
    "fr-FR": ("français", "francais", "french", "fr", "be", "fr-fr"),
}


def find_locale(locale: str) -> str | NoReturn:
    """We suppose `locale` is in `_available_locales.values()`"""

    for key, val in available_locales.items():
        if locale in val:
            return key

    raise NotImplementedError("This locale isn't implemented")


def list_locales() -> str:
    description = ""

    for key, value in available_locales.items():
        description += f":flag_{key[-2:].lower()}: {value[0]}\n"

    return description


def get_locale_name(locale: str) -> str:
    """Return the name of this `locale`"""
    return available_locales[find_locale(locale)][0]


class Translator:
    """Class to load texts at init."""

    def __init__(self, name: str, file_location: Path | os.PathLike | str):
        """Initializes the Translator object.

        Parameters
        ----------
        name : str
            The cog name.
        file_location:Path|os.PathLike|str
            File path for the required extension.

        """
        self.cog_folder = Path(file_location).resolve().parent
        self.cog_name = name
        self.translations: Dict[str, Any] = {}

        _translators.append(self)

        self.load_translations()

    def __call__(
        self, untranslated: str, ctx: ContextPlus, config: Config
    ) -> str:
        try:
            user_locale = search_for(
                config.Users, ctx.author.id, "locale", None
            )
            if user_locale:
                return self.translations[user_locale][untranslated]

            guild_locale = search_for(
                config.Servers, ctx.guild.id, "locale", None
            )
            if guild_locale:
                return self.translations[guild_locale][untranslated]

            return self.translations[config.Core.locale][untranslated]
        except KeyError:
            return untranslated

    def __repr__(self):
        return "<Translator, name=%s, file_location=%s>" % (
            self.cog_name,
            self.cog_folder,
        )

    def load_translations(self):
        """Loads the current translations."""
        for locale in available_locales:
            locale_path = self.cog_folder / "locales" / f"{locale}.po"

            with locale_path.open("r") as f:
                catalog = read_po(f)

            for message in catalog:
                if message.id:
                    self._add_translation(locale, message.id, message.string)

    def _add_translation(
        self, locale: str, untranslated: str, translated: str
    ):
        if translated:
            if not self.translations.get(locale, False):
                self.translations[locale] = {}

            self.translations[locale][untranslated] = translated
