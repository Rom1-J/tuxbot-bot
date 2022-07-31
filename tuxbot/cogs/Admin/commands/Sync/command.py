"""
tuxbot.cogs.Admin.commands.Sync.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Command to sync Tuxbot
"""
from typing import Literal

import discord
from discord.ext import commands

from tuxbot.core.Tuxbot import Tuxbot


class SyncCommand(commands.Cog):
    """Sync tuxbot"""

    def __init__(self, bot: Tuxbot):
        self.bot = bot

    # =========================================================================
    # =========================================================================

    @commands.command("sync")
    async def _sync(
        self,
        ctx: commands.Context,
        guilds: commands.Greedy[discord.Object],
        spec: Literal["~"] | None = None,
    ) -> None:
        if not guilds:
            if spec == "~":
                fmt = await ctx.bot.tree.sync(guild=ctx.guild)
            else:
                fmt = await ctx.bot.tree.sync()

            await ctx.send(
                f"Synced {len(fmt)} commands "
                + ("globally" if spec is not None else "to the current guild.")
            )
            return

        assert guilds is not None

        fmt = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                fmt += 1

        await ctx.send(f"Synced the tree to {fmt}/{len(guilds)} guilds.")
