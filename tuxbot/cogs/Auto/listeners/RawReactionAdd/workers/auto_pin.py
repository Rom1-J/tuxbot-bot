"""
tuxbot.cogs.Auto.listeners.RawReactionAdd.workers.AutoPin
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.

"""
import typing

import discord

from tuxbot.cogs.Auto.commands.AutoPin.models.auto_pin import AutoPinModel
from tuxbot.core.tuxbot import Tuxbot


class AutoPin:
    """Automatically send process reaction add for pin."""

    def __init__(self: typing.Self, bot: Tuxbot) -> None:
        self.bot = bot

    async def process(
        self: typing.Self, payload: discord.RawReactionActionEvent
    ) -> None:
        """Process worker."""
        if (
            not payload.guild_id
            or payload.user_id == self.bot.client_options.get("id")
        ) or payload.emoji != discord.PartialEmoji(name="📌"):
            return

        if not self.bot.cached_config[payload.guild_id].get("AutoPin") and (
            model := await AutoPinModel.get_or_create(
                guild_id=payload.guild_id
            )
        ):
            self.bot.cached_config[payload.guild_id]["AutoPin"] = {
                "activated": model[0].activated,
                "threshold": model[0].threshold,
            }

        threshold = self.bot.cached_config[payload.guild_id]["AutoPin"].get(
            "threshold"
        )

        if self.bot.cached_config[payload.guild_id]["AutoPin"][
            "activated"
        ] and (
            (
                channel := await self.bot.fetch_channel_or_none(
                    payload.channel_id
                )
            )
            and isinstance(channel, discord.abc.Messageable)
            and (
                message := await self.bot.fetch_message_or_none(
                    channel, payload.message_id
                )
            )
            and (pins := discord.utils.get(message.reactions, emoji="📌"))
            and pins.count >= threshold
        ):
            await message.pin(reason="Auto pinned via reactions")
