from structured_config import Structure, StrField

HAS_MODELS = False


class DevConfig(Structure):
    url: str = StrField("")
    login: str = StrField("")
    password: str = StrField("")


extra = {
    "url": {
        "type": str,
        "description": "URL of the YouTrack instance (without /youtrack/)",
    },
    "login": {"type": str, "description": "Login for YouTrack instance"},
    "password": {
        "type": str,
        "description": "Password for YouTrack instance",
    },
}
