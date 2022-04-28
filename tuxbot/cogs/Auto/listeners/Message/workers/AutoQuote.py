"""
tuxbot.cogs.Logs.listeners.Message.workers.auto_quote
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import re

import discord
from discord.ext import commands

from tuxbot.core.Tuxbot import Tuxbot

from ....commands.AutoQuote.models.AutoQuote import AutoQuoteModel


REGEX = (
    r"(https://((ptb|canary)\.)?discord\.com"
    r"/channels/\d{18}/\d{18}/\d{18})"
)


class AutoQuote:
    """Automatically send message link content"""

    def __init__(self, bot: Tuxbot):
        self.bot = bot

    async def process(self, message: discord.Message):
        """Process worker"""

        if message.guild is None or message.author.bot:
            return

        if await AutoQuoteModel.get_or_none(
                guild_id=message.guild.id, activated=True
        ):
            if not (ctx := await self.bot.get_context(message)):
                return

            if ctx.command is not None:
                return

            quotes = [q[0] for q in re.findall(REGEX, message.content)]
            embeds = []

            for message_link in quotes[:5]:
                if not (
                        referred_message := await commands.MessageConverter()
                        .convert(ctx, message_link)
                ) or not referred_message.content:
                    return

                if referred_message.channel.permissions_for(
                    ctx.author
                ).read_message_history:
                    embed = discord.Embed(
                        description=referred_message.content,
                        colour=self.bot.utils.colors.EMBED_BORDER.value
                    )
                    embed.timestamp = referred_message.created_at

                    embed.set_footer(
                        text=referred_message.author.display_name,
                        icon_url=referred_message.author.display_avatar
                    )

                    embeds.append(embed)

            if embeds:
                await ctx.send(embeds=embeds)
