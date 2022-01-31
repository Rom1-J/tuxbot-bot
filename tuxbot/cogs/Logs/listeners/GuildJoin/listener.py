"""
tuxbot.cogs.Logs.listeners.GuildJoin.listener
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Listener whenever a guild is joined
"""
import discord
from discord.ext import commands

from tuxbot.core.Tuxbot import Tuxbot


class GuildJoin(commands.Cog):
    """Listener whenever a guild is joined"""

    def __init__(self, bot: Tuxbot):
        self.bot = bot

    @commands.Cog.listener(name="on_guild_join")
    async def _on_guild_join(
            self, guild: discord.Guild
    ):  # pylint: disable=unused-argument
        self.bot.statsd.gauge(
            "guilds",
            value=len(self.bot.guilds),
        )

        if guild_model := await self.bot.models["Guild"].get_or_none(
                id=guild.id
        ):
            guild_model.deleted = False
            await guild_model.save()
        else:
            guild_model = await self.bot.models["Guild"].create(
                id=guild.id,
                moderators=[],
                moderator_roles=[],
                deleted=False
            )
            await guild_model.save()
