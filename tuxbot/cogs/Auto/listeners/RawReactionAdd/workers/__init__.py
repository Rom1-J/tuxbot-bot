"""
tuxbot.cogs.Auto.listeners.RawReactionAdd.workers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import discord

from tuxbot.core.Tuxbot import Tuxbot

from .AutoPin import AutoPin


class Worker:
    """Autoworker"""

    def __init__(self, bot: Tuxbot) -> None:
        self.bot = bot

        self.__workers = [
            AutoPin(self.bot),
        ]

    async def runs(self, payload: discord.RawReactionActionEvent) -> None:
        """Run all automatics workers"""

        for worker in self.__workers:
            await worker.process(payload)
