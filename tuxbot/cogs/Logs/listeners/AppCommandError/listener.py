"""
tuxbot.cogs.Logs.listeners.AppCommandError.listener
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Listener whenever an app command raises an unknown error
"""
import datetime as dt
import os
import textwrap
import traceback
import typing

import discord
import sentry_sdk
from discord import app_commands
from discord.ext import commands

from tuxbot.core.config import config
from tuxbot.core.tuxbot import Tuxbot


class AppCommandError(commands.Cog):
    """Listener whenever an app command fails"""

    def __init__(self: typing.Self, bot: Tuxbot) -> None:
        self.bot = bot
        self.bot.tree.on_error = self._on_app_command_error

        self.error_webhook: str = config.WEBHOOKS["error"]

    # =========================================================================
    # =========================================================================

    @commands.Cog.listener(name="cog_app_command_error")
    async def _on_app_command_error(
        self: typing.Self,
        interaction: discord.Interaction,
        error: app_commands.AppCommandError,
    ) -> None:
        if isinstance(error, (discord.Forbidden, discord.NotFound)):
            return

        if not (command := interaction.command):
            return

        self.bot.statsd.incr(
            f"command_error.{command.qualified_name}",
            1,
        )

        self.bot.logger.exception(
            "[CommandError] '%s' raises unknown error.", command.qualified_name
        )

        e = discord.Embed(title="Command Error", colour=0xCC3366)
        e.add_field(name="Name", value=command.qualified_name)
        e.add_field(
            name="Author",
            value=f"{interaction.user} (ID: {interaction.user.id})",
        )

        fmt = ""
        if interaction.channel:
            fmt = (
                f"Channel: {interaction.channel} "
                f"(ID: {interaction.channel.id})"
            )
        if interaction.guild:
            fmt = (
                f"{fmt}\nGuild: {interaction.guild} "
                f"(ID: {interaction.guild.id})"
            )

        e.add_field(name="Location", value=fmt, inline=False)
        e.add_field(
            name="Cluster ID",
            value=os.getenv("CLUSTER_ID"),
        )

        exc = "".join(
            traceback.format_exception(
                type(error),
                error,
                error.__traceback__,
                chain=False,
            )
        )
        e.description = f"```py\n{textwrap.shorten(exc, width=2035)}\n```"
        e.timestamp = dt.datetime.now(dt.UTC)

        full_e = e.copy()

        e.description = (
            "```An error occurred, the bot owner has been advertised...```"
        )

        e.remove_field(0)
        e.remove_field(1)
        e.remove_field(1)

        if os.getenv("PYTHON_ENV", "production") != "development":
            await self.bot.post_webhook(
                webhook=self.error_webhook, payload=full_e
            )
            sentry_sdk.capture_exception(error)
            e.set_footer(text=sentry_sdk.last_event_id())
        else:
            from rich.console import Console

            # flake8: noqa
            # noinspection PyBroadException
            try:  # Re-inject error to sys
                raise error
            except:
                Console().print_exception(width=None, show_locals=True)

        await interaction.response.send_message(embed=e, ephemeral=True)
