"""
tuxbot.cogs.Network.functions.Getheaders.utils
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Set of utils functions
"""

import asyncio
import socket
from urllib.parse import urlparse

import aiohttp
import ipwhois
from ipwhois import IPWhois

from ..exceptions import RFC1918
from .exceptions import UnreachableAddress


async def check_for_rfc1918_or_raise(ip: str) -> bool:
    """Check for RFC1918 or raise"""

    def _check_for_rfc1918_or_raise(_ip: str) -> None:
        try:
            IPWhois(
                socket.getaddrinfo(urlparse(_ip).netloc, None)[1][4][0]
            ).lookup_whois()
        except ipwhois.exceptions.IPDefinedError as e:
            raise RFC1918(
                "This IP address defined as Private-Use Networks via RFC 1918."
            ) from e

    try:
        return await asyncio.wait_for(
            asyncio.get_running_loop().run_in_executor(
                None, _check_for_rfc1918_or_raise, str(ip)  # type: ignore
            ),
            timeout=2,
        )
    except asyncio.exceptions.TimeoutError:
        raise UnreachableAddress("Failed to reach this address.")


async def get_headers(ip: str, user_agent: str) -> tuple:
    """Retrieve address headers"""

    req_headers = {}

    if user_agent:
        req_headers["User-Agent"] = user_agent

    async with aiohttp.ClientSession() as cs, cs.get(
        str(ip),
        headers=req_headers,
        timeout=aiohttp.ClientTimeout(total=8),
    ) as s:
        # noinspection PyTypeChecker
        headers = dict(s.headers.items())
        headers.pop("Set-Cookie", headers)
        headers.pop("X-Client-IP", headers)

        return s, headers
