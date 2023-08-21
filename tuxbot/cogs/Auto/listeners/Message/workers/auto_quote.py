"""
tuxbot.cogs.Auto.listeners.Message.workers.AutoQuote
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.

"""
import re
import typing

import discord
from discord.ext import commands

from tuxbot.cogs.Auto.commands.AutoQuote.models.auto_quote import (
    AutoQuoteModel,
)
from tuxbot.core.tuxbot import Tuxbot


REGEX = r"(https://((ptb|canary)\.)?discord\.com/channels/\d+/\d+/\d+)"


class AutoQuote:
    """Automatically send message link content."""

    def __init__(self: typing.Self, bot: Tuxbot) -> None:
        self.bot = bot

    async def process(  # noqa: C901
        self: typing.Self, message: discord.Message
    ) -> None:
        """Process worker."""
        if not message.guild or message.author.bot:
            return

        if not self.bot.cached_config[message.guild.id].get("AutoQuote") and (
            model := await AutoQuoteModel.get_or_create(
                guild_id=message.guild.id
            )
        ):
            self.bot.cached_config[message.guild.id]["AutoQuote"] = {
                "activated": model[0].activated
            }

        if self.bot.cached_config[message.guild.id]["AutoQuote"][
            "activated"
        ] and not (ctx := await self.bot.get_context(message)):
            return

        if ctx.command is not None:
            return

        if not isinstance(ctx.author, discord.Member):
            return

        quotes = [q[0] for q in re.findall(REGEX, message.content)]
        embeds = []

        for message_link in quotes[:3]:
            try:
                referred_message = await commands.MessageConverter().convert(
                    ctx, message_link
                )

                if not referred_message or not referred_message.content:
                    return

                if referred_message.channel.permissions_for(
                    ctx.author
                ).read_message_history:
                    embed = discord.Embed(
                        description=referred_message.content,
                        colour=self.bot.utils.colors.EMBED_BORDER,
                    )
                    embed.timestamp = referred_message.created_at

                    embed.set_footer(
                        text=referred_message.author.display_name,
                        icon_url=referred_message.author.display_avatar,
                    )

                    embeds.append(embed)
            except (
                commands.MessageNotFound,
                commands.ChannelNotFound,
                commands.ChannelNotReadable,
                commands.GuildNotFound,
            ):
                pass

        if embeds:
            await ctx.send(embeds=embeds)
