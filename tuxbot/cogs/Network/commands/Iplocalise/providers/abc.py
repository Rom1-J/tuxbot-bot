"""
tuxbot.cogs.Network.functions.providers.abc
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.

Abstract Class for providers.
"""
import typing
from abc import ABC, abstractmethod


class Provider(ABC):
    """Abstract Class for providers."""

    def __init__(self: typing.Self, apikey: str | None = None) -> None:
        self.apikey = apikey

    @abstractmethod
    async def fetch(
        self: typing.Self, ip: str
    ) -> tuple[str, dict[str, typing.Any] | str]:
        ...
