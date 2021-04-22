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

from aiocache import cached
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


@cached(ttl=15 * 60, serializer=PickleSerializer())
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


@cached(ttl=15 * 60, serializer=PickleSerializer())
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


@cached(ttl=15 * 60, serializer=PickleSerializer())
async def get_ipwhois_result(loop, ip_address: str) -> NoReturn | dict:
    def _get_ipwhois_result(_ip_address: str) -> NoReturn | dict:
        try:
            net = Net(ip_address)
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
            loop.run_in_executor(None, _get_ipwhois_result, str(ip_address)),
            timeout=0.200,
        )
    except asyncio.exceptions.TimeoutError:
        return {}


@cached(ttl=15 * 60, serializer=PickleSerializer())
async def get_ipinfo_result(apikey: str, ip_address: str) -> dict:
    try:
        handler = ipinfo.getHandlerAsync(
            apikey, request_options={"timeout": 7}
        )
        return (await handler.getDetails(ip_address)).all
    except RequestQuotaExceededError:
        return {}


@cached(ttl=15 * 60, serializer=PickleSerializer())
async def get_crimeflare_result(
    session: aiohttp.ClientSession, ip_address: str
) -> Optional[str]:
    try:
        async with session.post(
            "http://www.crimeflare.org:82/cgi-bin/cfsearch.cgi",
            data=f"cfS={ip_address}",
            timeout=aiohttp.ClientTimeout(total=15),
        ) as s:
            ip = re.search(r"(\d*\.\d*\.\d*\.\d*)", await s.text())

            if ip:
                return ip.group()
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


@cached(ttl=15 * 60, serializer=PickleSerializer())
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


@cached(ttl=15 * 60, serializer=PickleSerializer())
async def get_peeringdb_as_set_result(
    session: aiohttp.ClientSession, asn: str
) -> Optional[dict]:
    try:
        async with session.get(
            f"https://www.peeringdb.com/api/as_set/{asn}",
            timeout=aiohttp.ClientTimeout(total=5),
        ) as s:
            return await s.json()
    except (
        aiohttp.ClientError,
        aiohttp.ContentTypeError,
        asyncio.exceptions.TimeoutError,
    ):
        pass

    return None


@cached(ttl=15 * 60, serializer=PickleSerializer())
async def get_peeringdb_net_irr_as_set_result(
    session: aiohttp.ClientSession, asn: str
) -> Optional[dict]:
    try:
        async with session.get(
            f"https://www.peeringdb.com/api/net?irr_as_set={asn}",
            timeout=aiohttp.ClientTimeout(total=10),
        ) as s:
            json = await s.json()

            for data in json:
                if data["asn"] == int(asn):
                    return data
    except (
        aiohttp.ClientError,
        aiohttp.ContentTypeError,
        asyncio.exceptions.TimeoutError,
    ):
        pass

    return None


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
