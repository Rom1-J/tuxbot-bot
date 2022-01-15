from typing import Dict

from structured_config import Structure, StrField

HAS_MODELS = False


class MathConfig(Structure):
    WolframAlphaKey: str = StrField("")


extra: Dict[str, Dict] = {
    "WolframAlphaKey": {
        "type": str,
        "description": "API Key for wolframalpha.com (.wolf command)",
    },
}
