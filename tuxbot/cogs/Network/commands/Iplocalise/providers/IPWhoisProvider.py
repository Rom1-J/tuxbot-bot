import asyncio
from typing import Tuple

import ipwhois
from ipwhois import IPWhois

from ...exceptions import RFC1918
from .abc import Provider


class IPWhoisProvider(Provider):
    async def fetch(self, ip: str) -> Tuple[str, dict]:
        def _get_ipwhois_result(_ip: str) -> dict:
            try:
                obj = IPWhois(ip)
                return obj.lookup_whois()

            except ipwhois.exceptions.ASNRegistryError:
                return {}

            except ipwhois.exceptions.IPDefinedError as e:
                raise RFC1918(
                    "This IP address defined as Private-Use Networks via "
                    "RFC 1918."
                ) from e

        try:
            return "ipwhois", await asyncio.wait_for(
                asyncio.get_running_loop().run_in_executor(
                    None, _get_ipwhois_result, str(ip)
                ),
                timeout=2,
            )
        except asyncio.exceptions.TimeoutError:
            return "ipwhois", {}
