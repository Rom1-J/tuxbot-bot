"""
tuxbot.cogs.Admin.commands.Sync.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Command to sync Tuxbot
"""
import typing

import discord
from discord.ext import commands

from tuxbot.abc.TuxbotABC import TuxbotABC
from tuxbot.core.Tuxbot import Tuxbot


class SyncCommand(commands.Cog):
    """Sync tuxbot"""

    def __init__(self, bot: Tuxbot) -> None:
        self.bot = bot

    # =========================================================================
    # =========================================================================

    @commands.command("sync")
    async def _sync(
        self,
        ctx: commands.Context[TuxbotABC],
        guilds: commands.Greedy[discord.Object],
        spec: typing.Literal["~"] | None = None,
    ) -> None:
        if not guilds and ctx.guild:
            if spec == "~":
                fmt = await ctx.bot.tree.sync(guild=ctx.guild)
            else:
                fmt = await ctx.bot.tree.sync()

            await ctx.send(
                f"Synced {len(fmt)} commands "
                + ("globally" if spec is not None else "to the current guild.")
            )
            return

        if not guilds:
            return

        i = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                i += 1

        await ctx.send(f"Synced the tree to {i}/{len(guilds)} guilds.")
