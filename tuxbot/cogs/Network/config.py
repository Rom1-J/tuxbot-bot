from structured_config import Structure, StrField

HAS_MODELS = False


class NetworkConfig(Structure):
    ipinfoKey: str = StrField("")


extra = {
    "ipinfoKey": {
        "type": str,
        "description": "API Key for ipinfo.io (.iplocalise command)",
    },
}
