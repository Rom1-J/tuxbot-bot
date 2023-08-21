import asyncio
import typing

import ipwhois
from ipwhois import IPWhois

from tuxbot.cogs.Network.commands.exceptions import RFCReserved

from .abc import Provider


class IPWhoisProvider(Provider):
    async def fetch(
        self: typing.Self, ip: str
    ) -> tuple[str, dict[str, typing.Any]]:
        def _get_ipwhois_result(_ip: str) -> dict[str, typing.Any]:
            try:
                obj = IPWhois(ip)
                return obj.lookup_whois()

            except ipwhois.exceptions.ASNRegistryError:
                return {}

            except ipwhois.exceptions.IPDefinedError as e:
                msg = (
                    "This IP address defined as Private-Use Networks "
                    "via RFC 1918."
                )
                raise RFCReserved(msg) from e

        try:
            return "ipwhois", await asyncio.wait_for(
                asyncio.get_running_loop().run_in_executor(
                    None, _get_ipwhois_result, str(ip)
                ),
                timeout=2,
            )
        except asyncio.exceptions.TimeoutError:
            return "ipwhois", {}
