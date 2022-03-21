"""
tuxbot.cogs.Logs.listeners.GuildRemove.listener
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Listener whenever a guild is leaved
"""
import discord
from discord.ext import commands

from tuxbot.core.Tuxbot import Tuxbot


class GuildRemove(commands.Cog):
    """Listener whenever a guild is leaved"""

    def __init__(self, bot: Tuxbot):
        self.bot = bot

    # =========================================================================
    # =========================================================================

    @commands.Cog.listener(name="on_guild_remove")
    async def _on_guild_remove(
        self, guild: discord.Guild
    ):  # pylint: disable=unused-argument
        self.bot.statsd.gauge(
            "guilds",
            value=len(self.bot.guilds),
        )

        self.bot.logger.info(
            "[GuildRemove] Tuxbot removed from the guild '%s'.", guild.name
        )

        if guild_model := await self.bot.models["Guild"].get_or_none(
            id=guild.id
        ):
            guild_model.deleted = True
            await guild_model.save()
        else:
            guild_model = await self.bot.models["Guild"].create(
                id=guild.id, moderators=[], moderator_roles=[], deleted=True
            )
            await guild_model.save()
