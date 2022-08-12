"""
tuxbot.cogs.Logs.listeners.Message.workers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import discord

from tuxbot.core.Tuxbot import Tuxbot

from .AutoQuote import AutoQuote


class Worker:
    """Autoworker"""

    def __init__(self, bot: Tuxbot) -> None:
        self.bot = bot

        self.__workers = [
            AutoQuote(self.bot),
        ]

    async def runs(self, message: discord.Message) -> None:
        """Run all automatics workers"""

        for worker in self.__workers:
            await worker.process(message)
