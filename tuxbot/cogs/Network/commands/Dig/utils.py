"""
tuxbot.cogs.Network.functions.Dig.utils
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Set of utils functions
"""

import asyncio
from typing import Any, Dict

import aiohttp


async def get_from_bortzmeyer(domain: str, query_type: str) -> Dict[str, Any]:
    """Get result from https://dns.bortzmeyer.org/"""

    try:
        async with aiohttp.ClientSession() as cs, cs.get(
            f"https://dns.bortzmeyer.org/{domain}/{query_type}?format=json",
            timeout=aiohttp.ClientTimeout(total=2),
        ) as s:
            return await s.json()
    except (aiohttp.ClientError, asyncio.exceptions.TimeoutError):
        pass

    return {}
