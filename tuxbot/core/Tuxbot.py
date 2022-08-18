"""
Tuxbot core module: Tuxbot

Client class instance for Tuxbot
"""
import json
import os
import sys
import traceback
import typing
from datetime import datetime
from distutils.util import strtobool

import aiohttp
import discord
from datadog import initialize
from ddtrace import patch
from discord.ext import commands
from discord.http import Route
from jishaku import Jishaku

from tuxbot.abc.ModuleABC import ModuleABC
from tuxbot.abc.TuxbotABC import TuxbotABC
from tuxbot.core import redis
from tuxbot.core.collections.ModuleCollection import ModuleCollection
from tuxbot.core.config import config
from tuxbot.core.models.Guild import GuildModel
from tuxbot.core.utils.ContextPlus import ContextPlus


if strtobool(os.getenv("DD_ACTIVE", "false")):
    initialize(
        statsd_host=os.getenv("STATSD_HOST", "127.0.0.1"),
        statsd_port=8125,
        statsd_namespace="tuxbot_metric",
    )

    patch(
        aioredis=True,
        asyncio=True,
        requests=True,
        asyncpg=True,
        logging=True,
    )


class Tuxbot(TuxbotABC):
    """
    Tuxbot client class
    """

    def __init__(self, options: dict[str, typing.Any]) -> None:
        self._config = config

        options = options or {}

        self.client_options, self.cluster_options = self.configure(options)
        super().__init__(**self.client_options)

        self._internal_request = self.http.request
        self.http.request = self._request  # type: ignore

        self.collection = ModuleCollection(self._config, self)
        self.running_instance = True

    # =========================================================================
    # =========================================================================

    async def setup_hook(self) -> None:
        """Load configurations"""

        await self.collection.register(Jishaku)
        await self.collection.load_modules()

        await self.db.init()

        db_config = await self.models["Tuxbot"].get_or_none(
            id=self.config["client"].get("id")
        )

        if db_config:
            self.config |= db_config
        else:
            await self.models["Tuxbot"].create(
                id=self.config["client"].get("id"),
                ignored_users=[],
                ignored_channels=[],
                ignored_guilds=[],
            )

    # =========================================================================

    async def on_ready(self) -> None:
        """Ready event handler"""

        if not self.user:
            return

        if self.uptime is not None and self.uptime.timestamp() > 0:
            self.last_on_ready = datetime.now()
            return

        self.uptime = datetime.now()
        self.last_on_ready = self.uptime

        self.logger.info(
            "[Tuxbot] %s "
            "ready with %d guilds, "
            "%d users and "
            "%d commands.",
            self.user.name,
            len(self.guilds),
            len(self.users),
            len(tuple(self.walk_commands())),
        )

        if game := self.config["client"].get("game"):
            await self.change_presence(
                status=discord.Status.online, activity=discord.Game(game)
            )

        # todo: fix this
        #  (IntegrityError: null value in column "moderators" of relation
        #  "guild" violates not-null constraint)
        # for guild in self.guilds:
        #     guild_model: GuildModel | None = await self.models[
        #         "Guild"
        #     ].get_or_none(id=guild.id)
        #
        #     if guild_model:
        #         guild_model.deleted = False
        #         await guild_model.save()
        #         return
        #
        #     await self.models["Guild"].create(
        #         id=guild.id,
        #         moderators=[],
        #         moderator_roles=[],
        #         deleted=False,
        #     )

    # =========================================================================
    async def get_context(  # type: ignore
        self,
        message: discord.Message,
        *,
        cls: type[ContextPlus] = None,  # type: ignore
    ) -> ContextPlus:
        """Bind custom context"""

        return await super().get_context(message, cls=cls or ContextPlus)

    # =========================================================================

    async def invoke(self, ctx: ContextPlus) -> None:  # type: ignore
        """Bind custom command invoker"""
        if ctx.command is not None and await ctx.command.can_run(ctx):
            async with ctx.typing():
                await super().invoke(ctx)

    # =========================================================================

    def dispatch(
        self, event_name: str, /, *args: typing.Any, **kwargs: typing.Any
    ) -> None:
        """Bind custom command invoker"""
        if self.running_instance:
            super().dispatch(event_name, *args, **kwargs)

    # =========================================================================
    # =========================================================================

    @staticmethod
    async def fetch_member_or_none(
        guild: discord.Guild, user_id: int
    ) -> discord.Member | None:
        """fetch member and return None instead of raising NotFound"""
        try:
            return await guild.fetch_member(user_id)
        except discord.NotFound:
            return None

    # =========================================================================

    async def fetch_user_or_none(self, user_id: int) -> discord.User | None:
        """fetch user and return None instead of raising NotFound"""
        try:
            return await self.fetch_user(user_id)
        except discord.NotFound:
            return None

    # =========================================================================

    async def launch(self) -> None:
        """Login to discord"""

        try:
            self.redis = redis.connect()
            await self.redis.ping()
            self.logger.info("[Tuxbot] Redis connection established.")
        except Exception as e:
            self.logger.error(e)

        await super().start(config["client"]["token"])

    # =========================================================================

    async def shutdown(self) -> None:
        """Disconnect from Discord and closes all actives connections."""
        await self.db.disconnect()
        await super().close()

    # =========================================================================

    async def _request(
        self,
        route: Route,
        *,
        files: typing.Sequence[discord.File] | None = None,
        form: typing.Iterable[dict[str, typing.Any]] | None = None,
        **kwargs: typing.Any,
    ) -> typing.Any:
        """Proxy function for internal request manager of dpy"""

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

    def change_running_state(self, new_state: bool) -> None:
        """Change running_instance state"""

        self.running_instance = new_state
        self.logger.info("[Tuxbot] 'running_instance' set to %s", new_state)

    # =========================================================================
    # =========================================================================

    @staticmethod
    async def post_webhook(
        webhook: str, payload: dict[str, typing.Any] | discord.Embed
    ) -> None:
        """Post webhook

        Parameters
        ----------
        webhook:str
            Webhook URL
        payload:dict[str, typing.Any] | discord.Embed
            Webhook data
        """
        async with aiohttp.ClientSession() as session:
            if isinstance(payload, discord.Embed):
                webhook = discord.Webhook.from_url(webhook, session=session)
                await webhook.send(embed=payload)
            else:
                await session.post(webhook, json=payload)

    # =========================================================================

    @staticmethod
    def configure(
        options: dict[str, typing.Any]
    ) -> tuple[dict[str, typing.Any], dict[str, typing.Any]]:
        """Configure Tuxbot"""

        async def get_prefix(
            bot: "Tuxbot", message: discord.Message
        ) -> list[str]:
            """Get bot prefixes from config or set it as mentionable"""
            prefixes: list[str] | None = config.get("prefixes")

            if not prefixes or not isinstance(prefixes, list):
                prefixes = commands.when_mentioned(bot, message)

            return prefixes

        client_config: dict[str, typing.Any] = {
            "disable_events": {"TYPING_START": True},
            "allowed_mentions": discord.AllowedMentions(
                everyone=(not config["client"]["disable_everyone"]) or False
            ),
            "max_messages": (
                int(config["client"]["max_cached_messages"]) or 10000
            ),
            "command_prefix": get_prefix,
            "owner_ids": config["client"]["owners_id"],
            "first_shard_id": (
                options.get("first_shard_id")
                or options.get("custer_id")
                or options.get("shard_id")
                or 0
            ),
            "last_shard_id": (
                options.get("last_shard_id")
                or options.get("custer_id")
                or options.get("shard_id")
                or 0
            ),
            "max_shards": options.get("shard_count") or 1,
            "intents": config["client"].get("intents", discord.Intents.all()),
            "help_command": None,
        }

        cluster_config: dict[str, typing.Any] = {
            "cluster_id": options.get("cluster_id"),
            "cluster_count": options.get("cluster_count"),
        }

        if not config["test"]:
            client_config["disable_events"]["PRESENCE_UPDATE"] = True

        if config.get("disable_events"):
            for event in config["disable_events"]:
                client_config["disable_events"][event] = True

        config["client_options"] = client_config
        config["cluster_config"] = cluster_config

        return client_config, cluster_config

    # =========================================================================

    @staticmethod
    def crash_report(client: "Tuxbot", err: Exception) -> None:
        """Generate crash report file and exit

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
        cluster_id = f"C{client.cluster_options.get('cluster_id')}"
        time = datetime.utcnow().isoformat()

        crash_name = f"crashreport_{cluster_id}_{time}.txt"
        crash_path = config["paths"]["cwd"] / "data" / "logs" / crash_name

        trace = "".join(
            traceback.TracebackException.from_exception(err).format()
        )

        client_options = json.dumps(
            client.client_options,
            indent=4,
            sort_keys=True,
            default=lambda o: f"<<non-serializable: {repr(o)}>>",
        )
        cluster_options = json.dumps(
            client.cluster_options,
            indent=4,
            sort_keys=True,
            default=lambda o: f"<<non-serializable: {repr(o)}>>",
        )

        report = f"Crash Report [{cluster_id}] {time}:\n\n"
        report += trace

        report += "\n\nClient Options:"
        report += f"\n{client_options}"

        report += "\n\nCluster Options:"
        report += f"\n{cluster_options}"

        report += "\n\nCogs crash reports:"

        for module in client.cogs:
            if isinstance(module, ModuleABC) and hasattr(
                module, "crash_report"
            ):
                report += f"\n{module.crash_report()}\n"

        with open(str(crash_path), "w", encoding="UTF-8") as f:
            f.write(report)

        sys.exit(1)
