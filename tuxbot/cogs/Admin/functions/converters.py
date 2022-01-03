from discord.ext import commands
from discord.ext.commands import Context


class ChannelConverter(commands.Converter):
    async def convert(self, ctx: Context, argument: str):  # skipcq: PYL-W0613
        return await ctx.bot.fetch_channel(int(argument))
