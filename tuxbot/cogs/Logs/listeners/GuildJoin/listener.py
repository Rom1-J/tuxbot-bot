"""
tuxbot.cogs.Logs.listeners.GuildJoin.listener
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.

Listener whenever a guild is joined
"""
import typing

import discord
from discord.ext import commands

from tuxbot.core.models.guild import GuildModel
from tuxbot.core.tuxbot import Tuxbot


class GuildJoin(commands.Cog):
    """Listener whenever a guild is joined."""

    def __init__(self: typing.Self, bot: Tuxbot) -> None:
        self.bot = bot

    # =========================================================================
    # =========================================================================

    @commands.Cog.listener(name="on_guild_join")
    async def _on_guild_join(self: typing.Self, guild: discord.Guild) -> None:
        self.bot.statsd.gauge(
            "guilds",
            value=len(self.bot.guilds),
        )

        self.bot.logger.info(
            "[GuildJoin] Tuxbot added to the guild '%s'.", guild.name
        )

        if guild_model := await GuildModel.get_or_none(id=guild.id):
            guild_model.deleted = False
            await guild_model.save()
        else:
            guild_model = await GuildModel.create(
                id=guild.id, moderators=[], moderator_roles=[], deleted=False
            )
            await guild_model.save()

        self.bot.cached_config[guild.id] = {}
