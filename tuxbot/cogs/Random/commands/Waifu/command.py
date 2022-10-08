"""
tuxbot.cogs.Random.commands.Waifu.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Get a random waifu generated from pre-trained model
"""
import asyncio

import discord
import replicate
from discord.ext import commands
from replicate.exceptions import ModelError

from tuxbot.abc.TuxbotABC import TuxbotABC
from tuxbot.core.Tuxbot import Tuxbot

from ..exceptions import APIException


class WaifuCommand(commands.Cog):
    """Random waifu picture"""

    def __init__(self, bot: Tuxbot) -> None:
        self.bot = bot

        client = replicate.Client(
            api_token=self.bot.config["Random"].get("replicate_key")
        )
        self.model = client.models.get("cjwbw/waifu-diffusion")

    # =========================================================================
    # =========================================================================

    async def __generate_waifu(self, keywords: str) -> tuple[str, str | None]:
        keywords = keywords.lower()

        def _get_waifu(_keywords: str) -> str:
            return str(self.model.predict(prompt=_keywords)[0])

        try:
            output = await asyncio.wait_for(
                asyncio.get_running_loop().run_in_executor(
                    None, _get_waifu, keywords
                ),
                timeout=60 * 1,
            )
            return keywords, output
        except asyncio.exceptions.TimeoutError:
            return keywords, None
        except ModelError as e:
            raise APIException(str(e))

    # =========================================================================
    # =========================================================================

    @commands.command(name="waifu", aliases=["randomwaifu"])
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def _waifu_generate(
        self, ctx: commands.Context[TuxbotABC], *, keywords: str
    ) -> None:
        q, image = await self.__generate_waifu(keywords)

        e = discord.Embed(title=f"Using keywords: {q}")

        if image:
            e.set_image(url=image)

        e.set_footer(
            text="Powered by https://replicate.com/cjwbw/waifu-diffusion"
        )

        await ctx.send(embed=e)
