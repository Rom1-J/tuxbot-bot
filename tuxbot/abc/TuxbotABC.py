"""
Tuxbot abstract class module: TuxbotABC

Contains all Tuxbot properties
"""
from datetime import datetime
from typing import Optional, Dict, Union

import aioredis
from datadog import DogStatsd, statsd
from discord.ext import commands

from tuxbot.core.collections.CommandCollection import CommandCollection
from tuxbot.core.collections.ModuleCollection import ModuleCollection

from tuxbot.core.managers.EventManager import EventManager
from tuxbot.core.managers.WebhookManager import WebhookManager
from tuxbot.core.managers.PermissionsManager import PermissionsManager

from tuxbot.core.logger import logger, prom
from tuxbot.core.database import db
from tuxbot.core import utils

_C = Union[CommandCollection, ModuleCollection]
_M = Union[WebhookManager, PermissionsManager]


class TuxbotABC(commands.AutoShardedBot):
    """Tuxbot Abstract Class"""

    _config: dict = {}
    _global_config: dict = {}

    _cluster_options: dict = {}
    _client_options: dict = {}

    _logger: logger
    _db: db
    _redis: aioredis.Redis

    _uptime: Optional[datetime] = None
    _last_on_ready: Optional[datetime] = None

    _collections: Optional[Dict[str, _C]]
    _managers: Optional[Dict[str, _M]]
    _dispatcher: Optional[EventManager] = None

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
    def logger(self) -> logger:
        """Logger

        Returns
        -------
        logger
        """
        return logger

    # =========================================================================

    @property
    def db(self) -> db:
        """DB instance

        Returns
        -------
        db
        """
        return db

    # =========================================================================

    @property
    def models(self) -> db:
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
        return self._uptime

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
        return self._last_on_ready

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
    def utils(self) -> utils:
        """Tuxbot utils set

        Returns
        -------
        utils
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

    @property
    def dispatcher(self) -> EventManager:
        """EventManager instance

        Returns
        -------
        EventManager
        """
        return self._dispatcher

    @dispatcher.setter
    def dispatcher(self, value: EventManager):
        self._dispatcher = value

    # =========================================================================

    @property
    def collections(self) -> Dict[str, _C]:
        """Collections instance

        Returns
        -------
        Dict[str, _C]
        """
        return self._collections

    @collections.setter
    def collections(self, value: Dict[str, _C]):
        self._collections = value

    # =========================================================================

    @property
    def managers(self) -> Dict[str, _M]:
        """Managers instance

        Returns
        -------
        Dict[str, _M]
        """
        return self._managers

    @managers.setter
    def managers(self, value: Dict[str, _M]):
        self._managers = value

    # =========================================================================
    # =========================================================================
