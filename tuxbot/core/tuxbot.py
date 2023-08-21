"""
Tuxbot core module: Tuxbot.

Client class instance for Tuxbot
"""
import json
import sys
import traceback
import typing
from datetime import datetime
from pathlib import Path

import aiohttp
import discord
from discord.ext import commands
from discord.http import Route

from tuxbot.abc.module_abc import ModuleABC
from tuxbot.abc.tuxbot_abc import TuxbotABC
from tuxbot.core import redis
from tuxbot.core.collections.module_collection import ModuleCollection
from tuxbot.core.config import config
from tuxbot.core.models.guild import GuildModel
from tuxbot.core.models.tuxbot import TuxbotModel
from tuxbot.core.utils.context_plus import ContextPlus


VocalGuildChannel = discord.VoiceChannel | discord.StageChannel
GuildChannel = (
    VocalGuildChannel
    | discord.ForumChannel
    | discord.TextChannel
    | discord.CategoryChannel
)

DiscordChannel = GuildChannel | discord.abc.PrivateChannel | discord.Thread


class Tuxbot(TuxbotABC):
    """Tuxbot client class."""

    def __init__(self: typing.Self) -> None:
        self.client_options = self.configure()
        super().__init__(**self.client_options)

        self._internal_request = self.http.request
        self.http.request = self._request

        self.collection = ModuleCollection(self)
        self.running_instance = True

    # =========================================================================
    # =========================================================================

    async def setup_hook(self: typing.Self) -> None:
        """Load configurations."""
        await self.collection.load_modules()

        await self.db.init()

        if not await TuxbotModel.get_or_none(id=config.CLIENT["id"]):
            await TuxbotModel.create(
                id=config.CLIENT["id"],
                ignored_users=[],
                ignored_channels=[],
                ignored_guilds=[],
            )

    # =========================================================================

    async def on_ready(self: typing.Self) -> None:
        """Ready event handler."""
        if not self.user:
            return

        if self.uptime is not None and self.uptime.timestamp() > 0:
            self.last_on_ready = datetime.now()
            return

        self.uptime = datetime.now()
        self.last_on_ready = self.uptime

        if game := config.CLIENT["game"]:
            await self.change_presence(
                status=discord.Status.online, activity=discord.Game(game)
            )

        async for guild in self.fetch_guilds():
            self.cached_config[guild.id] = {}
            guild_model: GuildModel | None = await self.models[
                "Guild"
            ].get_or_none(id=guild.id)

            if guild_model:
                guild_model.deleted = False
                await guild_model.save()
                continue

            await GuildModel.create(
                id=guild.id,
                moderators=[],
                moderator_roles=[],
                deleted=False,
            )

        self.logger.info(
            "[Tuxbot] %s "
            "ready with %d guilds, "
            "%d users, "
            "%d commands and "
            "%d app_commands.",
            self.user.name,
            len(self.guilds),
            len(self.users),
            len(tuple(self.walk_commands())),
            len(tuple(self.tree.walk_commands())),
        )

    # =========================================================================
    async def get_context(
        self: typing.Self,
        message: discord.Message,
        *,
        cls: type[ContextPlus] | None = None,
    ) -> ContextPlus:
        """Bind custom context."""
        return await super().get_context(message, cls=cls or ContextPlus)

    # =========================================================================

    async def invoke(self: typing.Self, ctx: ContextPlus) -> None:
        """Bind custom command invoker."""
        if ctx.command is not None and await ctx.command.can_run(ctx):
            async with ctx.typing():
                await super().invoke(ctx)

    # =========================================================================

    def dispatch(
        self: typing.Self,
        event_name: str,
        /,
        *args: typing.Any,
        **kwargs: typing.Any,
    ) -> None:
        """Bind custom command invoker."""
        if self.running_instance:
            super().dispatch(event_name, *args, **kwargs)

    # =========================================================================
    # =========================================================================

    @staticmethod
    async def fetch_message_or_none(
        channel: discord.abc.Messageable, message_id: int
    ) -> discord.Message | None:
        """Fetch message and return None instead of raising NotFound."""
        try:
            return await channel.fetch_message(message_id)
        except discord.NotFound:
            return None

    # =========================================================================

    @staticmethod
    async def fetch_member_or_none(
        guild: discord.Guild, user_id: int
    ) -> discord.Member | None:
        """Fetch member and return None instead of raising NotFound."""
        try:
            return await guild.fetch_member(user_id)
        except discord.NotFound:
            return None

    # =========================================================================

    async def fetch_user_or_none(
        self: typing.Self, user_id: int
    ) -> discord.User | None:
        """Fetch user and return None instead of raising NotFound."""
        try:
            return await self.fetch_user(user_id)
        except discord.NotFound:
            return None

    # =========================================================================

    async def fetch_channel_or_none(
        self: typing.Self, channel_id: int
    ) -> DiscordChannel | None:
        """Fetch channel and return None instead of raising NotFound."""
        try:
            return await self.fetch_channel(channel_id)
        except discord.NotFound:
            return None

    # =========================================================================

    async def launch(self: typing.Self) -> None:
        """Login to discord."""
        try:
            self.redis = redis.connect()
            await self.redis.ping()
            self.logger.info("[Tuxbot] Redis connection established.")
        except Exception as e:
            self.logger.exception(e)  # noqa: TRY401

        await super().start(config.CLIENT["token"])

    # =========================================================================

    async def shutdown(self: typing.Self) -> None:
        """Disconnect from Discord and closes all actives connections."""
        await self.db.disconnect()
        await super().close()

    # =========================================================================

    async def _request(
        self: typing.Self,
        route: Route,
        *,
        files: typing.Sequence[discord.File] | None = None,
        form: typing.Iterable[dict[str, typing.Any]] | None = None,
        **kwargs: typing.Any,
    ) -> typing.Any:
        """Proxy function for internal request manager of dpy."""
        self.statsd.increment(
            "request_event_type",
            value=1,
            tags=[
                f"request_method:{route.method}",
                f"request_endpoint:{route.path}",
            ],
        )

        return await self._internal_request(
            route, files=files, form=form, **kwargs
        )

    # =========================================================================
    # =========================================================================

    @staticmethod
    async def post_webhook(
        webhook: str, payload: dict[str, typing.Any] | discord.Embed
    ) -> None:
        """
        Post webhook.

        Parameters
        ----------
        webhook:str
            Webhook URL
        payload:dict[str, typing.Any] | discord.Embed
            Webhook data
        """
        async with aiohttp.ClientSession() as session:
            if isinstance(payload, discord.Embed):
                w: discord.Webhook = discord.Webhook.from_url(
                    webhook, session=session
                )
                await w.send(embed=payload)
            else:
                await session.post(webhook, json=payload)

    # =========================================================================

    @staticmethod
    def configure() -> dict[str, typing.Any]:
        """Configure Tuxbot."""

        async def get_prefix(
            bot: "Tuxbot", message: discord.Message
        ) -> list[str]:
            """Get bot prefixes from config or set it as mentionable."""
            prefixes: list[str] | None = config.CLIENT["prefixes"]

            if not prefixes or not isinstance(prefixes, list):
                prefixes = commands.when_mentioned(bot, message)

            return prefixes

        client_config: dict[str, typing.Any] = {
            "disable_events": {"TYPING_START": True},
            "allowed_mentions": discord.AllowedMentions(
                everyone=(not config.CLIENT["disable_everyone"]) or False
            ),
            "max_messages": (
                int(config.CLIENT["max_cached_messages"]) or 10000
            ),
            "command_prefix": get_prefix,
            "id": config.CLIENT["id"],
            "owner_ids": config.CLIENT["owners_id"],
            "first_shard_id": (config.FIRST_SHARD_ID or config.SHARD_ID or 0),
            "last_shard_id": (config.LAST_SHARD_ID or config.SHARD_ID or 0),
            "max_shards": config.SHARD_COUNT or 1,
            "intents": config.CLIENT.get("intents", discord.Intents.all()),
            "help_command": None,
        }

        client_config["disable_events"]["PRESENCE_UPDATE"] = True

        if disabled_events := config.CLIENT["disabled_events"]:
            for event in disabled_events:
                client_config["disable_events"][event] = True

        return client_config

    # =========================================================================

    @staticmethod
    def crash_report(client: "Tuxbot", err: Exception) -> None:
        """
        Generate crash report file and exit.

        Parameters
        ----------
        client: :class:`Tuxbot`
            Tuxbot client instance
        err:Exception
            Crash exception

        Returns
        -------
        typing.NoReturn
        """
        cluster_id = f"C{config.CLUSTER_ID}"
        time = datetime.utcnow().isoformat()

        crash_name = f"crashreport_{cluster_id}_{time}.txt"
        crash_path = f"logs/{crash_name}"

        trace = "".join(
            traceback.TracebackException.from_exception(err).format()
        )

        client_options = json.dumps(
            client.client_options,
            indent=4,
            sort_keys=True,
            default=lambda o: f"<<non-serializable: {o!r}>>",
        )

        report = f"Crash Report [{cluster_id}] {time}:\n\n"
        report += trace

        report += "\n\nClient Options:"
        report += f"\n{client_options}"

        report += "\n\nCogs crash reports:"

        for module in client.cogs:
            if isinstance(module, ModuleABC) and hasattr(
                module, "crash_report"
            ):
                report += f"\n{module.crash_report()}\n"

        with Path(crash_path).open("w") as f:
            f.write(report)

        sys.exit(1)
