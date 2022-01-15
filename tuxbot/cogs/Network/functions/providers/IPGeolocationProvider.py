import asyncio

import aiohttp

from .abc import Provider


class IPGeolocationProvider(Provider):
    async def fetch(self, ip: str) -> dict:
        try:
            async with aiohttp.ClientSession() as cs, cs.get(
                f"https://api.ipgeolocation.io/ipgeo?apiKey={self.apikey}&ip={ip}",
                timeout=aiohttp.ClientTimeout(total=2),
            ) as s:
                return await s.json()
        except (aiohttp.ClientError, asyncio.exceptions.TimeoutError):
            pass

        return {}
