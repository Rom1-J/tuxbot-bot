"""
Tuxbot core module: redis.

Manage redis instances
"""
from aioredis.client import Redis

from tuxbot.core.config import config


def connect() -> Redis:
    """
    Connector for redis instance.

    Returns
    -------
    aioredis.Redis
    """
    return Redis().from_url(config.REDIS["default"])
