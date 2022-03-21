"""
tuxbot.cogs.Math.commands.Wolf.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Shows result of WolframAlpha request for given query
"""

import base64
import io

import discord
import yaml
from discord.ext import commands

from tuxbot.core.Tuxbot import Tuxbot

from .WolframAlpha import WolframAlpha


class WolfCommand(commands.Cog):
    """Shows WolframAlpha result"""

    def __init__(self, bot: Tuxbot):
        self.bot = bot

        self.WA = WolframAlpha(self.bot.config["Math"].get("wolframalpha_key"))

    # =========================================================================
    # =========================================================================

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="wolf", aliases=["wolfram"])
    async def _wolf(self, ctx: commands.Context, *, query: str):
        await self.WA.get_client()

        if cache := await self.bot.redis.get(self.bot.utils.gen_key(query)):
            res = yaml.load(cache, Loader=yaml.Loader)

            q = res["q"]
            image = io.BytesIO(base64.b64decode(res["image"]))
        else:
            q, result = await self.WA.query(query)

            if result is None:
                return await ctx.send("No results found...")

            images = await self.WA.get_images(result)
            image = await self.WA.merge_images(images, self.WA.width(result))

            await self.bot.redis.set(
                self.bot.utils.gen_key(query),
                str(
                    {
                        "q": q,
                        "image": base64.b64encode(image.getvalue()).decode(),
                    }
                ),
                ex=3600 * 12,  # cache for 12h
            )

            image.seek(0)

        e = discord.Embed()

        if q != query:
            e.title = f"Using closest Wolfram|Alpha interpretation: {q}"
            query = q

        e.set_image(url="attachment://output.png")
        e.set_footer(
            text=str(ctx.author), icon_url=ctx.author.display_avatar.url
        )
        e.add_field(
            name="<:wolframalpha:851473526992797756> WolframAlpha",
            value=(
                f"[{discord.utils.escape_markdown(query)}]"
                f"(https://www.wolframalpha.com/input/?i="
                f"{WolframAlpha.clean_query(query)})"
            ),
        )

        file = discord.File(image, "output.png")

        await ctx.send(embed=e, file=file)
