"""
tuxbot.cogs.Auto.listeners.Message.workers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.

"""
import typing

import discord

from tuxbot.core.tuxbot import Tuxbot

from .auto_quote import AutoQuote


class Worker:
    """Autoworker."""

    def __init__(self: typing.Self, bot: Tuxbot) -> None:
        self.bot = bot

        self.__workers = [
            AutoQuote(self.bot),
        ]

    async def runs(self: typing.Self, message: discord.Message) -> None:
        """Run all automatics workers."""
        for worker in self.__workers:
            await worker.process(message)
