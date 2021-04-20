import asyncio
import datetime
import json
import logging
import textwrap
import traceback
from collections import defaultdict
from logging import LogRecord

import discord
import humanize
import psutil
import sentry_sdk
from discord.ext import commands, tasks
from structured_config import ConfigFile

from tuxbot.core.bot import Tux
from tuxbot.core.i18n import (
    Translator,
)
from tuxbot.core.utils.functions.extra import (
    command_extra,
    ContextPlus,
)
from tuxbot.core.utils.data_manager import cogs_data_path
from .config import LogsConfig
from .functions.utils import sort_by
from ...core.utils.functions.utils import shorten

log = logging.getLogger("tuxbot.cogs.Logs")
_ = Translator("Logs", __file__)


class GatewayHandler(logging.Handler):
    def __init__(self, cog):
        self.cog = cog
        super().__init__(logging.INFO)

    def filter(self, record: LogRecord):
        return (
            record.name == "discord.gateway"
            or "Shard ID" in record.msg
            or "Websocket closed " in record.msg
        )

    def emit(self, record: LogRecord):
        self.cog.add_record(record)


class Logs(commands.Cog, name="Logs"):
    def __init__(self, bot: Tux):
        self.bot = bot
        self.process = psutil.Process()
        self._batch_lock = asyncio.Lock()
        self._data_batch = []
        self._gateway_queue = asyncio.Queue()
        self.gateway_worker.start()  # pylint: disable=no-member

        self.__config: LogsConfig = ConfigFile(
            str(cogs_data_path("Logs") / "config.yaml"),
            LogsConfig,
        ).config

        self._resumes = []
        self._identifies = defaultdict(list)

        self.old_on_error = bot.on_error
        bot.on_error = self.on_error

        if self.bot.instance_name != "dev":
            sentry_sdk.init(
                dsn=self.__config.sentryKey,
                traces_sample_rate=1.0,
                environment=self.bot.instance_name,
                debug=False,
                attach_stacktrace=True,
            )

    def cog_unload(self):
        self.bot.on_error = self.old_on_error

    async def on_error(self, event, *args, **kwargs):
        raise  # pylint: disable=misplaced-bare-raise

    # =========================================================================
    # =========================================================================

    def webhook(self, log_type):
        webhook = discord.Webhook.from_url(
            getattr(self.__config, log_type),
            session=self.bot.session,
        )
        return webhook

    async def send_guild_stats(self, e, guild):
        e.add_field(name="Name", value=guild.name)
        e.add_field(name="ID", value=guild.id)
        e.add_field(name="Shard ID", value=guild.shard_id or "N/A")
        e.add_field(
            name="Owner", value=f"{guild.owner} (ID: {guild.owner.id})"
        )

        bots = sum(member.bot for member in guild.members)
        total = guild.member_count
        online = sum(
            member.status is discord.Status.online for member in guild.members
        )

        e.add_field(name="Members", value=str(total))
        e.add_field(name="Bots", value=f"{bots} ({bots / total:.2%})")
        e.add_field(name="Online", value=f"{online} ({online / total:.2%})")

        if guild.icon:
            e.set_thumbnail(url=guild.icon_url)

        if guild.me:
            e.timestamp = guild.me.joined_at

        await self.webhook("guilds").send(embed=e)

    def add_record(self, record: LogRecord):
        self._gateway_queue.put_nowait(record)

    async def notify_gateway_status(self, record: LogRecord):
        types = {"INFO": ":information_source:", "WARNING": ":warning:"}

        emoji = types.get(record.levelname, ":heavy_multiplication_x:")
        dt = datetime.datetime.utcfromtimestamp(record.created)
        msg = (
            f"{emoji} `[{dt:%Y-%m-%d %H:%M:%S}] "
            f"{await shorten(self.bot.session, record.msg, 1500)}`"
        )
        await self.webhook("gateway").send(msg)

    def clear_gateway_data(self):
        one_week_ago = datetime.datetime.utcnow() - datetime.timedelta(days=7)
        to_remove = [
            index
            for index, dt in enumerate(self._resumes)
            if dt < one_week_ago
        ]
        for index in reversed(to_remove):
            del self._resumes[index]

        for _, dates in self._identifies.items():
            to_remove = [
                index for index, dt in enumerate(dates) if dt < one_week_ago
            ]
            for index in reversed(to_remove):
                del dates[index]

    async def register_command(self, ctx: ContextPlus):
        if ctx.command is None:
            return

        command = ctx.command.qualified_name
        self.bot.stats["commands"][command] += 1
        message = ctx.message
        if ctx.guild is None:
            destination = "Private Message"
            guild_id = None
        else:
            destination = f"#{message.channel} ({message.guild})"
            guild_id = ctx.guild.id

        log.info(
            "%s: %s in %s > %s",
            message.created_at,
            message.author,
            destination,
            message.content,
        )
        async with self._batch_lock:
            self._data_batch.append(
                {
                    "guild": guild_id,
                    "channel": ctx.channel.id,
                    "author": ctx.author.id,
                    "used": message.created_at.isoformat(),
                    "prefix": ctx.prefix,
                    "command": command,
                    "failed": ctx.command_failed,
                }
            )

    # =========================================================================
    # =========================================================================

    @tasks.loop(seconds=0.0)
    async def gateway_worker(self):
        record = await self._gateway_queue.get()
        await self.notify_gateway_status(record)

    @commands.Cog.listener()
    async def on_command_completion(self, ctx: ContextPlus):
        await self.register_command(ctx)

    @commands.Cog.listener()
    async def on_socket_response(self, msg):
        self.bot.stats["socket"][msg.get("t")] += 1

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.guild):
        e = discord.Embed(colour=0x53DDA4, title="New Guild")  # green colour
        await self.send_guild_stats(e, guild)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.guild):
        e = discord.Embed(colour=0xDD5F53, title="Left Guild")  # red colour
        await self.send_guild_stats(e, guild)

    @commands.Cog.listener()
    async def on_message(self, message: discord.message):
        if message.guild is None:
            e = discord.Embed(colour=0x0A97F5, title="New DM")  # blue colour
            e.set_author(
                name=message.author,
                icon_url=message.author.avatar_url_as(format="png"),
            )
            e.description = message.content
            if len(message.attachments) > 0:
                e.set_image(url=message.attachments[0].url)
            e.set_footer(text=f"User ID: {message.author.id}")
            await self.webhook("dm").send(embed=e)

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: ContextPlus, error: commands.CommandError
    ):
        await self.register_command(ctx)
        if not isinstance(
            error, (commands.CommandInvokeError, commands.ConversionError)
        ):
            return

        error = error.original
        if isinstance(error, (discord.Forbidden, discord.NotFound)):
            return

        if self.bot.instance_name != "dev":
            sentry_sdk.capture_exception(error)
        self.bot.console.log(
            "Command Error, check sentry or discord error channel"
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
            name="Bot Instance",
            value=self.bot.instance_name,
        )

        exc = "".join(
            traceback.format_exception(
                type(error), error, error.__traceback__, chain=False
            )
        )
        e.description = f"```py\n{exc}\n```"
        e.timestamp = datetime.datetime.utcnow()
        await self.webhook("errors").send(embed=e)

        e.description = _(
            "```An error occurred, the bot owner has been advertised...```",
            ctx,
            self.bot.config,
        )
        e.remove_field(0)
        e.remove_field(1)
        e.remove_field(1)

        if self.bot.instance_name != "dev":
            e.set_footer(text=sentry_sdk.last_event_id())

        await ctx.send(embed=e)

    @commands.Cog.listener()
    async def on_socket_raw_send(self, data):
        if '"op":2' not in data and '"op":6' not in data:
            return

        back_to_json = json.loads(data)
        if back_to_json["op"] == 2:
            payload = back_to_json["d"]
            inner_shard = payload.get("shard", [0])
            self._identifies[inner_shard[0]].append(datetime.datetime.utcnow())
        else:
            self._resumes.append(datetime.datetime.utcnow())

        self.clear_gateway_data()

    # =========================================================================
    # =========================================================================

    @command_extra(name="commandstats", hidden=True, deletable=True)
    @commands.is_owner()
    async def _commandstats(self, ctx: ContextPlus, limit=20):
        counter = self.bot.stats["commands"]
        width = len(max(counter, key=len)) + 1

        if limit > 0:
            common = counter.most_common(limit)
        else:
            common = counter.most_common()[limit:]

        output = "\n".join(f"{k:<{width}}: {c}" for k, c in common)

        await ctx.send(f"```\n{output}\n```")

    @command_extra(name="socketstats", hidden=True, deletable=True)
    async def _socketstats(self, ctx: ContextPlus):
        delta = datetime.datetime.now() - self.bot.uptime
        minutes = delta.total_seconds() / 60

        counter = self.bot.stats["socket"]
        if None in counter:
            counter.pop(None)

        total = sum(self.bot.stats["socket"].values())
        cpm = total / minutes

        e = discord.Embed(
            title=_("Sockets stats", ctx, self.bot.config),
            description=_(
                "{} socket events observed ({:.2f}/minute):",
                ctx,
                self.bot.config,
            ).format(total, cpm),
            color=discord.colour.Color.green(),
        )

        for major, events in sort_by(counter.most_common()).items():
            if events:
                output = "\n".join(f"{k}: {v}" for k, v in events.items())
                e.add_field(
                    name=major.capitalize(),
                    value=f"```\n{output}\n```",
                    inline=False,
                )

        await ctx.send(embed=e)

    @command_extra(name="uptime")
    async def _uptime(self, ctx: ContextPlus):
        uptime = humanize.naturaltime(
            datetime.datetime.now() - self.bot.uptime
        )
        await ctx.send(f"Uptime: **{uptime}**")
