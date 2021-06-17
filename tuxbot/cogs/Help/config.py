from typing import Dict

from structured_config import Structure, StrField

HAS_MODELS = False


class HelpConfig(Structure):
    wikiUrl: str = StrField("")
    siteUrl: str = StrField("")
    discordUrl: str = StrField("")


extra: Dict[str, Dict] = {
    "wikiUrl": {
        "type": str,
        "description": "Tuxbot Wiki URL (.help command)",
    },
    "siteUrl": {
        "type": str,
        "description": "Tuxbot Site URL (.help command)",
    },
    "discordUrl": {
        "type": str,
        "description": "Tuxbot Discord URL (.help command)",
    },
}
