import ast
import json
import os

import discord
from discord.ext import commands
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

        return await super().send(content, *args, **kwargs)


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
