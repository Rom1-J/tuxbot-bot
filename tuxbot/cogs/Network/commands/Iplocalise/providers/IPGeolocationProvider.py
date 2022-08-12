import asyncio
import typing

import aiohttp

from .abc import Provider


class IPGeolocationProvider(Provider):
    async def fetch(self, ip: str) -> tuple[str, dict[str, typing.Any]]:
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
