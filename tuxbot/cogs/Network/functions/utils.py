import socket
from typing import NoReturn, Optional, Union

import asyncio
import re
import aiohttp
import pydig

from aiocache import cached, Cache
from aiocache.serializers import PickleSerializer

from tuxbot.cogs.Network.functions.exceptions import (
    VersionNotFound,
    InvalidQueryType,
    InvalidAsn,
)


def _(x):
    return x


@cached(
    ttl=24 * 3600,
    serializer=PickleSerializer(),
    cache=Cache.MEMORY,
    namespace="network",
)
async def get_ip(loop, ip: str, inet: Optional[int]) -> str:
    _inet: Union[socket.AddressFamily, int] = 0  # pylint: disable=no-member

    if inet:
        _inet = socket.AF_INET6 if inet == 6 else socket.AF_INET

    def _get_ip(_ip: str):
        try:
            return socket.getaddrinfo(_ip, None, _inet)[1][4][0]
        except socket.gaierror as e:
            raise VersionNotFound(
                _(
                    "Unable to collect information on this in the given "
                    "version",
                )
            ) from e

    return await loop.run_in_executor(None, _get_ip, str(ip))


@cached(
    ttl=24 * 3600,
    serializer=PickleSerializer(),
    cache=Cache.MEMORY,
    namespace="network",
)
async def get_crimeflare_result(ip: str) -> Optional[str]:
    try:
        async with aiohttp.ClientSession() as cs, cs.post(
            "http://www.crimeflare.org:82/cgi-bin/cfsearch.cgi",
            data=f"cfS={ip}",
            timeout=aiohttp.ClientTimeout(total=21),
        ) as s:
            result = re.search(r"(\d*\.\d*\.\d*\.\d*)", await s.text())

            if result:
                return result.group()
    except (aiohttp.ClientError, asyncio.exceptions.TimeoutError):
        pass

    return None


@cached(
    ttl=24 * 3600,
    serializer=PickleSerializer(),
    cache=Cache.MEMORY,
    namespace="network",
)
async def get_pydig_result(
    loop, domain: str, query_type: str, dnssec: Union[str, bool]
) -> list:
    additional_args = [] if dnssec is False else ["+dnssec"]

    def _get_pydig_result(_domain: str) -> Union[NoReturn, dict]:
        resolver = pydig.Resolver(
            nameservers=[
                "80.67.169.40",
                "80.67.169.12",
            ],
            additional_args=additional_args,
        )

        return resolver.query(_domain, query_type)

    try:
        return await asyncio.wait_for(
            loop.run_in_executor(None, _get_pydig_result, str(domain)),
            timeout=0.500,
        )
    except asyncio.exceptions.TimeoutError:
        return []


def check_query_type_or_raise(query_type: str) -> Union[bool, NoReturn]:
    query_types = (
        "a",
        "aaaa",
        "cname",
        "ns",
        "ds",
        "dnskey",
        "soa",
        "txt",
        "ptr",
        "mx",
    )

    if query_type in query_types:
        return True

    raise InvalidQueryType(
        _(
            "Supported queries : A, AAAA, CNAME, NS, DS, DNSKEY, SOA, TXT, PTR, MX"
        )
    )


def check_asn_or_raise(asn: str) -> Union[bool, NoReturn]:
    if asn.isdigit() and int(asn) < 4_294_967_295:
        return True

    raise InvalidAsn(_("Invalid ASN provided"))
