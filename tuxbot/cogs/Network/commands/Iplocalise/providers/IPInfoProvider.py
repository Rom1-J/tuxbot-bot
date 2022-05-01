import asyncio
from typing import Tuple

import ipinfo
from ipinfo.exceptions import RequestQuotaExceededError

from .abc import Provider


class IPInfoProvider(Provider):
    async def fetch(self, ip: str) -> Tuple[str, dict]:
        def _get_ipinfo_result(_ip: str) -> dict:
            """
            Q. Why no getHandlerAsync ?
            A. Use of this return "Unclosed client session" and
            "Unclosed connector"
            """
            try:
                handler = ipinfo.getHandler(self.apikey)
                return (handler.getDetails(ip)).all
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
