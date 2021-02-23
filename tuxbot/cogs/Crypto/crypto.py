import logging
from io import BytesIO

import discord
from discord.ext import commands
from ralgo.ralgo import Ralgo

from tuxbot.cogs.Crypto.functions.extractor import extract
from tuxbot.cogs.Crypto.functions.file import find_ext
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
            params = await extract(ctx.message.attachments, data, 100000)
        except ValueError:
            return await ctx.send("Invalid data provided")

        statement = Ralgo(params["message"])
        params = params["params"]
        encoded = statement.encode(chars=params["chars"])

        if params["compressed"]:
            return await ctx.send(str(encoded.compress()))
        if params["graphical"]:
            output = encoded.graphical().encode()
            file = discord.File(BytesIO(output.to_bytes()), "output.png")

            return await ctx.send(file=file)

        await ctx.send(str(encoded))

    @_ralgo.command(name="decode")
    async def _ralgo_decode(self, ctx: ContextPlus, *, data: str = None):
        try:
            params = await extract(ctx.message.attachments, data, 5000000)
        except ValueError:
            return await ctx.send("Invalid data provided")

        statement = Ralgo(params["message"])
        params = params["params"]

        if params["graphical"]:
            output = Ralgo(statement.graphical().decode()).decode()

            output = discord.utils.escape_markdown(str(output))
            output = discord.utils.escape_mentions(output)
        elif params["compressed"]:
            output = Ralgo(statement.decompress()).decode()
        else:
            output = statement.decode(chars=params["chars"])

        if isinstance(output, bytes):
            file = discord.File(BytesIO(output), f"output.{find_ext(output)}")

            return await ctx.send(file=file)

        output = discord.utils.escape_markdown(str(output))
        output = discord.utils.escape_mentions(output)

        await ctx.send(output if len(output) > 0 else "no content...")
