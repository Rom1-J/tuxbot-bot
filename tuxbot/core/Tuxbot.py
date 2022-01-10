"""
Tuxbot core module: Tuxbot

Client class instance for Tuxbot
"""
import json
import sys
import traceback
from datetime import datetime
from typing import NoReturn, Tuple

import aiohttp
import discord
from datadog import initialize

from tuxbot.abc.TuxbotABC import TuxbotABC

from tuxbot.core import redis
from tuxbot.core.config import config

from tuxbot.core.collections.CommandCollection import CommandCollection
from tuxbot.core.collections.ModuleCollection import ModuleCollection

from tuxbot.core.managers.PermissionsManager import PermissionsManager
from tuxbot.core.managers.WebhookManager import WebhookManager
from tuxbot.core.managers.EventManager import EventManager

initialize(**{
    'statsd_host': '127.0.0.1',
    'statsd_port': 8125
})


class Tuxbot(TuxbotABC):
    """
    Tuxbot client class
    """

    def __init__(self, options):
        self._config = config
        self._global_config = {
            "modules": {},
            "PermissionsManager": {}
        }

        # Create collections
        self.collections = {
            "commands": CommandCollection(config, self),
            "modules": ModuleCollection(config, self),
        }

        # Create managers
        self.managers = {
            "webhooks": WebhookManager(self),
            "permissions": PermissionsManager(self)
        }

        options = options or {}

        self.client_options, self.cluster_options = self.configure(options)
        super(Tuxbot, self).__init__(**self.client_options)

    async def load_config(self):
        """Load configurations"""
        try:
            if hasattr(self.models, "Config"):
                db_config = await self.models.Config.findOne(
                    client_id=self.config["client"].id
                )

                if db_config:
                    self.config |= db_config

            global_config = await self.models.Tuxbot.findOne()
            self.global_config = self.config["global_config"] = global_config
        except Exception as e:
            self.logger.error(e)

    async def launch(self) -> None:
        """Login to discord"""
        await self.load_config()

        try:
            self.redis = await redis.connect()
        except Exception as e:
            self.logger.error(e)

        self.dispatcher = EventManager(self)
        await self.collections.get("modules").load_modules()

        await super(Tuxbot, self).start(config["client"]["token"])

    async def shutdown(self) -> None:
        """Disconnect from Discord and closes all actives connections."""
        await super().close()

    async def on_ready(self):
        """Ready event handler"""
        if self.uptime is not None:
            self.last_on_ready = datetime.now()
            return

        self.uptime = datetime.now()
        self.last_on_ready = self.uptime

        self.logger.info(
            f"[Tuxbot] {self.config['name']} "
            f"ready with {len(self.guilds)} guilds."
        )

        self.logger.debug(self._listeners)

        if game := self.config["client"].get("game"):
            await self.change_presence(
                status=discord.Status.online,
                activity=discord.Game(game)
            )

    @staticmethod
    async def post_webhook(webhook: str, payload: dict):
        """Post webhook

        Parameters
        ----------
        webhook:str
            Webhook URL
        payload:dict
            Webhook data
        """
        async with aiohttp.ClientSession() as session:
            await session.post(webhook, json=payload)

    @staticmethod
    def configure(options: dict) -> Tuple[dict, dict]:
        """Configure Tuxbot"""

        client_config = {
            "disable_events": {
                "TYPING_START": True
            },
            "allowed_mentions": discord.AllowedMentions(
                everyone=(not config["client"]["disable_everyone"]) or False
            ),
            "max_messages": int(config["client"]["max_cached_messages"]) or 10000,
            "command_prefix": config["prefix"] if hasattr(config, 'prefix') else ".",
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
        client:Tuxbot
            Tuxbot client instance
        err:Exception
            Crash exception

        Returns
        -------
        NoReturn
        """
        cluster_id = f"C{client.cluster_options.get('cluster_id')}"
        time = datetime.utcnow().isoformat()
        trace = "".join(
            traceback.TracebackException.from_exception(err).format()
        )
        client_options = json.dumps(
            client.client_options,
            indent=4,
            sort_keys=True,
            default=lambda o: f"<<non-serializable: {repr(o)}>>"
        )
        cluster_options = json.dumps(
            client.cluster_options,
            indent=4,
            sort_keys=True,
            default=lambda o: f"<<non-serializable: {repr(o)}>>"
        )

        report = f"Crash Report [{cluster_id}] {time}:\n\n"
        report += trace

        report += "\n\nClient Options:"
        report += f"\n{client_options}"

        report += "\n\nCluster Options:"
        report += f"\n{cluster_options}"

        for module in client.collections.get("modules").values():
            if hasattr(module, "crash_report"):
                report += f"\n\n{module.crash_report()}"

        with open(f"logs/crashreport_{cluster_id}_{time}.txt", "w") as f:
            f.write(report)

        return sys.exit(1)

