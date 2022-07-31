"""
tuxbot.cogs.Network.functions.providers.base
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Global provider which uses all sub provider
"""
import asyncio

from . import (
    HostnameProvider,
    IPGeolocationProvider,
    IPInfoProvider,
    IPWhoisProvider,
    MapProvider,
    OpenCageDataProvider,
)


def get_base_providers(config: dict[str, str], data: dict) -> dict:
    """Get result from base providers"""

    hostname = HostnameProvider()
    ipgeo = IPGeolocationProvider(config["ipgeolocation_key"])
    ipinfo = IPInfoProvider(config["ipinfo_key"])
    ipwhois = IPWhoisProvider()

    result = {
        "hostname": asyncio.create_task(hostname.fetch(data["ip"])),
        "ipgeo": asyncio.create_task(ipgeo.fetch(data["ip"])),
        "ipinfo": asyncio.create_task(ipinfo.fetch(data["ip"])),
        "ipwhois": asyncio.create_task(ipwhois.fetch(data["ip"])),
    }

    return result


def get_auxiliary_providers(config: dict[str, str], data: dict) -> dict:
    """Get result from auxiliary providers"""

    loc = data["ipinfo"].get("loc", "")

    map_location = MapProvider(config["geoapify_key"])
    opencage = OpenCageDataProvider(config["opencagedata_key"])

    result = {
        "map": asyncio.create_task(map_location.fetch(loc)),
        "opencage": asyncio.create_task(opencage.fetch(loc.replace(",", "+"))),
    }

    return result
