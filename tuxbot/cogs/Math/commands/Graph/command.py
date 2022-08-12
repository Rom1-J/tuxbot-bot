"""
tuxbot.cogs.Math.commands.Graph.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Decompose math expression as graphic
"""

import asyncio
import io
import typing
from textwrap import shorten

import discord
from discord.ext import commands
from graphviz import Source
from sympy import dotprint, pretty

from tuxbot.abc.TuxbotABC import TuxbotABC
from tuxbot.core.Tuxbot import Tuxbot

from ...converters.ExprConverter import ExprConverter


class GraphCommand(commands.Cog):
    """Decompose math expression"""

    def __init__(self, bot: Tuxbot) -> None:
        self.bot = bot

    # =========================================================================
    # =========================================================================

    @staticmethod
    async def __get_graph_bytes(expr: typing.Any) -> io.BytesIO:
        """Generate graph as byte format from given expr"""

        def _get_graph_bytes(_expr: typing.Any) -> io.BytesIO:
            digraph = dotprint(expr)  # type: ignore[no-untyped-call]
            raw_bytes = Source(digraph).pipe(format="png")

            return io.BytesIO(raw_bytes)

        return await asyncio.get_running_loop().run_in_executor(
            None, _get_graph_bytes, expr
        )

    # =========================================================================
    # =========================================================================

    @commands.command(name="graph")
    async def _graph(
        self, ctx: commands.Context[TuxbotABC], *, expr: str
    ) -> None:
        expr, parsed_expr = await ExprConverter().convert(ctx, expr)

        if parsed_expr is None:
            await ctx.send("Unable to parse this expression")
            return

        graph_bytes = await self.__get_graph_bytes(parsed_expr)
        file = discord.File(graph_bytes, "output.png")

        text = pretty(parsed_expr, use_unicode=True)

        e = discord.Embed(
            title=shorten(discord.utils.escape_markdown(str(expr)), 255)
        )
        e.set_image(url="attachment://output.png")
        e.set_footer(
            text=str(ctx.author), icon_url=ctx.author.display_avatar.url
        )

        await ctx.send(f"```\n{text}```", embed=e, file=file)
