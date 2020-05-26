import ast
import asyncio
import json
import os

import discord
from discord.ext import commands, flags

from configs.bot.protected import protected
from configs.bot.settings import prefix


class ContextPlus(commands.Context):
    async def send(self, content=None, *args, **kwargs):
        if content is not None:
            for value in protected:
                content = content.replace(
                    str(value),
                    '[Deleted]'
                )

        if kwargs.get('content') is not None:
            for value in protected:
                kwargs['content'] = kwargs['content'].replace(
                    str(value),
                    '[Deleted]'
                )

        if kwargs.get('embeds') is not None and len(kwargs.get('embeds')) > 0:
            for i, embed in enumerate(kwargs.get('embeds')):
                embed = str(kwargs.get('embed').to_dict())
                for value in protected:
                    embed = embed.replace(str(value), '[Deleted]')
                kwargs['embeds'][i] = discord.Embed.from_dict(
                    ast.literal_eval(embed)
                )

        if kwargs.get('embed') is not None:
            embed = str(kwargs.get('embed').to_dict())
            for value in protected:
                embed = embed.replace(str(value), '[Deleted]')
            kwargs['embed'] = discord.Embed.from_dict(
                ast.literal_eval(embed)
            )

        if self.command.deletable:
            message = await super().send(content, *args, **kwargs)
            await message.add_reaction('🗑')

            def check(reaction: discord.Reaction, user: discord.User):
                return user == self.author \
                       and str(reaction.emoji) == '🗑' \
                       and reaction.message.id == message.id

            try:
                await self.bot.wait_for(
                    'reaction_add',
                    timeout=120.0,
                    check=check
                )
            except asyncio.TimeoutError:
                await message.remove_reaction('🗑', self.bot.user)
            else:
                await message.delete()
        else:
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


async def get_prefix(bot, message):
    custom_prefix = [prefix]
    if message.guild:
        path = f"configs/guilds/{str(message.guild.id)}.json"

        if os.path.exists(path):
            with open(path) as f:
                datas = json.load(f)

                custom_prefix = datas["Prefix"]

        return commands.when_mentioned_or(*custom_prefix)(bot, message)


def get_owners() -> list:
    with open("configs/bot/whitelist.json") as f:
        datas = json.load(f)

        return datas['owners']


def get_blacklist() -> dict:
    with open("configs/bot/blacklist.json") as f:
        return json.load(f)
