"""
tuxbot.cogs.Auto.listeners.RawReactionAdd.workers.AutoPin
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import discord

from tuxbot.core.Tuxbot import Tuxbot

from ....commands.AutoPin.models.AutoPin import AutoPinModel


class AutoPin:
    """Automatically send process reaction add for pin"""

    def __init__(self, bot: Tuxbot) -> None:
        self.bot = bot

    async def process(self, payload: discord.RawReactionActionEvent) -> None:
        """Process worker"""

        if (
            not payload.guild_id
            or payload.user_id == self.bot.client_options.get("id")
        ) or payload.emoji != discord.PartialEmoji(name="📌"):
            return

        if not self.bot.cached_config[payload.guild_id].get("AutoPin"):
            if model := await AutoPinModel.get_or_create(
                guild_id=payload.guild_id
            ):
                self.bot.cached_config[payload.guild_id]["AutoPin"] = {
                    "activated": model[0].activated,
                    "threshold": model[0].threshold,
                }

        threshold = self.bot.cached_config[payload.guild_id]["AutoPin"].get(
            "threshold"
        )

        if self.bot.cached_config[payload.guild_id]["AutoPin"]["activated"]:
            if channel := await self.bot.fetch_channel_or_none(
                payload.channel_id
            ):
                if isinstance(channel, discord.abc.Messageable) and (
                    message := await self.bot.fetch_message_or_none(
                        channel, payload.message_id
                    )
                ):
                    if (
                        pins := discord.utils.get(message.reactions, emoji="📌")
                    ) and pins.count >= threshold:
                        await message.pin(reason="Auto pinned via reactions")
