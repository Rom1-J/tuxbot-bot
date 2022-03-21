"""
tuxbot.cogs.Math.commands.Graph.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Decompose math expression as graphic
"""

import asyncio
import io
from textwrap import shorten

import discord
from discord.ext import commands
from graphviz import Source
from sympy import dotprint, pretty

from tuxbot.core.Tuxbot import Tuxbot

from ...converters.ExprConverter import ExprConverter


class GraphCommand(commands.Cog):
    """Decompose math expression"""

    def __init__(self, bot: Tuxbot):
        self.bot = bot

    # =========================================================================
    # =========================================================================

    @staticmethod
    async def __get_graph_bytes(expr) -> io.BytesIO:
        """Generate graph as byte format from given expr"""

        def _get_graph_bytes(_expr):
            digraph = dotprint(expr)
            raw_bytes = Source(digraph).pipe(format="png")

            return io.BytesIO(raw_bytes)

        return await asyncio.get_running_loop().run_in_executor(
            None, _get_graph_bytes, expr
        )

    # =========================================================================
    # =========================================================================

    @commands.command(name="graph")
    async def _graph(self, ctx: commands.Context, *, expr: ExprConverter):
        expr, parsed_expr = expr

        if parsed_expr is None:
            return await ctx.send("Unable to parse this expression")

        graph_bytes = await self.__get_graph_bytes(parsed_expr)
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
