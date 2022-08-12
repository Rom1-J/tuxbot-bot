import asyncio
import typing

import ipinfo
from ipinfo.exceptions import RequestQuotaExceededError

from .abc import Provider


class IPInfoProvider(Provider):
    async def fetch(self, ip: str) -> tuple[str, dict[str, typing.Any]]:
        def _get_ipinfo_result(_ip: str) -> dict[str, typing.Any]:
            """
            Q. Why no getHandlerAsync ?
            A. Use of this return "Unclosed client session" and
            "Unclosed connector"
            """
            try:
                handler = ipinfo.getHandler(self.apikey)
                return (handler.getDetails(ip)).all  # type: ignore
            except RequestQuotaExceededError:
                return {}

        try:
            return "ipinfo", await asyncio.wait_for(
                asyncio.get_running_loop().run_in_executor(
                    None, _get_ipinfo_result, str(ip)
                ),
                timeout=2,
            )
        except asyncio.exceptions.TimeoutError:
            return "ipinfo", {}
