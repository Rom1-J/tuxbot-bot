"""
tuxbot.cogs.Auto.listeners.RawReactionAdd.workers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.

"""
import typing

import discord

from tuxbot.core.tuxbot import Tuxbot

from .auto_pin import AutoPin


class Worker:
    """Autoworker."""

    def __init__(self: typing.Self, bot: Tuxbot) -> None:
        self.bot = bot

        self.__workers = [
            AutoPin(self.bot),
        ]

    async def runs(
        self: typing.Self, payload: discord.RawReactionActionEvent
    ) -> None:
        """Run all automatics workers."""
        for worker in self.__workers:
            await worker.process(payload)
