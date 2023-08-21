import asyncio
import typing

import aiohttp

from .abc import Provider


class OpenCageDataProvider(Provider):
    # pylint: disable=arguments-renamed
    async def fetch(
        self: typing.Self, latlon: str
    ) -> tuple[str, dict[str, typing.Any]]:
        try:
            async with aiohttp.ClientSession() as cs, cs.get(
                f"https://api.opencagedata.com/geocode/v1/json"
                f"?q={latlon}"
                f"&key={self.apikey}",
                timeout=aiohttp.ClientTimeout(total=2),
            ) as s:
                return "opencage", await s.json()
        except (aiohttp.ClientError, asyncio.exceptions.TimeoutError):
            pass

        return "opencage", {}
