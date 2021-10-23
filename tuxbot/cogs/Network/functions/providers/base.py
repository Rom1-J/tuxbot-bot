from ...config import NetworkConfig

from . import (
    IPGeolocationProvider,
    IPInfoProvider,
    IPWhoisProvider,
    MapProvider,
    OpenCageDataProvider,
)


async def get_all_providers(config: NetworkConfig, data: dict) -> dict:
    ip, domain, cache_key = data["ip"], data["domain"], data["cache_key"]

    ipgeo = IPGeolocationProvider(config.ipgeolocationKey)
    ipinfo = IPInfoProvider(config.ipinfoKey)
    ipwhois = IPWhoisProvider()
    map_location = MapProvider(config.geoapifyKey)
    opencage = OpenCageDataProvider(config.opencagedataKey)

    result = {
        "ip": ip,
        "domain": domain,
        "cache_key": cache_key,
        "ipgeo": await ipgeo.fetch(ip),
        "ipinfo": await ipinfo.fetch(ip),
        "ipwhois": await ipwhois.fetch(ip),
    }

    result["map"] = await map_location.fetch(result["ipinfo"].get("loc", ""))
    result["opencage"] = await opencage.fetch(
        result["ipinfo"].get("loc", "").replace(",", "+")
    )

    return result
