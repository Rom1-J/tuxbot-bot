"""
tuxbot.cogs.Utils.commands.Credits.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.

Shows information about tuxbot creators
"""
import typing

import discord
from discord.ext import commands

from tuxbot.abc.tuxbot_abc import TuxbotABC
from tuxbot.core.tuxbot import Tuxbot


class CreditsCommand(commands.Cog):
    """Shows tuxbot's creators."""

    def __init__(self: typing.Self, bot: Tuxbot) -> None:
        self.bot = bot

    # =========================================================================
    # =========================================================================

    @commands.command(
        name="credits", aliases=["contributors", "authors", "credit"]
    )
    async def _credits(
        self: typing.Self, ctx: commands.Context[TuxbotABC]
    ) -> None:
        e = discord.Embed(
            title="Contributors",
            color=self.bot.utils.colors.EMBED_BORDER,
        )

        e.add_field(
            name="**aspheric_** ",
            value=(
                "> • [github](https://github.com/Rom1-J)\n"
                "> • [gitea](https://git.gnous.eu/Romain)\n"
                "> • romain@gnous.eu"
            ),
            inline=True,
        )
        e.add_field(
            name="**outout** ",
            value=(
                "> • [gitea](https://git.gnous.eu/mael)\n"
                "> • [@outoutxyz](https://twitter.com/outouxyz)\n"
                "> • mael@gnous.eu"
            ),
            inline=True,
        )

        await ctx.send(embed=e)
