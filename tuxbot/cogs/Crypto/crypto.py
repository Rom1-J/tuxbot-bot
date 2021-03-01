import functools
import logging
import discord
from discord.ext import commands

from tuxbot.cogs.Crypto.functions.extractor import extract
from tuxbot.cogs.Crypto.functions.sync import encode
from tuxbot.core.bot import Tux
from tuxbot.core.i18n import (
    Translator,
)
from tuxbot.core.utils.functions.extra import group_extra, ContextPlus


log = logging.getLogger("tuxbot.cogs.Crypto")
_ = Translator("Crypto", __file__)


class Crypto(commands.Cog, name="Crypto"):
    def __init__(self, bot: Tux):
        self.bot = bot

    @group_extra(name="ralgo")
    async def _ralgo(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send_help("ralgo")

    @_ralgo.command(name="encode")
    async def _ralgo_encode(self, ctx: ContextPlus, *, data: str = None):
        try:
            params = await extract(ctx.message.attachments, data, 10000)
        except ValueError:
            return await ctx.send("Invalid data provided")

        async with ctx.typing():
            output = await self.bot.loop.run_in_executor(
                None, functools.partial(encode, params)
            )

        if params["graphical"]:
            return await ctx.send(file=output)

        await ctx.send(output)

    @_ralgo.command(name="decode")
    async def _ralgo_decode(self, ctx: ContextPlus, *, data: str = None):
        try:
            params = await extract(ctx.message.attachments, data, 100000)
        except ValueError:
            return await ctx.send("Invalid data provided")

        async with ctx.typing():
            output = await self.bot.loop.run_in_executor(
                None, functools.partial(encode, params)
            )

        if isinstance(output, discord.File):
            return await ctx.send(file=output)

        await ctx.send(output)
