"""
tuxbot.cogs.Polls.listeners.RawReactionAdd.listener
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.

Listener whenever a reaction is added
"""
import typing

import discord
from discord.ext import commands

from tuxbot.cogs.Polls.commands.Poll.command import PollCommand
from tuxbot.core.tuxbot import Tuxbot


class RawReactionAdd(commands.Cog):
    """Listener whenever a reaction is added."""

    def __init__(self: typing.Self, bot: Tuxbot) -> None:
        self.bot = bot

    # =========================================================================
    # =========================================================================

    @commands.Cog.listener(name="on_raw_reaction_add")
    async def _on_raw_reaction_add(
        self: typing.Self, pld: discord.RawReactionActionEvent
    ) -> None:
        if pld.member == self.bot.user:
            return

        if pld.emoji.name not in self.bot.utils.emotes.ALPHABET:
            return

        if poll := await PollCommand.get_poll(pld.message_id):
            choices = await poll.choices.all()

            if (
                pld.emoji.name
                not in self.bot.utils.emotes.ALPHABET[: len(choices)]
            ):
                return

            if not (
                _choice := [c for c in choices if c.label == pld.emoji.name]
            ):
                return

            choice = _choice[0]

            choice.checked += 1
            await choice.save()

            await PollCommand.update_poll(self.bot, poll)
