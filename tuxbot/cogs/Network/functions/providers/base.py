"""
tuxbot.cogs.Network.functions.providers.base
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Global provider which uses all sub provider
"""

from typing import Dict

from . import (
    IPGeolocationProvider,
    IPInfoProvider,
    IPWhoisProvider,
    MapProvider,
    OpenCageDataProvider,
)


async def get_all_providers(config: Dict[str, str], data: dict) -> dict:
    """Get result from all providers"""

    ip, domain = data["ip"], data["domain"]

    ipgeo = IPGeolocationProvider(config["ipgeolocation_key"])
    ipinfo = IPInfoProvider(config["ipinfo_key"])
    ipwhois = IPWhoisProvider()
    map_location = MapProvider(config["geoapify_key"])
    opencage = OpenCageDataProvider(config["opencagedata_key"])

    result = {
        "ip": ip,
        "domain": domain,
        "ipgeo": await ipgeo.fetch(ip),
        "ipinfo": await ipinfo.fetch(ip),
        "ipwhois": await ipwhois.fetch(ip),
    }

    result["map"] = await map_location.fetch(result["ipinfo"].get("loc", ""))
    result["opencage"] = await opencage.fetch(
        result["ipinfo"].get("loc", "").replace(",", "+")
    )

    return result
