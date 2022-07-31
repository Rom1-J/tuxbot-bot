"""
tuxbot.cogs.Network.functions.providers.abc
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Abstract Class for providers.
"""

from abc import ABC


class Provider(ABC):
    """Abstract Class for providers."""

    def __init__(self, apikey: str | None = None):
        self.apikey = apikey

    # pylint: disable=unused-argument
    # noinspection PyMissingOrEmptyDocstring
    async def fetch(self, ip: str) -> tuple[str, dict | str]:
        ...
