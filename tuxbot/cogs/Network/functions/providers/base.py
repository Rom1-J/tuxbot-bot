from typing import TYPE_CHECKING

from ...config import NetworkConfig

from . import (
    IPGeolocationProvider,
    IPInfoProvider,
    IPWhoisProvider,
    MapProvider,
    OpenCageDataProvider,
)

if TYPE_CHECKING:
    from tuxbot.core.bot import Tux


async def get_all_providers(config: NetworkConfig, data: dict) -> dict:
    ip, domain = data["ip"], data["domain"]

    ipgeo = IPGeolocationProvider(config.ipgeolocationKey)
    ipinfo = IPInfoProvider(config.ipinfoKey)
    ipwhois = IPWhoisProvider()
    map_location = MapProvider(config.geoapifyKey)
    opencage = OpenCageDataProvider(config.opencagedataKey)

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
