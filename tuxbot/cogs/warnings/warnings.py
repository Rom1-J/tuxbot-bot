from typing import Union

import discord
from discord.ext import commands

from tuxbot.core import checks
from tuxbot.core.bot import Tux


class Warnings(commands.Cog, name="Warnings"):
    def __init__(self, bot: Tux):
        self.bot = bot

    @commands.group(name="warn", alias=["warning"])
    @commands.guild_only()
    @checks.is_mod()
    async def _warn(self, ctx: commands.Context):
        division_by_zero = 1 / 0

    @_warn.command(name="add")
    @commands.guild_only()
    async def _warn_add(
        self,
        ctx: commands.Context,
        member: Union[discord.User, discord.Member],
        reason: str,
    ):
        pass

    @_warn.command(name="delete", aliases=["del", "remove"])
    @commands.guild_only()
    async def action_del(self, ctx: commands.Context, warn_id: int, reason: str = ""):
        pass

    @_warn.command(name="list", aliases=["all"])
    @commands.guild_only()
    async def action_del(
        self, ctx: commands.Context, member: Union[discord.User, discord.Member] = None
    ):
        pass
