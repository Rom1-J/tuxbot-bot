from structured_config import Structure, StrField


class AdminConfig(Structure):
    dm: str = StrField("")
    mentions: str = StrField("")
    guilds: str = StrField("")
    errors: str = StrField("")
    gateway: str = StrField("")


extra = {
    'dm': str,
    'mentions': str,
    'guilds': str,
    'errors': str,
    'gateway': str,
}
