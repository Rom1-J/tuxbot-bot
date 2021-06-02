import logging

import discord
from discord.ext import commands
from structured_config import ConfigFile

from tuxbot.core.bot import Tux
from tuxbot.core.i18n import (
    Translator,
)
from tuxbot.core.utils.data_manager import cogs_data_path
from tuxbot.core.utils.functions.extra import (
    ContextPlus,
    command_extra,
)

from .config import MathConfig
from .functions.converters import LatexConverter
from .functions.utils import get_latex_bytes

log = logging.getLogger("tuxbot.cogs.Math")
_ = Translator("Math", __file__)


class Math(commands.Cog):
    def __init__(self, bot: Tux):
        self.bot = bot
        self.__config: MathConfig = ConfigFile(
            str(cogs_data_path("Math") / "config.yaml"),
            MathConfig,
        ).config

    # =========================================================================
    # =========================================================================

    @command_extra(name="wolf", aliases=["wolfram"], deletable=True)
    async def _wolf(self, ctx: ContextPlus):
        _ = ctx, self.__config.WolframAlphaKey

    # =========================================================================

    @command_extra(name="latex", aliases=["tex"], deletable=True)
    async def _latex(self, ctx: ContextPlus, *, latex: LatexConverter):
        latex_bytes = await get_latex_bytes(self.bot.loop, str(latex))
        latex_clean = latex[2:-2]

        file = discord.File(latex_bytes, "output.png")

        e = discord.Embed(description=f"```{latex_clean}```")
        e.set_image(url="attachment://output.png")

        await ctx.send(embed=e, file=file)
