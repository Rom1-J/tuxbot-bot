import asyncio
import random
from io import BytesIO

import aiohttp
import discord
from discord import Embed
from discord.ext import commands

TOKEN_REPLACEMENT = "■" * random.randint(3, 15)
PASSWORD_REPLACEMENT = "■" * random.randint(3, 15)
IP_REPLACEMENT = "■" * random.randint(3, 15)


class ContextPlus(commands.Context):
    async def send(
        self,
        content=None,
        *,
        tts=False,
        embed=None,
        file=None,
        files=None,
        delete_after=None,
        nonce=None,
        allowed_mentions=None,
        deletable=True,
    ):  # i know *args and **kwargs but, i prefer work with same values
        from tuxbot.core.utils.functions.utils import (
            replace_in_dict,
            replace_in_list,
        )

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
                file = discord.File(BytesIO(content.encode()), "output.txt")
                content = "output too long..."
        if embed:
            e = embed.to_dict()
            for key, value in e.items():
                if isinstance(value, (str, bytes)):
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
                    e[key] = replace_in_list(
                        value, self.bot.config.Core.token, TOKEN_REPLACEMENT
                    )
                    e[key] = replace_in_list(
                        e[key],
                        self.bot.config.Core.Database.password,
                        PASSWORD_REPLACEMENT,
                    )
                    e[key] = replace_in_list(
                        e[key], self.bot.config.Core.ip, IP_REPLACEMENT
                    )
                    e[key] = replace_in_list(
                        e[key], self.bot.config.Core.ip6, IP_REPLACEMENT
                    )
                elif isinstance(value, dict):
                    e[key] = replace_in_dict(
                        value, self.bot.config.Core.token, TOKEN_REPLACEMENT
                    )
                    e[key] = replace_in_dict(
                        e[key],
                        self.bot.config.Core.Database.password,
                        PASSWORD_REPLACEMENT,
                    )
                    e[key] = replace_in_dict(
                        e[key], self.bot.config.Core.ip, IP_REPLACEMENT
                    )
                    e[key] = replace_in_dict(
                        e[key], self.bot.config.Core.ip6, IP_REPLACEMENT
                    )
            embed = Embed.from_dict(e)

        if (
            hasattr(self.command, "deletable") and self.command.deletable
        ) and deletable:
            message = await super().send(
                content=content,
                tts=tts,
                embed=embed,
                file=file,
                files=files,
                delete_after=delete_after,
                nonce=nonce,
                allowed_mentions=allowed_mentions,
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
                await message.remove_reaction("🗑", self.bot.user)
            else:
                await message.delete()
            return message

        return await super().send(
            content=content,
            tts=tts,
            embed=embed,
            file=file,
            files=files,
            delete_after=delete_after,
            nonce=nonce,
            allowed_mentions=allowed_mentions,
        )

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
