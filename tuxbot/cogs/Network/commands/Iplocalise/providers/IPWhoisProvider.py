import asyncio

import ipwhois
from ipwhois import IPWhois

from .abc import Provider
from ..exceptions import RFC1819


class IPWhoisProvider(Provider):
    async def fetch(self, ip: str) -> dict:
        def _get_ipwhois_result(_ip: str) -> dict:
            try:
                obj = IPWhois(ip)
                return obj.lookup_whois()

            except ipwhois.exceptions.ASNRegistryError:
                return {}

            except ipwhois.exceptions.IPDefinedError as e:
                raise RFC1819(
                    "This IP address defined as Private-Use Networks via RFC 1918."
                ) from e

        try:
            return await asyncio.wait_for(
                asyncio.get_running_loop().run_in_executor(
                    None, _get_ipwhois_result, str(ip)
                ),
                timeout=2,
            )
        except asyncio.exceptions.TimeoutError:
            return {}
