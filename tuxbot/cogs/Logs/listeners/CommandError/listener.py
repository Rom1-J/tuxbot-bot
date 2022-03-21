"""
tuxbot.cogs.Logs.listeners.CommandError.listener
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Listener whenever a command raises an unknown error
"""
import datetime
import os
import textwrap
import traceback

import discord
import sentry_sdk
from discord.ext import commands

from tuxbot.core.Tuxbot import Tuxbot


class CommandError(commands.Cog):
    """Listener whenever a command fails"""

    def __init__(self, bot: Tuxbot):
        self.bot = bot

        self.error_webhook: str = self.bot.config["error_webhook"]

    # =========================================================================
    # =========================================================================

    @commands.Cog.listener(name="on_command_error")
    async def _on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if not isinstance(
            error, (commands.CommandInvokeError, commands.ConversionError)
        ):
            return

        error = error.original
        if isinstance(error, (discord.Forbidden, discord.NotFound)):
            return

        command = ctx.command.name

        if parent_name := ctx.command.full_parent_name:
            command = f"{parent_name} {ctx.command.name}"

        self.bot.statsd.increment(
            "command_error", value=1, tags=[f"command:{command}"]
        )

        self.bot.logger.error(
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
                type(error), error, error.__traceback__, chain=False
            )
        )
        e.description = f"```py\n{textwrap.shorten(exc, width=2035)}\n```"
        e.timestamp = datetime.datetime.utcnow()

        await self.bot.post_webhook(webhook=self.error_webhook, payload=e)

        e.description = (
            "```An error occurred, the bot owner has been advertised...```"
        )

        e.remove_field(0)
        e.remove_field(1)
        e.remove_field(1)

        if os.getenv("PYTHON_ENV", "production") != "development":
            sentry_sdk.capture_exception(error)
            e.set_footer(text=sentry_sdk.last_event_id())

        await ctx.send(embed=e)
