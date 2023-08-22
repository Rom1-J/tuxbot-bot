"""
Tuxbot abstract class module: TuxbotABC.

Contains all Tuxbot properties
"""
import typing
from datetime import datetime

import discord
import redis as aioredis
import statsd
from discord.ext import commands

from tuxbot.core import utils
from tuxbot.core.database import Database, Models, db
from tuxbot.core.logger import Logger, logger


class TuxbotABC(commands.AutoShardedBot):
    """Tuxbot Abstract Class."""

    _cached_config: typing.ClassVar[dict[str | int, typing.Any]] = {}

    _client_options: typing.ClassVar[dict[str, typing.Any]] = {}

    _logger: Logger
    _db: Database
    _redis: aioredis.Redis

    _uptime: datetime | None = None
    _last_on_ready: datetime | None = None

    _running_instance: bool = True

    # =========================================================================
    # =========================================================================

    @property
    def cached_config(self: typing.Self) -> dict[str | int, typing.Any]:
        """
        Tuxbot cached configuration.

        Returns
        -------
        dict[str | int, typing.Any]
        """
        return self._cached_config

    # =========================================================================

    @property
    def client_options(self: typing.Self) -> dict[str, typing.Any]:
        """
        Tuxbot client options.

        Returns
        -------
        dict[str, typing.Any]
        """
        return self._client_options

    # =========================================================================

    @property
    def logger(self: typing.Self) -> Logger:
        """
        Logger.

        Returns
        -------
        Logger
        """
        return logger

    # =========================================================================

    @property
    def db(self: typing.Self) -> Database:
        """
        DB instance.

        Returns
        -------
        Database
        """
        return db

    # =========================================================================

    @property
    def models(self: typing.Self) -> Models:
        """
        DB models.

        Returns
        -------
        db
        """
        return db.models

    # =========================================================================

    @property
    def redis(self: typing.Self) -> aioredis.Redis:
        """
        Redis instance.

        Returns
        -------
        aioredis.Redis
        """
        return self._redis

    @redis.setter
    def redis(self: typing.Self, value: aioredis.Redis) -> None:
        self._redis = value

    # =========================================================================

    @property
    def uptime(self: typing.Self) -> datetime:
        """
        Uptime.

        Returns
        -------
        datetime
        """
        return self._uptime or datetime.fromtimestamp(0)

    @uptime.setter
    def uptime(self: typing.Self, value: datetime) -> None:
        self._uptime = value

    # =========================================================================

    @property
    def last_on_ready(self: typing.Self) -> datetime:
        """
        Latest on_ready registered event.

        Returns
        -------
        datetime
        """
        return self._last_on_ready or datetime.fromtimestamp(0)

    @last_on_ready.setter
    def last_on_ready(self: typing.Self, value: datetime) -> None:
        self._last_on_ready = value

    # =========================================================================

    @property
    def running_instance(self: typing.Self) -> bool:
        """
        Current instance running state.

        Returns
        -------
        bool
        """
        return self._running_instance

    @running_instance.setter
    def running_instance(self: typing.Self, value: bool) -> None:
        self.logger.info("[Tuxbot] 'running_instance' set to %s", value)
        self._running_instance = value

    # =========================================================================

    @property
    def statsd(self: typing.Self) -> statsd.StatsClient:
        """
        DogStatsd instance.

        Returns
        -------
        statsd.StatsClient
        """
        return statsd.StatsClient()

    # =========================================================================

    @property
    def utils(self: typing.Self) -> utils.Utils:
        """
        Tuxbot utils set.

        Returns
        -------
        utils.Utils
        """
        return utils.utils

    # =========================================================================
    # =========================================================================

    async def is_owner(self: typing.Self, user: discord.abc.User, /) -> bool:
        return await super().is_owner(user)
