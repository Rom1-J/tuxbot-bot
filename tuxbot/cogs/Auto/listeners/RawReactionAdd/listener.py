"""
tuxbot.cogs.Auto.listeners.RawReactionAdd.listener
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.

Listener whenever reaction is added
"""
import typing

import discord
from discord.ext import commands

from tuxbot.core.tuxbot import Tuxbot

from .workers import Worker


class RawReactionAdd(commands.Cog):
    """Listener whenever reaction is added."""

    def __init__(self: typing.Self, bot: Tuxbot) -> None:
        self.bot = bot
        self.worker = Worker(self.bot)

    # =========================================================================
    # =========================================================================

    @commands.Cog.listener(name="on_raw_reaction_add")
    async def _on_raw_reaction_add(
        self: typing.Self, payload: discord.RawReactionActionEvent
    ) -> None:
        await self.worker.runs(payload)
