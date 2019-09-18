import logging

import asyncpg

log = logging.getLogger(__name__)


class Table:
    @classmethod
    async def create_pool(cls, uri, **kwargs) -> asyncpg.pool.Pool:
        cls._pool = db = await asyncpg.create_pool(uri, **kwargs)
        return db
