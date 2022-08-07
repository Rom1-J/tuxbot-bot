"""
Tuxbot core module: redis

Manage redis instances
"""
from aioredis.client import Redis


def connect() -> Redis:
    """Connector for redis instance

    Returns
    -------
    aioredis.Redis
    """
    return Redis(db=1)
