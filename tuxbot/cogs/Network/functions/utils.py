import socket
from typing import Union, NoReturn

import discord
import ipinfo
import ipwhois
import pydig
from ipinfo.exceptions import RequestQuotaExceededError

from ipwhois import Net
from ipwhois.asn import IPASN

from tuxbot.cogs.Network.functions.exceptions import (
    VersionNotFound,
    RFC18,
    InvalidIp,
    InvalidQueryType,
)


def _(x):
    return x


async def get_ip(ip: str, inet: str = "", tmp: discord.Message = None) -> str:
    if inet == "6":
        inet = socket.AF_INET6
    elif inet == "4":
        inet = socket.AF_INET
    else:
        inet = 0

    try:
        return socket.getaddrinfo(str(ip), None, inet)[1][4][0]
    except socket.gaierror as e:
        if tmp:
            await tmp.delete()

        raise VersionNotFound(
            _(
                "Unable to collect information on this in the given "
                "version",
            )
        ) from e


async def get_hostname(ip: str) -> str:
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return "N/A"


async def get_ipwhois_result(
    ip_address: str, tmp: discord.Message = None
) -> Union[NoReturn, dict]:
    try:
        net = Net(ip_address)
        obj = IPASN(net)
        return obj.lookup()
    except ipwhois.exceptions.ASNRegistryError:
        return {}
    except ipwhois.exceptions.IPDefinedError as e:
        if tmp:
            await tmp.delete()

        raise RFC18(
            _(
                "IP address {ip_address} is already defined as Private-Use"
                " Networks via RFC 1918."
            )
        ) from e


async def get_ipinfo_result(
    apikey: str, ip_address: str
) -> Union[NoReturn, dict]:
    try:
        handler = ipinfo.getHandlerAsync(apikey)
        return (await handler.getDetails(ip_address)).all
    except RequestQuotaExceededError:
        return {}


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


async def get_pydig_result(
    domain: str, query_type: str, dnssec: Union[str, bool]
) -> list:
    additional_args = [] if dnssec is False else ["+dnssec"]

    resolver = pydig.Resolver(
        nameservers=[
            "80.67.169.40",
            "80.67.169.12",
        ],
        additional_args=additional_args,
    )

    return resolver.query(domain, query_type)


def check_ip_version_or_raise(version: str) -> Union[bool, NoReturn]:
    if version in ["4", "6", ""]:
        return True

    raise InvalidIp(_("Invalid ip version"))


def check_query_type_or_raise(query_type: str) -> Union[bool, NoReturn]:
    query_types = [
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
    ]

    if query_type in query_types:
        return True

    raise InvalidQueryType(
        _(
            "Supported queries : A, AAAA, CNAME, NS, DS, DNSKEY, SOA, TXT, PTR, MX"
        )
    )
