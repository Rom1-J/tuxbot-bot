"""
Tuxbot core module: Tuxbot

Client class instance for Tuxbot
"""
import json
import sys
import traceback
from datetime import datetime
from typing import NoReturn, Tuple, List, Union

import aiohttp
import discord
from discord.ext import commands
from datadog import initialize
from jishaku import Jishaku

from tuxbot.core.collections.ModuleCollection import ModuleCollection

from tuxbot.abc.TuxbotABC import TuxbotABC

from tuxbot.core import redis
from tuxbot.core.config import config

initialize(
    statsd_host="192.168.1.197",
    statsd_port=8125,
    statsd_namespace="tuxbot_metric",
)


class Tuxbot(TuxbotABC):
    """
    Tuxbot client class
    """

    def __init__(self, options):
        self._config = config
        self._global_config = {"modules": {}, "PermissionsManager": {}}

        options = options or {}

        self.client_options, self.cluster_options = self.configure(options)
        super().__init__(**self.client_options)

    async def load_config(self):
        """Load configurations"""

        modules = ModuleCollection(self._config, self)
        modules.register(Jishaku)
        modules.load_modules()

        try:
            if hasattr(self.models, "Config"):
                db_config = await self.models.Config.findOne(
                    client_id=self.config["client"].id
                )

                if db_config:
                    self.config |= db_config

            # Todo: remove pylint disable when models done
            global_config = (
                await self.models.Tuxbot.findOne()  # pylint: disable=no-member
            )
            self.global_config = self.config["global_config"] = global_config
        except Exception as e:
            self.logger.error(e)

    async def launch(self) -> None:
        """Login to discord"""
        await self.load_config()

        try:
            self.redis = await redis.connect()
            self.logger.info("[Tuxbot] Redis connection established.")
        except Exception as e:
            self.logger.error(e)

        await super().start(config["client"]["token"])

    async def shutdown(self) -> None:
        """Disconnect from Discord and closes all actives connections."""
        await super().close()

    async def on_ready(self):
        """Ready event handler"""
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

    @staticmethod
    async def post_webhook(webhook: str, payload: Union[dict, discord.Embed]):
        """Post webhook

        Parameters
        ----------
        webhook:str
            Webhook URL
        payload:Union[dict, discord.Embed]
            Webhook data
        """
        async with aiohttp.ClientSession() as session:
            if isinstance(payload, discord.Embed):
                await discord.Webhook.from_url(webhook, session=session).send(
                    embed=payload
                )
            else:
                await session.post(webhook, json=payload)

    @staticmethod
    def configure(options: dict) -> Tuple[dict, dict]:
        """Configure Tuxbot"""

        async def get_prefix(
            bot: "Tuxbot", message: discord.Message
        ) -> List[str]:
            """Get bot prefixes from config or set it as mentionable"""
            if not (prefixes := config.get("prefixes")):
                prefixes = commands.when_mentioned(bot, message)

            return prefixes

        client_config = {
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
        }

        cluster_config = {
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

    @staticmethod
    def crash_report(client: "Tuxbot", err: Exception) -> NoReturn:
        """Generate crash report file and exit

        Parameters
        ----------
        client: :class:`Tuxbot`
            Tuxbot client instance
        err:Exception
            Crash exception

        Returns
        -------
        NoReturn
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
            if hasattr(module, "crash_report"):
                report += f"\n{module.crash_report()}\n"

        with open(str(crash_path), "w", encoding="UTF-8") as f:
            f.write(report)

        sys.exit(1)
