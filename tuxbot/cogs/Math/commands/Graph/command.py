"""
tuxbot.cogs.Math.commands.Graph.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Decompose math expression as graphic
"""

from textwrap import shorten

import discord
from discord.ext import commands
from sympy import pretty

from tuxbot.core.Tuxbot import Tuxbot

from .converters.ExprConverter import ExprConverter
from .Graph import get_graph_bytes


class GraphCommand(commands.Cog):
    """Decompose math expression"""

    def __init__(self, bot: Tuxbot):
        self.bot = bot

    @commands.command(name="graph")
    async def _graph(self, ctx: commands.Context, *, expr: ExprConverter):
        expr, parsed_expr = expr

        if parsed_expr is None:
            return await ctx.send("Unable to parse this expression")

        graph_bytes = await get_graph_bytes(self.bot.loop, parsed_expr)
        file = discord.File(graph_bytes, "output.png")

        text = pretty(parsed_expr, use_unicode=True)

        e = discord.Embed(
            title=shorten(discord.utils.escape_markdown(expr), 255)
        )
        e.set_image(url="attachment://output.png")
        e.set_footer(
            text=str(ctx.author), icon_url=ctx.author.display_avatar.url
        )

        await ctx.send(f"```\n{text}```", embed=e, file=file)
