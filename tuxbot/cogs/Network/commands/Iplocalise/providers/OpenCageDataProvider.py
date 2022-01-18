import asyncio

import aiohttp

from .abc import Provider


class OpenCageDataProvider(Provider):
    # pylint: disable=arguments-renamed
    async def fetch(self, latlon: str) -> dict:
        try:
            async with aiohttp.ClientSession() as cs, cs.get(
                f"https://api.opencagedata.com/geocode/v1/json?q={latlon}&key={self.apikey}",
                timeout=aiohttp.ClientTimeout(total=2),
            ) as s:
                return await s.json()
        except (aiohttp.ClientError, asyncio.exceptions.TimeoutError):
            pass

        return {}
