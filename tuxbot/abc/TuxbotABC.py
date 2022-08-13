"""
Tuxbot abstract class module: TuxbotABC

Contains all Tuxbot properties
"""
import typing
from datetime import datetime

import aioredis
import discord
from datadog.dogstatsd.base import DogStatsd, statsd
from discord.ext import commands

from tuxbot.core import utils
from tuxbot.core.database import Database, Models, db
from tuxbot.core.logger import Logger, logger


class TuxbotABC(commands.AutoShardedBot):
    """Tuxbot Abstract Class"""

    _config: dict[str | int, typing.Any] = {}
    _cached_config: dict[str | int, typing.Any] = {}

    _cluster_options: dict[str, typing.Any] = {}
    _client_options: dict[str, typing.Any] = {}

    _logger: Logger
    _db: Database
    _redis: aioredis.Redis

    _uptime: datetime | None = None
    _last_on_ready: datetime | None = None

    # =========================================================================
    # =========================================================================

    @property
    def config(self) -> dict[str | int, typing.Any]:
        """Tuxbot configuration

        Returns
        -------
        dict[str | int, typing.Any]
        """
        return self._config

    @config.setter
    def config(self, value: dict[str | int, typing.Any]) -> None:
        self._config = value

    # =========================================================================

    @property
    def cached_config(self) -> dict[str | int, typing.Any]:
        """Tuxbot cached configuration

        Returns
        -------
        dict[str | int, typing.Any]
        """
        return self._cached_config

    @cached_config.setter
    def cached_config(self, value: dict[str | int, typing.Any]) -> None:
        self._cached_config = value

    # =========================================================================

    @property
    def cluster_options(self) -> dict[str, typing.Any]:
        """Tuxbot cluster options

        Returns
        -------
        dict[str, typing.Any]
        """
        return self._cluster_options

    @cluster_options.setter
    def cluster_options(self, value: dict[str, typing.Any]) -> None:
        self._cluster_options = value

    # =========================================================================

    @property
    def client_options(self) -> dict[str, typing.Any]:
        """Tuxbot client options

        Returns
        -------
        dict[str, typing.Any]
        """
        return self._client_options

    @client_options.setter
    def client_options(self, value: dict[str, typing.Any]) -> None:
        self._client_options = value

    # =========================================================================

    @property
    def logger(self) -> Logger:
        """Logger

        Returns
        -------
        Logger
        """
        return logger

    # =========================================================================

    @property
    def db(self) -> Database:
        """DB instance

        Returns
        -------
        Database
        """
        return db

    # =========================================================================

    @property
    def models(self) -> Models:
        """DB models

        Returns
        -------
        db
        """
        return db.models

    # =========================================================================

    @property
    def redis(self) -> aioredis.Redis:
        """Redis instance

        Returns
        -------
        aioredis.Redis
        """
        return self._redis

    @redis.setter
    def redis(self, value: aioredis.Redis) -> None:
        self._redis = value

    # =========================================================================

    @property
    def uptime(self) -> datetime:
        """Uptime

        Returns
        -------
        datetime
        """
        return self._uptime or datetime.fromtimestamp(0)

    @uptime.setter
    def uptime(self, value: datetime) -> None:
        self._uptime = value

    # =========================================================================

    @property
    def last_on_ready(self) -> datetime:
        """Latest on_ready registered event

        Returns
        -------
        datetime
        """
        return self._last_on_ready or datetime.fromtimestamp(0)

    @last_on_ready.setter
    def last_on_ready(self, value: datetime) -> None:
        self._last_on_ready = value

    # =========================================================================

    @property
    def statsd(self) -> DogStatsd:
        """DogStatsd instance

        Returns
        -------
        DogStatsd
        """
        return statsd

    # =========================================================================

    @property
    def utils(self) -> utils.Utils:
        """Tuxbot utils set

        Returns
        -------
        utils.Utils
        """
        return utils.utils

    # =========================================================================
    # =========================================================================

    async def is_owner(self, user: discord.abc.User, /) -> bool:
        return await super().is_owner(user)
