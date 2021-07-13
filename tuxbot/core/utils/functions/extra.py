import asyncio

import aiohttp
import discord
from discord import Embed
from discord.ext import commands

TOKEN_REPLACEMENT = "■" * 13
PASSWORD_REPLACEMENT = "■" * 13
IP_REPLACEMENT = "■" * 13


class ContextPlus(commands.Context):
    # noinspection PyTypedDict
    async def send(
        self,
        content: str = None,
        *,
        embed: discord.Embed = None,
        deletable=True,
        **kwargs
    ):
        from tuxbot.core.utils.functions.utils import (
            replace_in_dict,
            replace_in_list,
        )

        # todo: rewrite replacements
        if content:
            content = (
                content.replace(self.bot.config.Core.token, TOKEN_REPLACEMENT)
                .replace(
                    self.bot.config.Core.Database.password,
                    PASSWORD_REPLACEMENT,
                )
                .replace(self.bot.config.Core.ip, IP_REPLACEMENT)
                .replace(self.bot.config.Core.ip6, IP_REPLACEMENT)
            )

            if len(content) > 1800:
                content = "output too long..."
        if embed:
            e = embed.to_dict()
            for key, value in e.items():
                if isinstance(value, str):
                    # skipcq
                    e[key] = (
                        value.replace(
                            self.bot.config.Core.token, TOKEN_REPLACEMENT
                        )
                        .replace(
                            self.bot.config.Core.Database.password,
                            PASSWORD_REPLACEMENT,
                        )
                        .replace(self.bot.config.Core.ip, IP_REPLACEMENT)
                        .replace(self.bot.config.Core.ip6, IP_REPLACEMENT)
                    )
                elif isinstance(value, list):
                    # skipcq
                    e[key] = replace_in_list(
                        value, self.bot.config.Core.token, TOKEN_REPLACEMENT
                    )
                    # skipcq
                    e[key] = replace_in_list(
                        e[key],
                        self.bot.config.Core.Database.password,
                        PASSWORD_REPLACEMENT,
                    )
                    # skipcq
                    e[key] = replace_in_list(
                        e[key], self.bot.config.Core.ip, IP_REPLACEMENT
                    )
                    # skipcq
                    e[key] = replace_in_list(
                        e[key], self.bot.config.Core.ip6, IP_REPLACEMENT
                    )
                elif isinstance(value, dict):
                    # skipcq
                    e[key] = replace_in_dict(
                        value, self.bot.config.Core.token, TOKEN_REPLACEMENT
                    )
                    # skipcq
                    e[key] = replace_in_dict(
                        e[key],
                        self.bot.config.Core.Database.password,
                        PASSWORD_REPLACEMENT,
                    )
                    # skipcq
                    e[key] = replace_in_dict(
                        e[key], self.bot.config.Core.ip, IP_REPLACEMENT
                    )
                    # skipcq
                    e[key] = replace_in_dict(
                        e[key], self.bot.config.Core.ip6, IP_REPLACEMENT
                    )
            embed = Embed.from_dict(e)

        if (
            hasattr(self.command, "deletable") and self.command.deletable
        ) and deletable:
            message = await super().send(
                content=content,
                embed=embed,
                reference=self.message,
                mention_author=False,
                **kwargs,
            )
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
                try:
                    await message.remove_reaction("🗑", self.bot.user)
                except discord.HTTPException:
                    return None
            else:
                try:
                    await self.message.add_reaction("✅")
                except discord.HTTPException:
                    pass

                try:
                    await message.delete()
                except discord.HTTPException:
                    pass

            return message

        return await super().send(
            content=content,
            embed=embed,
            reference=self.message,
            mention_author=False,
            **kwargs,
        )

    async def ask(
        self,
        content=None,
        *,
        embed=None,
        emotes=None,
        name=None,
        possibilities=None,
        timeout=10,
        **kwargs
    ):
        message = await self.send(
            content=content, embed=embed, deletable=False
        )

        for emote in emotes:
            await message.add_reaction(emote)

        def check(reaction: discord.Reaction, user: discord.User):
            return (
                user == self.author
                and str(reaction.emoji) in emotes
                and reaction.message.id == message.id
            )

        try:
            r, m = await self.bot.wait_for(
                "reaction_add", timeout=timeout, check=check
            )
        except asyncio.TimeoutError:
            try:
                await message.delete()
            except discord.HTTPException:
                return None
        else:
            self.bot.dispatch(name, message, r, m, possibilities, **kwargs)

    @property
    def session(self) -> aiohttp.ClientSession:
        return self.bot.session

    def __repr__(self):
        items = (
            "message=%s" % self.message,
            "channel=%s" % self.channel,
            "guild=%s" % self.guild,
            "author=%s" % self.author,
            "prefix=%s" % self.prefix,
            "args=%s" % self.args,
            "kwargs=%s" % self.kwargs,
        )

        return "<%s %s>" % (self.__class__.__name__, ", ".join(items))


class CommandPLus(commands.Command):
    def __init__(self, function, **kwargs):
        super().__init__(function, **kwargs)
        self.deletable = kwargs.pop("deletable", True)


def command_extra(*args, **kwargs):
    return commands.command(*args, **kwargs, cls=CommandPLus)


class GroupPlus(commands.Group):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.deletable = kwargs.pop("deletable", True)


def group_extra(*args, **kwargs):
    return commands.group(*args, **kwargs, cls=GroupPlus)
