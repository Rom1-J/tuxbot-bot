"""
tuxbot.cogs.Utils.commands.Source.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Gives tuxbot sources
"""
import inspect
import os

from discord.ext import commands

from tuxbot.abc.TuxbotABC import TuxbotABC
from tuxbot.core.Tuxbot import Tuxbot


class SourceCommand(commands.Cog):
    """Gives tuxbot sources"""

    def __init__(self, bot: Tuxbot) -> None:
        self.bot = bot

        self.github_url = "https://github.com/Rom1-J/tuxbot-bot/"

    # =========================================================================
    # =========================================================================

    @commands.command(name="source", aliases=["sources"])
    async def _source(
        self, ctx: commands.Context[TuxbotABC], *, name: str | None = None
    ) -> None:
        if not name:
            await ctx.send(self.github_url)
            return

        cmd = self.bot.get_command(name)

        if cmd:
            src = cmd.callback.__code__
            rpath = src.co_filename
        else:
            await ctx.send(f"Unable to find `{name}`")
            return

        try:
            lines, start_line = inspect.getsourcelines(src)
        except OSError:
            await ctx.send(f"Unable to fetch lines for `{name}`")
            return

        if "venv" in rpath:
            location = (
                os.path.relpath(rpath)
                .replace("\\", "/")
                .split("site-packages/")[-1]
                .lstrip("/")
            )
        else:
            location = rpath.split("tuxbot_bot")[-1].lstrip("/")

        final_url = (
            f"{self.github_url}/tree/master/{location}#L{start_line}"
            f"-L{start_line + len(lines) - 1}"
        )

        await ctx.send(final_url)
