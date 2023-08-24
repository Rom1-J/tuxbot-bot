"""
tuxbot.cogs.Logs.listeners.CommandError.listener
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Listener whenever a command raises an unknown error
"""
import datetime as dt
import os
import textwrap
import traceback
import typing

import discord
import sentry_sdk
from discord.ext import commands

from tuxbot.abc.tuxbot_abc import TuxbotABC
from tuxbot.core.config import config
from tuxbot.core.tuxbot import Tuxbot


class CommandError(commands.Cog):
    """Listener whenever a command fails"""

    def __init__(self: typing.Self, bot: Tuxbot) -> None:
        self.bot = bot

        self.error_webhook: str = config.WEBHOOKS["error"]

    # =========================================================================
    # =========================================================================

    @commands.Cog.listener(name="on_command_error")
    async def _on_command_error(
        self: typing.Self,
        ctx: commands.Context[TuxbotABC],
        error: commands.CommandError,
    ) -> None:
        if not isinstance(
            error,
            (
                commands.CommandInvokeError,
                commands.ConversionError,
            ),
        ):
            return

        original_error = error.original
        if isinstance(original_error, (discord.Forbidden, discord.NotFound)):
            return

        if not ctx.command:
            return

        command = ctx.command.name

        if parent_name := ctx.command.full_parent_name:
            command = f"{parent_name} {ctx.command.name}"

        self.bot.statsd.incr(f"command_error.{command}", 1)

        self.bot.logger.exception(
            "[CommandError] '%s' raises unknown error.", ctx.command.name
        )

        e = discord.Embed(title="Command Error", colour=0xCC3366)
        e.add_field(name="Name", value=ctx.command.qualified_name)
        e.add_field(name="Author", value=f"{ctx.author} (ID: {ctx.author.id})")

        fmt = f"Channel: {ctx.channel} (ID: {ctx.channel.id})"
        if ctx.guild:
            fmt = f"{fmt}\nGuild: {ctx.guild} (ID: {ctx.guild.id})"

        e.add_field(name="Location", value=fmt, inline=False)
        e.add_field(
            name="Content",
            value=textwrap.shorten(ctx.message.content, width=512),
        )
        e.add_field(
            name="Cluster ID",
            value=os.getenv("CLUSTER_ID"),
        )

        exc = "".join(
            traceback.format_exception(
                type(original_error),
                original_error,
                original_error.__traceback__,
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
            sentry_sdk.capture_exception(original_error)
            e.set_footer(text=sentry_sdk.last_event_id())
        else:
            from rich.console import Console

            # flake8: noqa
            # noinspection PyBroadException
            try:  # Re-inject error to sys
                raise original_error
            except:
                Console().print_exception(width=None, show_locals=True)

        await ctx.send(embed=e)
