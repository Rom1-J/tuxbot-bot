import logging

import discord
from discord.ext import commands
from structured_config import ConfigFile

from tuxbot.core.bot import Tux
from tuxbot.core.i18n import Translator
from tuxbot.core.utils.data_manager import cogs_data_path
from tuxbot.core.utils.functions.extra import (
    ContextPlus,
    command_extra,
)

from .config import MathConfig
from .functions.converters import LatexConverter
from .functions.utils import get_latex_bytes, Wolfram, clean_query

log = logging.getLogger("tuxbot.cogs.Math")
_ = Translator("Math", __file__)


class Math(commands.Cog):
    def __init__(self, bot: Tux):
        self.bot = bot
        self.__config: MathConfig = ConfigFile(
            str(cogs_data_path("Math") / "config.yaml"),
            MathConfig,
        ).config

        self.WA = Wolfram(self.bot.loop, self.__config.WolframAlphaKey)

    async def cog_before_invoke(self, ctx: ContextPlus):
        await ctx.trigger_typing()

    # =========================================================================
    # =========================================================================

    @commands.cooldown(1, 10, commands.BucketType.user)
    @command_extra(name="wolf", aliases=["wolfram"], deletable=True)
    async def _wolf(self, ctx: ContextPlus, *, query: str):
        await self.WA.get_client()
        q, result = await self.WA.query(query)

        if result is None:
            return await ctx.send(
                _("No results found...", ctx, self.bot.config)
            )

        images = await self.WA.get_images(result)
        image = await self.WA.merge_images(images, self.WA.width(result))

        e = discord.Embed()

        if q != query:
            e.title = _(
                "Using closest Wolfram|Alpha interpretation: {}",
                ctx,
                self.bot.config,
            ).format(q)

            query = q

        e.set_image(url="attachment://output.png")
        e.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        e.add_field(
            name="<:wolframalpha:851473526992797756> WolframAlpha",
            value=(
                f"[{discord.utils.escape_markdown(query)}]"
                f"(https://www.wolframalpha.com/input/?i={clean_query(query)})"
            ),
        )

        file = discord.File(image, "output.png")

        await ctx.send(
            embed=e, file=file, reference=ctx.message, mention_author=False
        )

    # =========================================================================

    @command_extra(name="latex", aliases=["tex"], deletable=True)
    async def _latex(self, ctx: ContextPlus, *, latex: LatexConverter):
        latex_bytes = await get_latex_bytes(self.bot.loop, str(latex))
        latex_clean = discord.utils.escape_mentions(latex[2:-2])

        file = discord.File(latex_bytes, "output.png")

        e = discord.Embed(description=f"```{latex_clean}```")
        e.set_image(url="attachment://output.png")

        await ctx.send(embed=e, file=file)
