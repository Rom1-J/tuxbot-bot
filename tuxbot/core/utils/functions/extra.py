import asyncio

import discord
from discord import Embed
from discord.ext import commands, flags

from rich.console import Console

console = Console()

TOKEN_REPLACEMENT = "whoops, leaked token"


class ContextPlus(commands.Context):
    async def send(self, *args, content=None, **kwargs):
        if content is not None:
            content = content.replace(
                self.bot.config.Core.token, TOKEN_REPLACEMENT
            )
        if kwargs.get("embed"):
            embed = kwargs.get("embed").to_dict()
            for key, value in embed.items():
                if isinstance(value, (str, bytes)):
                    embed[key] = value.replace(
                        self.bot.config.Core.token, TOKEN_REPLACEMENT
                    )
            kwargs["embed"] = Embed.from_dict(embed)

        if (
            hasattr(self.command, "deletable") and self.command.deletable
        ) or kwargs.pop("deletable", False):
            message = await super().send(content, *args, **kwargs)
            await message.add_reaction("🗑")

            def check(reaction: discord.Reaction, user: discord.User):
                return (
                    user == self.author
                    and str(reaction.emoji) == "🗑"
                    and reaction.message.id == message.id
                )

            try:
                await self.bot.wait_for(
                    "reaction_add", timeout=42.0, check=check
                )
            except asyncio.TimeoutError:
                await message.remove_reaction("🗑", self.bot.user)
            else:
                await message.delete()
            return message

        return await super().send(content, *args, **kwargs)


class CommandPLus(flags.FlagCommand):
    def __init__(self, function, **kwargs):
        super().__init__(function, **kwargs)
        self.deletable = kwargs.pop("deletable", True)


def command_extra(*args, **kwargs):
    return commands.command(*args, **kwargs, cls=CommandPLus)


class GroupPlus(flags.FlagGroup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.deletable = kwargs.pop("deletable", True)


def group_extra(*args, **kwargs):
    return commands.group(*args, **kwargs, cls=GroupPlus)
