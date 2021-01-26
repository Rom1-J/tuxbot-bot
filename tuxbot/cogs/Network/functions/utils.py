import socket
from typing import Union, NoReturn

import ipinfo
import ipwhois
from ipinfo.exceptions import RequestQuotaExceededError

from ipwhois import Net
from ipwhois.asn import IPASN

from tuxbot.cogs.Network.functions.exceptions import VersionNotFound, RFC18


def _(x):
    return x


async def get_ip(ip: str, inet: str = "") -> str:
    if inet == "6":
        inet = socket.AF_INET6
    elif inet == "4":
        inet = socket.AF_INET
    else:
        inet = 0

    try:
        return socket.getaddrinfo(str(ip), None, inet)[1][4][0]
    except socket.gaierror as e:
        raise VersionNotFound(
            _(
                "Impossible to collect information on this in the given "
                "version",
            )
        ) from e


def get_hostname(ip: str) -> str:
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return "N/A"


def get_ipwhois_result(ip_address: str) -> Union[NoReturn, dict]:
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
        org = ipinfo_result.get("org", "")
        asn = org.split()[0]

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
