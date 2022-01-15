from typing import Dict

from structured_config import Structure, StrField

HAS_MODELS = False


class NetworkConfig(Structure):
    ipinfoKey: str = StrField("")
    geoapifyKey: str = StrField("")
    ipgeolocationKey: str = StrField("")
    opencagedataKey: str = StrField("")


extra: Dict[str, Dict] = {
    "ipinfoKey": {
        "type": str,
        "description": "API Key for ipinfo.io (.iplocalise command)",
    },
    "geoapifyKey": {
        "type": str,
        "description": "API Key for geoapify.com (.iplocalise command)",
    },
    "ipgeolocationKey": {
        "type": str,
        "description": "API Key for ipgeolocation.io (.iplocalise command)",
    },
    "opencagedataKey": {
        "type": str,
        "description": "API Key for opencagedata.io (.iplocalise command)",
    },
}
