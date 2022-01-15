from aiocache import cached, Cache
from aiocache.serializers import PickleSerializer

from tuxbot.cogs.Linux.functions.cnf import CNF


@cached(
    ttl=24 * 3600,
    serializer=PickleSerializer(),
    cache=Cache.MEMORY,
    namespace="linux",
)
async def get_from_cnf(command: str) -> dict:
    cnf = CNF(command)
    await cnf.fetch()

    return cnf.to_dict()
