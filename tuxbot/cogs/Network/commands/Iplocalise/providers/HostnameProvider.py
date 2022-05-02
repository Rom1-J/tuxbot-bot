import asyncio
import socket
from typing import Tuple

import aiohttp

from .abc import Provider


class HostnameProvider(Provider):
    async def fetch(self, ip: str) -> Tuple[str, str]:
        def _get_hostname(_ip: str):
            try:
                return socket.gethostbyaddr(_ip)[0]
            except (socket.gaierror, UnicodeError):
                return "N/A"

        try:
            return "hostname", await asyncio.wait_for(
                asyncio.get_running_loop().run_in_executor(
                    None, _get_hostname, str(ip)
                ),
                timeout=2,
            )
        except asyncio.exceptions.TimeoutError:
            return "hostname", "N/A"
