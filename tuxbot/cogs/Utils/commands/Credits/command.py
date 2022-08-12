"""
tuxbot.cogs.Utils.commands.Credits.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Shows information about tuxbot creators
"""

import discord
from discord.ext import commands

from tuxbot.abc.TuxbotABC import TuxbotABC
from tuxbot.core.Tuxbot import Tuxbot


class CreditsCommand(commands.Cog):
    """Shows tuxbot's creators"""

    def __init__(self, bot: Tuxbot) -> None:
        self.bot = bot

    # =========================================================================
    # =========================================================================

    @commands.command(
        name="credits", aliases=["contributors", "authors", "credit"]
    )
    async def _credits(self, ctx: commands.Context[TuxbotABC]) -> None:
        e = discord.Embed(
            title="Contributors",
            color=self.bot.utils.colors.EMBED_BORDER.value,
        )

        e.add_field(
            name="**Romain#5117** ",
            value=(
                "> • [github](https://github.com/Rom1-J)\n"
                "> • [gitlab](https://gitlab.gnous.eu/Romain)\n"
                "> • romain@gnous.eu"
            ),
            inline=True,
        )
        e.add_field(
            name="**Outout#4039** ",
            value=(
                "> • [gitea](https://git.gnous.eu/mael)\n"
                "> • [@outoutxyz](https://twitter.com/outouxyz)\n"
                "> • mael@gnous.eu"
            ),
            inline=True,
        )

        await ctx.send(embed=e)
