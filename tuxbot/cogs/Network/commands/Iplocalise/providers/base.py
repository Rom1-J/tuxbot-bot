"""
tuxbot.cogs.Network.functions.providers.base
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Global provider which uses all sub provider
"""
import asyncio
import typing

from tuxbot.core.config import config

from . import (
    HostnameProvider,
    IPGeolocationProvider,
    IPInfoProvider,
    IPWhoisProvider,
    MapProvider,
    OpenCageDataProvider,
)


def get_base_providers(data: dict[str, typing.Any]) -> dict[str, typing.Any]:
    """Get result from base providers"""

    hostname = HostnameProvider()
    ipgeo = IPGeolocationProvider(config.IPGEOLOCATION_KEY)
    ipinfo = IPInfoProvider(config.IPINFO_KEY)
    ipwhois = IPWhoisProvider()

    result = {
        "hostname": asyncio.create_task(hostname.fetch(data["ip"])),
        "ipgeo": asyncio.create_task(ipgeo.fetch(data["ip"])),
        "ipinfo": asyncio.create_task(ipinfo.fetch(data["ip"])),
        "ipwhois": asyncio.create_task(ipwhois.fetch(data["ip"])),
    }

    return result


def get_auxiliary_providers(
    data: dict[str, typing.Any]
) -> dict[str, typing.Any]:
    """Get result from auxiliary providers"""

    loc = data["ipinfo"].get("loc", "")

    map_location = MapProvider(config.GEOAPIFY_KEY)
    opencage = OpenCageDataProvider(config.OPENCAGEDATA_KEY)

    result = {
        "map": asyncio.create_task(map_location.fetch(loc)),
        "opencage": asyncio.create_task(opencage.fetch(loc.replace(",", "+"))),
    }

    return result
