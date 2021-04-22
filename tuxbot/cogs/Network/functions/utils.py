import socket
from typing import NoReturn, Optional

import asyncio
import re
import ipinfo
import ipwhois
import pydig
import aiohttp

from ipinfo.exceptions import RequestQuotaExceededError

from ipwhois import Net
from ipwhois.asn import IPASN

from aiocache import cached, Cache
from aiocache.serializers import PickleSerializer

from tuxbot.cogs.Network.functions.exceptions import (
    VersionNotFound,
    RFC18,
    InvalidIp,
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
async def get_ip(loop, ip: str, inet: str = "") -> str:
    _inet: socket.AddressFamily | int = 0  # pylint: disable=no-member

    if inet == "6":
        _inet = socket.AF_INET6
    elif inet == "4":
        _inet = socket.AF_INET

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
async def get_hostname(loop, ip: str) -> str:
    def _get_hostname(_ip: str):
        try:
            return socket.gethostbyaddr(ip)[0]
        except socket.herror:
            return "N/A"

    try:
        return await asyncio.wait_for(
            loop.run_in_executor(None, _get_hostname, str(ip)),
            timeout=0.200,
        )
    # assuming that if the hostname isn't retrieved in first .3sec,
    # it doesn't exists
    except asyncio.exceptions.TimeoutError:
        return "N/A"


@cached(
    ttl=24 * 3600,
    serializer=PickleSerializer(),
    cache=Cache.MEMORY,
    namespace="network",
)
async def get_ipwhois_result(loop, ip: str) -> NoReturn | dict:
    def _get_ipwhois_result(_ip: str) -> NoReturn | dict:
        try:
            net = Net(ip)
            obj = IPASN(net)
            return obj.lookup()
        except ipwhois.exceptions.ASNRegistryError:
            return {}
        except ipwhois.exceptions.IPDefinedError as e:
            raise RFC18(
                _(
                    "IP address {ip_address} is already defined as Private-Use"
                    " Networks via RFC 1918."
                )
            ) from e

    try:
        return await asyncio.wait_for(
            loop.run_in_executor(None, _get_ipwhois_result, str(ip)),
            timeout=0.200,
        )
    except asyncio.exceptions.TimeoutError:
        return {}


@cached(
    ttl=24 * 3600,
    serializer=PickleSerializer(),
    cache=Cache.MEMORY,
    namespace="network",
)
async def get_ipinfo_result(apikey: str, ip: str) -> dict:
    try:
        handler = ipinfo.getHandlerAsync(
            apikey, request_options={"timeout": 7}
        )
        return (await handler.getDetails(ip)).all
    except RequestQuotaExceededError:
        return {}


@cached(
    ttl=24 * 3600,
    serializer=PickleSerializer(),
    cache=Cache.MEMORY,
    namespace="network",
)
async def get_crimeflare_result(ip: str) -> Optional[str]:
    try:
        async with aiohttp.ClientSession() as cs:
            async with cs.post(
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


def merge_ipinfo_ipwhois(ipinfo_result: dict, ipwhois_result: dict) -> dict:
    output = {"belongs": "N/A", "rir": "N/A", "region": "N/A", "flag": "N/A"}

    if ipinfo_result:
        org = ipinfo_result.get("org", "N/A")
        asn = org.split()[0] if len(org.split()) > 1 else "N/A"

        output["belongs"] = f"[{org}](https://bgp.he.net/{asn})"
        output["rir"] = f"```{ipwhois_result.get('asn_registry', 'N/A')}```"
        output["region"] = (
            f"```{ipinfo_result.get('city', 'N/A')} - "
            f"{ipinfo_result.get('region', 'N/A')} "
            f"({ipinfo_result.get('country', 'N/A')})```"
        )
        output["flag"] = (
            f"https://www.countryflags.io/{ipinfo_result['country']}"
            f"/shiny/64.png"
        )
    elif ipwhois_result:
        org = ipwhois_result.get("asn_description", "N/A")
        asn = ipwhois_result.get("asn", "N/A")
        asn_country = ipwhois_result.get("asn_country_code", "N/A")

        output["belongs"] = f"{org} ([AS{asn}](https://bgp.he.net/{asn}))"
        output["rir"] = f"```{ipwhois_result['asn_registry']}```"
        output["region"] = f"```{asn_country}```"
        output[
            "flag"
        ] = f"https://www.countryflags.io/{asn_country}/shiny/64.png"

    return output


@cached(
    ttl=24 * 3600,
    serializer=PickleSerializer(),
    cache=Cache.MEMORY,
    namespace="network",
)
async def get_pydig_result(
    loop, domain: str, query_type: str, dnssec: str | bool
) -> list:
    additional_args = [] if dnssec is False else ["+dnssec"]

    def _get_pydig_result(_domain: str) -> NoReturn | dict:
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


@cached(
    ttl=24 * 3600,
    serializer=PickleSerializer(),
    cache=Cache.MEMORY,
    namespace="network",
)
async def get_peeringdb_net_result(asn: str) -> dict:
    try:
        async with aiohttp.ClientSession() as cs:
            async with cs.get(
                f"https://peeringdb.com/api/net?asn={asn}",
                timeout=aiohttp.ClientTimeout(total=21),
            ) as s:
                return await s.json()
    except (asyncio.exceptions.TimeoutError,):
        pass

    return {"data": []}


def check_ip_version_or_raise(version: str) -> bool | NoReturn:
    if version in ("4", "6", "None"):
        return True

    raise InvalidIp(_("Invalid ip version"))


def check_query_type_or_raise(query_type: str) -> bool | NoReturn:
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


def check_asn_or_raise(asn: str) -> bool | NoReturn:
    if asn.isdigit() and int(asn) < 4_294_967_295:
        return True

    raise InvalidAsn(_("Invalid ASN provided"))
