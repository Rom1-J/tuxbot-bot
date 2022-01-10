"""
Tuxbot core module: redis

Manage redis instances
"""
import aioredis


async def connect() -> aioredis.Redis:
    """Connector for redis instance

    Returns
    -------
    aioredis.Redis
    """
    return await aioredis.from_url("redis://localhost", db=1)
