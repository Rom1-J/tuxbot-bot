import re

from discord.ext import commands
from discord.ext.commands import Context


def _(x):
    return x


URL_REG = re.compile(r"https?://(?:www\.)?.+")


class QueryConverter(commands.Converter):
    async def convert(self, ctx: Context, argument: str):  # skipcq: PYL-W0613
        query = argument.strip("<>")

        if not URL_REG.match(query):
            query = f"ytsearch:{query}"

        return query
