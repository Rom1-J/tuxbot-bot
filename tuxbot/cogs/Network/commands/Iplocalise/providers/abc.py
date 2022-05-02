"""
tuxbot.cogs.Network.functions.providers.abc
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Abstract Class for providers.
"""

from abc import ABC
from typing import Optional, Tuple, Union


class Provider(ABC):
    """Abstract Class for providers."""

    def __init__(self, apikey: Optional[str] = None):
        self.apikey = apikey

    # pylint: disable=unused-argument
    # noinspection PyMissingOrEmptyDocstring
    async def fetch(self, ip: str) -> Tuple[str, Union[dict, str]]:
        ...
