"""
Tuxbot abstract class module: TuxbotABC

Contains all Tuxbot properties
"""

from datetime import datetime
from typing import Optional

import aioredis
from datadog import DogStatsd, statsd
from discord.ext import commands

from tuxbot.core.logger import Logger, logger, prom
from tuxbot.core.database import db
from tuxbot.core.utils import Utils, utils


class TuxbotABC(commands.AutoShardedBot):
    """Tuxbot Abstract Class"""

    _config: dict = {}
    _global_config: dict = {}

    _cluster_options: dict = {}
    _client_options: dict = {}

    _logger: logger  # type: ignore
    _db: db  # type: ignore
    _redis: aioredis.Redis

    _uptime: Optional[datetime] = None
    _last_on_ready: Optional[datetime] = None

    # =========================================================================
    # =========================================================================

    @property
    def config(self) -> dict:
        """Tuxbot configuration

        Returns
        -------
        dict
        """
        return self._config

    @config.setter
    def config(self, value: dict):
        self._config = value

    # =========================================================================

    @property
    def global_config(self) -> dict:
        """Tuxbot global configuration

        Returns
        -------
        dict
        """
        return self._global_config

    @global_config.setter
    def global_config(self, value: dict):
        self._global_config = value

    # =========================================================================

    @property
    def cluster_options(self) -> dict:
        """Tuxbot cluster options

        Returns
        -------
        dict
        """
        return self._cluster_options

    @cluster_options.setter
    def cluster_options(self, value: dict):
        self._cluster_options = value

    # =========================================================================

    @property
    def client_options(self) -> dict:
        """Tuxbot client options

        Returns
        -------
        dict
        """
        return self._client_options

    @client_options.setter
    def client_options(self, value: dict):
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
    def db(self) -> db:  # type: ignore
        """DB instance

        Returns
        -------
        db
        """
        return db

    # =========================================================================

    @property
    def models(self) -> db:  # type: ignore
        """DB models

        Returns
        -------
        db
        """
        return db.models  # pylint: disable=no-member

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
    def redis(self, value: aioredis.Redis):
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
    def uptime(self, value: datetime):
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
    def last_on_ready(self, value: datetime):
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
    def utils(self) -> Utils:  # type: ignore
        """Tuxbot utils set

        Returns
        -------
        Utils
        """
        return utils

    # =========================================================================

    @property
    def prom(self) -> prom:
        """Prometheus instance

        Returns
        -------
        prom
        """
        return prom

    # =========================================================================
    # =========================================================================
