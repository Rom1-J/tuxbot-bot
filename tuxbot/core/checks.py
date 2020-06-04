from typing import Awaitable, Dict

import discord
from discord.ext import commands
from discord.ext.commands import (
    bot_has_permissions,
    has_permissions,
    is_owner,
)

from tuxbot.core.utils.functions.extra import ContextPlus

__all__ = [
    "bot_has_permissions",
    "has_permissions",
    "is_owner",
    "is_mod",
    "is_admin",
    "check_permissions",
    "guild_owner_or_permissions",
]


def is_mod():
    async def pred(ctx):
        if await ctx.bot.is_owner(ctx.author):
            return True
        permissions: discord.Permissions = ctx.channel.permissions_for(ctx.author)
        return permissions.manage_messages

    return commands.check(pred)


def is_admin():
    async def pred(ctx):
        if await ctx.bot.is_owner(ctx.author):
            return True
        permissions: discord.Permissions = ctx.channel.permissions_for(ctx.author)
        return permissions.administrator

    return commands.check(pred)


async def check_permissions(ctx: "ContextPlus", **perms: Dict[str, bool]):
    if await ctx.bot.is_owner(ctx.author):
        return True

    elif not perms:
        return False
    resolved = ctx.channel.permissions_for(ctx.author)

    return all(
        getattr(resolved, name, None) == value for name, value in perms.items()
    )


def guild_owner_or_permissions(**perms: Dict[str, bool]):
    async def pred(ctx):
        if ctx.author is ctx.guild.owner:
            return True
        return await check_permissions(ctx, **perms)

    return commands.check(pred)
