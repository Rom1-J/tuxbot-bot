import asyncio
from typing import Tuple

import aiohttp

from .abc import Provider


class IPGeolocationProvider(Provider):
    async def fetch(self, ip: str) -> Tuple[str, dict]:
        try:
            async with aiohttp.ClientSession() as cs, cs.get(
                f"https://api.ipgeolocation.io/ipgeo"
                f"?apiKey={self.apikey}"
                f"&ip={ip}",
                timeout=aiohttp.ClientTimeout(total=2),
            ) as s:
                return "ipgeo", await s.json()
        except (aiohttp.ClientError, asyncio.exceptions.TimeoutError):
            pass

        return "ipgeo", {}
