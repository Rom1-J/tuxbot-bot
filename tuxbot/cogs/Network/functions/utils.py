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
